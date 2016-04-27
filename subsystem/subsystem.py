#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Download and process subtitle files in batch.

Additional options allow for renaming video files and removing advertising
from subtitle files.


Sample download times...

[ss]
real    0m3.450s
user    0m0.900s
sys     0m0.138s

[subscope]
real    0m8.807s
user    0m0.495s
sys     0m0.057s

[periscope]
real    0m15.234s
user    0m2.292s
sys     0m0.205s
"""

from contextlib import contextmanager
import os
import sys

# application imports
from . import __description__, __program__, __version__


class Config:   # pylint: disable=too-few-public-methods

    """Store global script configuration values."""

    # indicate the GUI terminal app (to be used with subnuker)
    TERMINAL = 'xfce4-terminal'

    # indicate the default subtitle download tool to be used
    DOWNLOADER_DEFAULT = 'ss'


class Downloader:

    """Functions to prepare and use the downloaders."""

    MODULES = ['ss']
    SCRIPTS = ['periscope', 'subscope']
    SUPPORTED = SCRIPTS + MODULES

    def __init__(self):
        self.available = self.getavailable()
        Config.DOWNLOADER_DEFAULT = self.getdefault()

    def getavailable(self):
        """Return a list of subtitle downloaders available."""

        from importlib import import_module

        available = []

        for script in self.SCRIPTS:
            if have(script):
                available.append(script)

        for module in self.MODULES:
            try:
                import_module(module)
                available.append(module)
            except ImportError:
                pass

        return sorted(available)

    def getdefault(self):
        """Return an available default downloader."""

        if not self.available:
            error('No supported downloaders available')
            print('\nPlease install one of the following:', file=sys.stderr)
            print(self.SUPPORTED, file=sys.stderr)
            sys.exit(1)

        default = Config.DOWNLOADER_DEFAULT

        if default in self.available:
            return default
        else:
            alternative = self.available[0]
            warning('Default downloader {!r} not available, using {!r} instead'
                    .format(Config.DOWNLOADER_DEFAULT, alternative))
            return alternative

    def download(self, paths, tool, language):
        """Download subtitles via a number of tools."""

        if tool not in self.available:
            fatal('{!r} is not installed'.format(tool))

        try:
            from subsystem import plugins
            downloader = plugins.__getattribute__(tool)
        except AttributeError:
            fatal('{!r} is not a supported download tool'.format(tool))

        try:
            if downloader.__code__.co_argcount is 2:
                downloader(paths, language)
            elif downloader.__code__.co_argcount is 1:
                downloader(paths)
        except:  # pylint: disable=bare-except
            if not check_connectivity():
                error('Internet connectivity appears to be disabled')
            else:
                error('{!r} experienced an unknown error'.format(tool))

    def epilog(self):
        """Return text formatted for the usage description's epilog."""

        bold = '\033[1m'
        end = '\033[0m'
        available = self.available.copy()
        index = available.index(Config.DOWNLOADER_DEFAULT)
        available[index] = bold + '(' + available[index] + ')' + end
        formatted = '  |  '.join(available)
        return 'Downloaders available: ' + formatted


def check_connectivity():
    """
    Check for Internet connectivity (upon download error).
    """

    from urllib import request

    try:
        request.urlopen('http://www.google.com', timeout=5)
        return True
    except request.URLError:
        pass


@contextmanager
def devnull():
    """Temporarily redirect stdout and stderr to /dev/null."""

    try:
        original_stderr = os.dup(sys.stderr.fileno())
        original_stdout = os.dup(sys.stdout.fileno())
        null = open(os.devnull, 'w')
        os.dup2(null.fileno(), sys.stderr.fileno())
        os.dup2(null.fileno(), sys.stdout.fileno())
        yield

    finally:
        if original_stderr is not None:
            os.dup2(original_stderr, sys.stderr.fileno())
        if original_stdout is not None:
            os.dup2(original_stdout, sys.stdout.fileno())
        if null is not None:
            null.close()


def error(*args):
    """Display error message via stderr or GUI."""
    if sys.stdin.isatty():
        print('ERROR:', *args, file=sys.stderr)
    else:
        notify_error(*args)


