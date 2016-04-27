# -*- coding: utf-8 -*-
"""Interfaces to external download tools."""

from .subsystem import devnull, multithreader


def periscope(paths, language):
    """
    Download subtitles for multiple video files via periscope.

    NOTE: Execute periscope via shell because it only supports Python 2
    """

    multithreader(['periscope', '-l', language, '--quiet'], paths)


def ss(paths):  # pylint: disable=invalid-name
    """Download subtitles for multiple video files via periscope."""

    from ss import main

    with devnull():
        # main will strip arg[0]
        main(['ss'] + paths)


def subscope(paths, language):
    """
    Download subtitles for multiple video files via subscope script.

    NOTE: Runs subscope via shell to support Python 2 version of subscope
          (and the Python 3 version has issues)
    """

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
