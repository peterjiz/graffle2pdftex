Graffle To PDF_Tex
=======================

A command line tool that exports OmniGraffle figures to PDF_Tex

Installation
------------

In order to have it successfully installed and working, following is required:

-   [OmniGraffle](http://www.omnigroup.com/mailman/archive/omnigraffle-users/2008/004785.html) 7.21
-   python \>= 3.9
-   [appscript](http://appscript.sourceforge.net/py-appscript/index.html) \>= 0.22
-   PyMuPDF

You can either clone the repository and install using 

    pip install .

Or install straight from the PIP repository:

    pip install graffle2pdftex

Usage
-----

    Usage: graffle2pdftex [options] <source>

    Options:
      -h, --help  show this help message and exit
      --debug     print out debug messages

Exports the figure/canvases to a new folder of the same name as the input file in the source file's parent directory

Examples
--------

-   Export *all* canvases into PDF_Tex files

    ```
    $ graffle2pdftex figure.graffle
    ```

Making a release
----------------

- update the version number in `setup.py`
- commit
- push
- register release `$ python setup.py register`
- upload release `$ python setup.py bdist upload`

Developing graffle2pdftex
-----------------------------

- clone
- stage `$ python setup.py develop`
- make a new feature branch
- code
- do release
- unstage `$python setup.py develop --uninstall`