def execute(*args):
    """Execute shell commands."""
    import subprocess

    subprocess.call(args, stdout=subprocess.DEVNULL)


def failure(path, downloader):
    """Display warning message via stderr or GUI."""
    base = os.path.basename(path)
    if sys.stdin.isatty():
        print('INFO [{}]: Failed to download {!r}'.format(downloader, base))
    else:
        notify_failure(base, downloader)


def fatal(*args):
    """Display error message via stderr or GUI before exiting."""
    error(*args)
    sys.exit(1)


def have(cmd):
    """Determine whether supplied argument is a command on the PATH."""

    try:
        # Python 3.3+ only
        from shutil import which
    except ImportError:
        def which(cmd):
            """
            Given a command, return the path which conforms to the given mode
            on the PATH, or None if there is no such file.
            """

            def _access_check(path):
                """
                Check that a given file can be accessed with the correct mode.
                Additionally check that `path` is not a directory.
                """
                return (os.path.exists(path) and os.access(
                    path, os.F_OK | os.X_OK) and not os.path.isdir(path))

            # If we're given a path with a directory part, look it up directly
            # rather than referring to PATH directories. This includes checking
            # relative to the current directory, e.g. ./script
            if os.path.dirname(cmd):
                if _access_check(cmd):
                    return cmd
                return None

            paths = os.environ.get('PATH', os.defpath.lstrip(':')).split(':')

            seen = set()
            for path in paths:
                if path not in seen:
                    seen.add(path)
                    name = os.path.join(path, cmd)
                    if _access_check(name):
                        return name
            return None

    return which(cmd) is not None


def main(args=None):
    """Start application."""

    dlx = Downloader()
    epilog = dlx.epilog()

    options, arguments = parse(args, epilog)

    # create list of video files that don't have accompanying 'srt' subtitles
    targets = [p for p in arguments if os.path.isfile(p) and not
               os.path.exists(os.path.splitext(p)[0] + '.srt')]

    if not targets:
        fatal('No valid targets were specified')

    if options.rename:
        videos = [rename(p) for p in targets]
    else:
        videos = targets

    dlx.download(videos, options.downloader, options.language)

    subtitles = []

    for video_path in videos:
        srt_path = os.path.splitext(video_path)[0] + '.srt'
        if os.path.isfile(srt_path):
            subtitles.append(srt_path)
        elif not options.quiet:
            failure(video_path, options.downloader)

    if options.scan and subtitles:
        scan(subtitles)


def multithreader(args, paths):
    """Execute multiple processes at once."""

    def shellprocess(path):
        """Return a ready-to-use subprocess."""
        import subprocess
        return subprocess.Popen(args + [path],
                                stderr=subprocess.DEVNULL,
                                stdout=subprocess.DEVNULL)

    processes = [shellprocess(path) for path in paths]

    for process in processes:
        process.wait()


def notify(title, message, icon):
    """Display a message."""
    execute('notify-send', '--icon=' + icon, title, message)


def notify_error(message):
    """Display an error message."""
    notify(__program__, 'ERROR: ' + message, 'edit-delete')


def notify_failure(path, downloader):
    """Display a failure notification."""
    notify('{} [{}]'.format(__program__, downloader),
           'Subtitles not downloaded successfully.\n' +
           path, 'edit-delete')


def notify_warning(message):
    """Display a warning message."""
    notify(__program__, 'WARNING: ' + message, 'emblem-important')


def parse(args, epilog):
    """
    Parse command-line arguments. Arguments may consist of any
    combination of directories, files, and options.
    """

    import argparse
    from locale import getlocale

    # set the default language
    default_language = getlocale()[0].split('_')[0].lower()

    parser = argparse.ArgumentParser(
        add_help=False,
        description=__description__,
        epilog=epilog,
        usage='%(prog)s [OPTIONS] FILES|FOLDERS')
    parser.add_argument(
        '-d', '--downloader',
        default=Config.DOWNLOADER_DEFAULT,
        dest='downloader',
        help='indicate downloader to use')
    parser.add_argument(
        '-l', '--language',
        default=default_language,
        dest='language',
        help='indicate language to use [{}]'.format(default_language))
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        dest='quiet',
        help='do not display failure notifications via notify-send')
    parser.add_argument(
        '-r', '--rename',
        action='store_true',
        dest='rename',
        help='prompt to rename video files')
    parser.add_argument(
        '-s', '--scan',
        action='store_true',
        dest='scan',
        help='remove advertising from subtitle files')
    parser.add_argument(
        '-h', '--help',
        action='help',
        help=argparse.SUPPRESS)
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s ' + __version__)
    parser.add_argument(
        action='append',
        dest='targets',
        help=argparse.SUPPRESS,
        nargs='*')

    options = parser.parse_args(args)
    arguments = options.targets[0]

    return options, arguments


