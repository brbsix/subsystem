#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Interfaces to external download tools."""


def periscope(paths, language):
    """
    Download subtitles for multiple video files via periscope.

    NOTE: Execute periscope via shell because it only supports Python 2
    """

    from subsystem.subsystem import multithreader

    multithreader(['periscope', '-l', language, '--quiet'], paths)


def ss(paths):  # pylint: disable=invalid-name
    """Download subtitles for multiple video files via periscope."""

    from ss import main
    from subsystem.subsystem import devnull

    with devnull():
        # main will strip arg[0]
        main(['ss'] + paths)


def subscope(paths, language):
    """
    Download subtitles for multiple video files via subscope script.

    NOTE: Runs subscope via shell to support Python 2 version of subscope
          (and the Python 3 version has issues)
    """

    from subsystem.subsystem import multithreader

    multithreader(['subscope', '-l', language], paths)


# def subscope(paths, language):
#     """
#     Download subtitles for multiple video files via subscope module.

#     NOTE: The Python 3 version of subscope has issues
#     """

#     from subscope.core import DownloadFirstHandler, Subscope

#     handler = DownloadFirstHandler(Subscope())

#     try:
#         with devnull():
#             handler.run(paths, [language])
#     except KeyboardInterrupt:
#         sys.exit(1)
