#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Download subtitle files in batch.

Additional options allow for renaming video files and removing advertising
from subtitle files.
"""

__program__ = 'subsystem'
__version__ = '0.1'


# --- BEGIN CODE --- #

def download(filenames):
    """Download subtitles for multiple video files."""

    try:
        from distutil.spawn import find_executable
    except ImportError:
        from shutil import which as find_executable

    if not find_executable('periscope'):
        fatal_error('Please install periscope.')

    import os

    pids = [periscope(filename) for filename in filenames]

    for pid in pids:
        os.waitpid(pid, 0)


def fatal_error():
    """Print error message then exit."""

    import sys

    print('ERROR:', *args, file=sys.stderr)
    sys.exit(1)


def execute(*args):
    """Execute shell commands."""
    import subprocess

    subprocess.Popen(args,
                     stderr=subprocess.PIPE,
                     stdout=subprocess.PIPE)


def main():
    """Start application."""

    import os

    options, arguments = parse()

    videos = []

    for video_path in arguments:
        srt_path = os.path.splitext(video_path)[0] + '.srt'
        if os.path.isfile(video_path) and not os.path.exists(srt_path):
            if options.rename:
                videos.append(rename(video_path))
            else:
                videos.append(video_path)

    download(videos)

    subtitles = []

    for video_path in videos:
        srt_path = os.path.splitext(video_path)[0] + '.srt'
        if os.path.isfile(srt_path):
            subtitles.append(srt_path)
        elif not options.quiet:
            notify(video_path)

    if options.scan and subtitles:
        scan(subtitles)


def notify(path):
    """Display a failure notification."""

    import os
    execute('notify-send', '--urgency=normal', '--icon=edit-delete', 'Periscope', 'Subtitles not downloaded successfully.\n' + os.path.basename(path))


def parse():
    """Parse command-line arguments. Arguments may consist of any
    combination of directories, files, and options."""

    import argparse

    parser = argparse.ArgumentParser(
        add_help=False,
        description="Download subtitle files for videos.",
        usage="%(prog)s OPTIONS FILES/FOLDERS")
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        dest="quiet",
        help="do not display notifications")
    parser.add_argument(
        "-r", "--rename",
        action="store_true",
        dest="rename",
        help="prompt to rename video files")
    parser.add_argument(
        "-s", "--scan",
        action="store_true",
        dest="scan",
        help="remove advertising from subtitle files")
    parser.add_argument(
        "-h", "--help",
        action="help",
        help=argparse.SUPPRESS)
    parser.add_argument(
        "--version",
        action="version",
        version="%s %s" % (__program__, __version__))
    parser.add_argument(
        action="append",
        dest="targets",
        help=argparse.SUPPRESS,
        nargs="*")

    options = parser.parse_args()
    arguments = options.targets[0]

    return options, arguments


def periscope(filename):
    """Open periscope subprocess."""

    from locale import getlocale
    import subprocess

    lang = getlocale()[0].split('_')[0].lower()
    args = ['periscope', '-l', lang, '--quiet', filename]
    process = subprocess.Popen(args,
                     stderr=subprocess.PIPE,
                     stdout=subprocess.PIPE)

    return process.pid


def prompt(path):
    """Prompt for a new file name."""

    try:
        from distutil.spawn import find_executable
    except ImportError:
        from shutil import which as find_executable

    import os
    import subprocess
    import sys

    filepath, extension = os.path.splitext(path)
    basename = os.path.basename(filepath)
    dirname = os.path.dirname(filepath)

    retry_text = 'Sorry, please try again...'

    # detect and configure dialog program
    if find_executable('yad'):
        args = ['yad', '--borders=5', '--entry', '--entry-label=Filename:', '--entry-text=' + basename, '--title=Batch Tool', '--window-icon=video-x-generic']
        retry_args = args + ['--text=<b>' + retry_text + '</b>', '--text-align=center']
    elif find_executable('zenity'):
        base = ['zenity', '--entry', '--entry-text=' + basename, '--title=Batch Tool', '--window-icon=/usr/share/icons/elementary-xfce/mimes/24/video-x-generic.png']
        args = base + ['--text=Filename:']
        retry_args = base + ['--text=' + retry_text]
    else:
        fatal_error('ERROR: Please install yad (or zenity)')

    # display prompt
    try:
        new_basename = subprocess.check_output(args).decode().strip()
    except CalledProcessError:
        sys.exit(1)

    # retry prompt if new filename already exists
    while os.path.exists(os.path.join(dirname, new_basename + extension)) and new_basename != basename:
        try:
            new_basename = subprocess.check_output(retry_args).decode().strip()
        except CalledProcessError:
            sys.exit(1)

    if new_basename == '':
        new_basename = basename

    return os.path.join(dirname, new_basename + extension)


def rename(path):
    """Rename a file if necessary."""

    new_path = prompt(path)

    if path != new_path:
        try:
            from shutil import move
        except ImportError:
            from os import rename as move

        move(path, new_path)

    return new_path


def scan(subtitles):
    """Remove advertising from subtitles."""

    execute('xfce4-terminal', '--execute', 'subnuker', '--gui', '--regex', *subtitles)


if __name__ == '__main__':
    main()