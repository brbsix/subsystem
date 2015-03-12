About
=====

This script is intended to be a one-stop-shop for batch preparing freshly downloaded video files for use with subtitles.

The tool can be used from the command-line but is ideal for use via GUI file managers (i.e. Thunar Custom Actions). With a single click of several video files: prompt to rename files, download the best subtitle file available (displaying a popup notification upon failure), then open a terminal window to scan and remove advertising (via subnuker_).

If you are used to downloading subtitles with other tools, you are in for a surprise. Not only does it pack a wicked set of features, but it makes full use your processor to download subtitles in parallel... superfast.


Installation
============

::

  pip3 install --user subsystem

The ``subsystem`` package is known to be compatible with Python 3.


Requirements
============

*NOTE: The most recent version of subsystem is bundled with yad 0.28.0. It is tentatively included at this time purely out of convenience.*

A GTK dialog tool (yad or zenity) is required if you'd like to make use of the GUI renamer.

yad is available via tarball (at its homepage_) or webupd8team PPA (Launchpad_):

::

    sudo apt-add-repository ppa:webupd8team/y-ppa-manager
    sudo apt-get update && sudo apt-get install yad

In order to make use of ``subsystem``, you'll need to install a downloader. I recommend the Python 3 compatible ``ss``. In my limited experience is the fastest and most reliable tool available.

::

  pip3 install --user ss

``subsystem`` is also compatible with the Python 2 scripts ``periscope`` and ``subscope``

::

  pip2 install --user periscope

::

  pip2 install --user subscope


Usage
=====

From the command line, run ``subsystem --help`` to display available options and downloaders. ``subsystem11 will use ``ss`` by default if possible, but will detect and use whatever is available.

To download subtitles for files:

::

    subsystem FILES

To use an alternate downloader:

::

    subsystem -d DOWNLOADER FILES

To rename video files then scan upon download completion:

::

    subsystem --rename --scan FILES

To silence popup notications upon failure:

::

    subsystem --quiet FILES


License
=======

Copyright (c) 2015 Six (brbsix@gmail.com).

Licensed under the GPLv3 license.

.. _homepage: http://sourceforge.net/projects/yad-dialog/
.. _Launchpad: https://launchpad.net/~webupd8team/+archive/ubuntu/y-ppa-manager
:: _subnuker: https://github.com/brbsix/subnuker