def prompt(path):
    """Prompt for a new filename via terminal or GUI."""

    if sys.stdin.isatty():
        return prompt_terminal(path)
    else:
        return prompt_gui(path)


def prompt_gui(path):
    """Prompt for a new filename via GUI."""

    import subprocess

    filepath, extension = os.path.splitext(path)
    basename = os.path.basename(filepath)
    dirname = os.path.dirname(filepath)

    retry_text = 'Sorry, please try again...'
    icon = 'video-x-generic'

    # detect and configure dialog program
    if have('yad'):
        args = ['yad',
                '--borders=5',
                '--entry',
                '--entry-label=Filename:',
                '--entry-text=' + basename,
                '--title=Batch Tool',
                '--window-icon=' + icon]
        retry_args = args + ['--text=<b>' + retry_text + '</b>',
                             '--text-align=center']

    elif have('zenity'):
        base = ['zenity',
                '--entry',
                '--entry-text=' + basename,
                '--title=Batch Tool',
                '--window-icon=info']
        args = base + ['--text=Filename:']
        retry_args = base + ['--text=' + retry_text]

    else:
        fatal('Please install yad (or zenity)')

    # display filename prompt
    try:
        new_basename = subprocess.check_output(
            args, universal_newlines=True).strip()
    except subprocess.CalledProcessError:
        sys.exit(1)

    # retry prompt if new filename already exists
    while os.path.exists(os.path.join(dirname, new_basename + extension)) and \
            new_basename != basename:
        try:
            new_basename = subprocess.check_output(
                retry_args, universal_newlines=True).strip()
        except subprocess.CalledProcessError:
            sys.exit(1)

    if new_basename == '':
        new_basename = basename

    return os.path.join(dirname, new_basename + extension)


def prompt_terminal(path):
    """Prompt for a new filename via terminal."""

    def rlinput(prompt_msg, prefill=''):
        """
        One line is read from standard input. Display `prompt_msg` on
        standard error. `prefill` is placed into the editing buffer
        before editing begins.
        """
        import readline
        readline.set_startup_hook(lambda: readline.insert_text(prefill))
        try:
            return input(prompt_msg)
        finally:
            readline.set_startup_hook()

    filepath, extension = os.path.splitext(path)
    basename = os.path.basename(filepath)
    dirname = os.path.dirname(filepath)

    # display filename prompt
    new_basename = rlinput('Filename: ', basename)

    # retry prompt if new filename already exists
    while os.path.exists(os.path.join(dirname, new_basename + extension)) and \
            new_basename != basename:
        new_basename = rlinput('Sorry, please try again... Filename: ',
                               basename)

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

    from distutils.version import StrictVersion
    from importlib.util import find_spec

    try:
        import subnuker
    except ImportError:
        fatal('Unable to scan subtitles. Please install subnuker.')

    # check whether aeidon is available
    aeidon = find_spec('aeidon') is not None

    if sys.stdin.isatty():
        # launch subnuker from the existing terminal
        args = (['--aeidon'] if aeidon else []) + \
               ['--gui', '--regex'] + subtitles
        subnuker.main(args)
    else:
        # launch subnuker from a new terminal
        args = (['--aeidon'] if aeidon else []) + \
               ['--gui', '--regex']
        execute(Config.TERMINAL,
                '--execute',
                'subnuker',
                *args + subtitles)


def warning(*args):
    """Display warning message via stderr or GUI."""
    if sys.stdin.isatty():
        print('WARNING:', *args, file=sys.stderr)
    else:
        notify_warning(*args)


if __name__ == '__main__':
    main()
