#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Interfaces to external download tools."""


def periscope(paths, language):
    """
    Download subtitles for multiple video files via periscope.
    NOTE: currently supporting periscope via the shell because it is Py2 only"""

    from subsystem.subsystem import multithreader

    multithreader(['periscope', '-l', language, '--quiet'], paths)

def ss(paths):  # pylint: disable=C0103
    """Download subtitles for multiple video files via periscope."""

    from ss import main
    from subsystem.subsystem import devnull

    with devnull():
        # main will strip arg[0]
        main(['ss'] + paths)

def subscope(paths, language):
    """
    Download subtitles for multiple video files via subscope script.
    NOTE: currently supporting Py2 version of subscope via the shell (Py3 version has issues)
    """

    from subsystem.subsystem import multithreader

    multithreader(['subscope', '-l', language], paths)

# def subscope(paths, language):
#     """
#     Download subtitles for multiple video files via subscope module.
#     NOTE: subscope module is buggy in py3
#     """

#     from subscope.core import DownloadFirstHandler, Subscope

#     handler = DownloadFirstHandler(Subscope())

#     try:
#         with devnull():
#             handler.run(paths, [language])
#     except KeyboardInterrupt:
#         sys.exit(1)
