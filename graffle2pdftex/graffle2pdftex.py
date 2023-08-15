#!/usr/bin/env python

import logging
import optparse
import os
import pathlib
import re
import shutil
import sys
import tempfile as tf

import fitz
import runcmd

# from graffle2pdftex.omnigraffle import OmniGraffle
from omnigraffle import OmniGraffle

def tempfile():
    """create temp file and return path"""
    f, path = tf.mkstemp()
    os.close(f)
    return path

def osascript_run(applescript, argv=None, background=False):
    """run applescript file/code with arguments."""

    # Check if provided applescript is a path or inline code
    if os.path.exists(applescript):
        path = applescript
    else:
        # Use a temporary file if provided applescript is inline code
        path = tempfile()
        open(path, "w").write(applescript)

    # Build the command
    cmd = ["osascript", path]

    # Add arguments if provided
    if argv:
        for arg in argv:
            cmd.append(str(arg))

    r = runcmd.run(cmd, background=background)
    return r.code, r.out, r.err

def redact_text_from_pdf(input_pdf_path, output_pdf_path):
    document = fitz.open(input_pdf_path)

    for page_number in range(len(document)):
        page = document.load_page(page_number)

        # Extract the text and its details
        text_instances = page.get_text("dict")["blocks"]

        # Iterate through the text instances and replace with whitespaces
        for instance in text_instances:
            if hasattr(instance, "lines") or "lines" in instance:
                for line in instance["lines"]:
                    for span in line["spans"]:
                        text = span["text"]
                        # Calculate the number of whitespaces needed
                        # white_spaces = ' ' * len(text)
                        # Get the position of the text
                        rect = fitz.Rect(span["bbox"])
                        # Add a white space to replace the original text
                        # page.add_freetext(rect, white_spaces, fontsize=span["size"], color=(1, 1, 1))
                        page.add_redact_annot(rect)  # Mark the text for redaction

        # Apply redaction, effectively removing the text
        page.apply_redactions()


    document.save(output_pdf_path)

# https://stackoverflow.com/questions/4427542/how-to-do-sed-like-text-replace-with-python
def sed_inplace(filename, pattern, repl):
    '''
    Perform the pure-Python equivalent of in-place `sed` substitution: e.g.,
    `sed -i -e 's/'${pattern}'/'${repl}' "${filename}"`.
    '''
    # For efficiency, precompile the passed regular expression.
    pattern_compiled = re.compile(pattern)

    # For portability, NamedTemporaryFile() defaults to mode "w+b" (i.e., binary
    # writing with updating). This is usually a good thing. In this case,
    # however, binary writing imposes non-trivial encoding constraints trivially
    # resolved by switching to text writing. Let's do that.
    with tf.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        with open(filename) as src_file:
            for line in src_file:
                tmp_file.write(pattern_compiled.sub(repl, line))

    # Overwrite the original file with the munged temporary file in a
    # manner preserving file attributes (e.g., permissions).
    shutil.copystat(filename, tmp_file.name)
    shutil.move(tmp_file.name, filename)


# https://github.com/fikovnik/omnigraffle-export
def export(source, debug=False):
    # logging
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    # check source
    if not os.access(source, os.R_OK):
        print("File: %s could not be opened for reading" % source, file=sys.stderr)
        sys.exit(1)

    filepath = pathlib.Path(source)
    destination = filepath.parent / filepath.stem
    destination.mkdir(parents=True, exist_ok=True)
    with tf.TemporaryDirectory() as temp_dir:
        tmpFilepath = pathlib.Path(temp_dir) / filepath.name
        tmpGrafflePath = pathlib.Path(temp_dir) / filepath.stem
        tmpGrafflePath.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(str(filepath), str(tmpFilepath))
        og = OmniGraffle()
        schema = og.open(str(tmpFilepath))
        ogscriptPath = pathlib.Path(__file__).resolve().parent / "graffle2pdftex.applescript"
        code, out, err = osascript_run(str(ogscriptPath), ["false"])

        for file in tmpGrafflePath.rglob('*.pdf'):
            redact_text_from_pdf(str(file), str(destination / file.name))

        for file in tmpGrafflePath.rglob('*.pdf_tex*'):
            shutil.copy(str(file), str(destination))


def main():
    usage = "Usage: %prog [options] <source> <target>"
    parser = optparse.OptionParser(usage=usage)

    parser.add_option('--debug', action='store_true', help='debug', dest='debug')
    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.print_help()
        sys.exit(1)
    (source,) = args

    export(source, options.debug)

if __name__ == '__main__':
    main()
