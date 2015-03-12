About
=====

This script is intended to be a one-stop-shop for batch preparing freshly downloaded video files for use with subtitles.

The tool can be used from the command-line but is ideal for use via GUI file managers (i.e. Thunar Custom Actions). With a single click of several video files: prompt to rename files, download the best subtitle file available (displaying a popup notification upon failure), then open a terminal window to scan and remove advertising (via subnuker).


Installation
============

::

  pip3 install --user subsystem

The ``subsystem`` package is known to be compatible with Python 3.


Requirements
============

NOTE: The most recent version of ``subsystem`` includes a bundled copy of the yad v0.28.0 binary. It is tentatively included at this time purely out of convenience.

yad or zenity is required if you'd like to make use of the GUI renamer.

yad is highly recommended over zenity and is available via tarball (at its homepage_) or webupd8team PPA (Launchpad_):

::

    sudo apt-add-repository ppa:webupd8team/y-ppa-manager
    sudo apt-get update && sudo apt-get install yad

In order to make use of subsystem, you need have external downloaders installed. I recommend the Python 3 compatible download tool ``ss``. In my limited experience is has been the fastest and most reliable tool available.

::

  pip3 install --user ss

subsystem is also compatible with ``periscope`` and ``subscope`` (NOTE: these scripts appear to be Python 2 ONLY)

::

  pip2 install --user periscope

::

  pip2 install --user subscope


Usage
=====

From the command line, run ``subsystem --help`` to display options and downloaders available. Subsystem will use ``ss`` by default if possible, but will use whatever is available.

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
