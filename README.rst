subsystem
---------

.. image:: https://img.shields.io/pypi/v/subsystem.svg
  :target: https://pypi.python.org/pypi/subsystem

.. image:: https://img.shields.io/pypi/l/subsystem.svg
  :target: https://pypi.python.org/pypi/subsystem

.. image:: https://img.shields.io/pypi/dm/subsystem.svg
  :target: https://pypi.python.org/pypi/subsystem

This script is intended to be a one-stop-shop for batch preparing freshly downloaded video files for use with subtitles.

The tool can be used from the command-line but is ideal for use via GUI file managers (i.e. Thunar Custom Actions or Nautilus actions.). With a single click of several video files: prompt to rename files, download the best subtitle file available (displaying a popup notification upon failure), then open a terminal window to scan and remove advertising (via subnuker_).

If you have some experience downloading subtitles with other tools, you are in for a pleasant surprise. Not only does it pack a wicked set of features, but it makes full use your processor to download subtitles in parallel... superfast.


Installation
============

``subsystem`` is compatible with Python 3. To install to the Python user install directory for your platform, typically ``$HOME/.local/``:

::

  pip3 install --user subsystem

If installing with the ``--user`` flag, ensure that ``$HOME/.local/bin`` is on your PATH.


Requirements
============

A GTK dialog tool (yad or zenity) is required if you'd like to make use of the GUI renamer.

yad is the recommmended tool. It is available via tarball (at it's homepage_) or webupd8team PPA (Launchpad_):

::

    sudo apt-add-repository ppa:nilarimogard/webupd8
    sudo apt-get update && sudo apt-get install yad

In order to make use of ``subsystem``, you'll need to install a downloader. I recommend the Python 3 compatible ``ss``. In my experience it is the fastest and most reliable tool available.

::

  pip3 install --user ss

``subsystem`` is also compatible with the Python 2 scripts ``periscope`` and ``subscope``

::

  pip2 install --user periscope

::

  pip2 install --user subscope


Usage
=====

From the command line, run ``subsystem --help`` to display available options and downloaders. ``subsystem`` will use ``ss`` by default if possible, otherwise it will detect and use whatever is available.

To download subtitles for files:

::

    subsystem FILE...

To use an alternate downloader:

::

    subsystem -d DOWNLOADER FILE...

To rename video files prior to download of subtitles:

::

    subsystem --rename FILE...

To scan subtitles files with ``subnuker`` upon download completion:

::

    subsystem --scan FILE...

Executing subsystem with the ``--scan`` option from a GUI will open ``subnuker`` in a terminal window. It is configured to use ``xfce4-terminal``. Let me know if you'd like to support another terminal and I'll add the feature.

To silence ``notify-send`` notications upon failure:

::

    subsystem --quiet FILE...

*Note: Multiple command line options may be used concurrently*


License
=======

Copyright (c) 2015 Six (brbsix@gmail.com).

Licensed under the GPLv3 license.

.. _homepage: http://sourceforge.net/projects/yad-dialog/
.. _Launchpad: https://launchpad.net/~nilarimogard/+archive/ubuntu/webupd8
.. _subnuker: https://github.com/brbsix/subnuker
