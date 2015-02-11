#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Download subtitle files in batch.

Additional options allow for renaming video files and removing advertising
from subtitle files.


Sample download times...

SS
real    0m3.450s
user    0m0.900s
sys     0m0.138s

SUBSCOPE
real    0m8.807s
user    0m0.495s
sys     0m0.057s

PERISCOPE
real    0m15.234s
user    0m2.292s
sys     0m0.205s
"""

__program__ = 'subsystem'
__version__ = '0.3'


# --- BEGIN CODE --- #

from contextlib import contextmanager


class Config:   # pylint: disable=R0903
    """Store global script configuration values."""
    DOWNLOADER_DEFAULT = 'ss'
    DOWNLOADER_MODULES = ['periscope']
    DOWNLOADER_SCRIPTS = ['ss', 'subscope']
    DOWNLOADERS_SUPPORTED = DOWNLOADER_SCRIPTS + DOWNLOADER_MODULES

    # this is determined at runtime
    DOWNLOADERS_AVAILABLE = []


def download(downloader):
    """Return appropriate downloader."""

    if downloader not in Config.DOWNLOADERS_AVAILABLE:
        fatal_error("'%s' is not installed")

    if downloader == 'periscope':
        return download_periscope
    elif downloader == 'ss':
        return download_ss
    elif downloader == 'subscope':
        return download_subscope


def download_periscope(filepaths):
    """Download subtitles for multiple video files via periscope."""

    import os

    pids = [periscope(filepath) for filepath in filepaths]

    for pid in pids:
        os.waitpid(pid, 0)


def download_ss(filepaths):
    """Download subtitles for multiple video files via periscope."""

    import ss

    with null():
        # ss.main will strip arg[0]
        ss.main(['ss'] + filepaths)


def download_subscope(filepaths):
    """Download subtitles for multiple video files via subscope."""

    from subscope.core import DownloadFirstHandler, Subscope
    import sys

    handler = DownloadFirstHandler(Subscope())

    try:
        with null():
            handler.run(filepaths, ['en'])
    except KeyboardInterrupt:
        sys.exit(1)


def downloader_default():
    """Return an available Config.DOWNLOADER_DEFAULT."""

    if not Config.DOWNLOADERS_AVAILABLE:
        fatal_error()

    if Config.DOWNLOADER_DEFAULT in Config.DOWNLOADERS_AVAILABLE:
        return Config.DOWNLOADER_DEFAULT
    else:
        alternative = Config.DOWNLOADERS_AVAILABLE[0]
        warning("Default downloader '%s' is not available, using '%s' instead."
                % (Config.DOWNLOADER_DEFAULT, alternative))
        return alternative


def downloaders_available():
    """Return a list of subtitle downloaders available."""

    from importlib import import_module

    try:
        from distutil.spawn import find_executable
    except ImportError:
        from shutil import which as find_executable

    available = []

    scripts = ['periscope']
    for script in scripts:
        if find_executable(script):
            available.append(script)

    modules = ['ss', 'subscope']
    for module in modules:
        try:
            import_module(module)
            available.append(module)
        except:
            pass

    return available


def epilog_formatter():
    """Return text formatted for the usage description's epilog."""
    bold = '\033[1m'
    end = '\033[0m'
    available = Config.DOWNLOADERS_AVAILABLE.copy()
    index = available.index(Config.DOWNLOADER_DEFAULT)
    available[index] = bold + '(' + available[index] + ')' + end
    formatted = '  |  '.join(available)
    return 'Downloaders available: ' + formatted


def execute(*args):
    """Execute shell commands."""
    import subprocess

    subprocess.Popen(args,
                     stderr=subprocess.PIPE,
                     stdout=subprocess.PIPE)


def fatal_error(*args):
    """Print error message to stderr then exit."""

    import sys
    print('ERROR:', *args, file=sys.stderr)
    sys.exit(1)


def main():
    """Start application."""

    import os

    Config.DOWNLOADERS_AVAILABLE = downloaders_available()
    Config.DOWNLOADER_DEFAULT = downloader_default()

    options, arguments = parse()

    # create list of video files that don't have accompanying 'srt' subtitles
    targets = [p for p in arguments if os.path.isfile(p) and not
               os.path.exists(os.path.splitext(p)[0] + '.srt')]

    if options.rename:
        videos = [rename(p) for p in targets]
    else:
        videos = targets

    downloader = download(options.downloader)
    downloader(videos)

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
    execute('notify-send', '--urgency=normal', '--icon=edit-delete',
            'Periscope', 'Subtitles not downloaded successfully.\n'
            + os.path.basename(path))


@contextmanager
def null():
    """Temporarily redirect stdout and stderr to /dev/null."""

    import os
    import sys

    try:
        original_stderr = os.dup(sys.stderr.fileno())
        original_stdout = os.dup(sys.stdout.fileno())
        devnull = open(os.devnull, 'w')
        os.dup2(devnull.fileno(), sys.stderr.fileno())
        os.dup2(devnull.fileno(), sys.stdout.fileno())
        yield

    finally:
        if original_stderr is not None:
            os.dup2(original_stderr, sys.stderr.fileno())
        if original_stdout is not None:
            os.dup2(original_stdout, sys.stdout.fileno())
        if devnull is not None:
            devnull.close()


def parse():
    """Parse command-line arguments. Arguments may consist of any
    combination of directories, files, and options."""

    import argparse

    parser = argparse.ArgumentParser(
        add_help=False,
        description="Download subtitle files for videos.",
        epilog=epilog_formatter(),
        usage="%(prog)s [OPTIONS] FILES/FOLDERS")
    parser.add_argument(
        "-d", "--downloader",
        action="store",
        default=Config.DOWNLOADER_DEFAULT,
        dest="downloader",
        help="indicate downloader to use")
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        dest="quiet",
        help="do not display failure notifications via notify-send")
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
    icon = 'video-x-generic'

    # detect and configure dialog program
    if find_executable('yad'):
        args = ['yad',
                '--borders=5',
                '--entry',
                '--entry-label=Filename:',
                '--entry-text=' + basename,
                '--title=Batch Tool',
                '--window-icon=' + icon]
        retry_args = args + ['--text=<b>' + retry_text + '</b>',
                             '--text-align=center']

    elif find_executable('zenity'):
        base = ['zenity',
                '--entry',
                '--entry-text=' + basename,
                '--title=Batch Tool',
                '--window-icon=/usr/share/icons/elementary-xfce/mimes/24/' + icon]
        args = base + ['--text=Filename:']
        retry_args = base + ['--text=' + retry_text]

    else:
        fatal_error('ERROR: Please install yad (or zenity)')

    # display prompt
    try:
        new_basename = subprocess.check_output(args).decode().strip()
    except subprocess.CalledProcessError:
        sys.exit(1)

    # retry prompt if new filename already exists
    while os.path.exists(os.path.join(dirname, new_basename + extension)) and \
            new_basename != basename:
        try:
            new_basename = subprocess.check_output(retry_args).decode().strip()
        except subprocess.CalledProcessError:
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

    execute('xfce4-terminal',
            '--execute',
            'subnuker',
            '--gui',
            '--regex',
            *subtitles)


def warning(*args):
    """Print warning message to stderr."""

    import sys
    print('WARNING:', *args, file=sys.stderr)


if __name__ == '__main__':
    main()
