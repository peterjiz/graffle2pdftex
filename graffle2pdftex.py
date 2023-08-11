#!/usr/bin/env python

import logging
import optparse
import os
import pathlib
import re
import shutil
import sys
import tempfile

import fitz
import osascript
import pdfrw

from omnigraffle import OmniGraffle

#
# def remove_text_from_pdf(input_pdf_path, output_pdf_path):
#     # Open the PDF file
#     document = fitz.open(input_pdf_path)
#
#     # Iterate through the pages
#     for page_number in range(len(document)):
#         page = document.load_page(page_number)
#
#         # Get the blocks on the page, where blocks contain various elements like text and images
#         blocks = page.get_text("blocks")
#
#         # Iterate through the blocks and remove the text blocks
#         for block in blocks:
#             x0, y0, x1, y1, _, _, _ = block[:7]
#             rectangle = fitz.Rect(x0, y0, x1, y1)
#             page.add_redact_annot(rectangle) # Mark the text for redaction
#
#         # Apply redaction, effectively removing the text
#         page.apply_redactions()
#
#     # Save the PDF with the text removed
#     document.save(output_pdf_path)
#
# # def create_new_pdf_without_text(input_pdf_path, output_pdf_path):
# #     # Open the input PDF
# #     document = fitz.open(input_pdf_path)
# #     # Create a new PDF to hold the non-text content
# #     new_document = fitz.open()
# #
# #     # Iterate through each page of the input PDF
# #     for page_number in range(len(document)):
# #         page = document.load_page(page_number)
# #         # Create a new page with the same dimensions as the original
# #         new_page = new_document.new_page(width=page.rect.width, height=page.rect.height)
# #
# #         # Iterate through the page's display list (this includes text, images, etc.)
# #         for item in page.get_displaylist().items():
# #             # If the item's type is text, skip it
# #             if item[0] == 1:
# #                 continue
# #             # Otherwise, add the item to the new page
# #             new_page.insert_image(rect=item[-2], stream=item[-1])
# #
# #     # Save the new PDF (without text) to the output path
# #     new_document.save(output_pdf_path)


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

# def test(input_pdf_path, output_pdf_path):
#     # Read the PDF
#     pdf = pdfrw.PdfReader(input_pdf_path)
#
#     # Iterate through the PDF's pages
#     for page in pdf.pages:
#         # Find all text objects
#         text_objects = pdfrw.find_objects(page, "/Type", "/Font")
#         for obj in text_objects:
#             # Replace text content with an empty string
#             obj.stream = ""
#
#     # Write the modified PDF
#     pdfrw.PdfWriter().write(output_pdf_path, pdf)

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
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
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
    with tempfile.TemporaryDirectory() as temp_dir:
        tmpFilepath = pathlib.Path(temp_dir) / filepath.name
        tmpGrafflePath = pathlib.Path(temp_dir) / filepath.stem
        tmpGrafflePath.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(str(filepath), str(tmpFilepath))
        og = OmniGraffle()
        schema = og.open(str(tmpFilepath))
        ogscriptPath = "graffle2pdftex.applescript"
        osascript.osascript(str(ogscriptPath))

        # for file in tmpGrafflePath.rglob('*.pdf*'):
        #     shutil.copy(str(file), str(destination))

        for file in tmpGrafflePath.rglob('*.pdf'):
            # shutil.copy(str(file), str(destination))
            # remove_text_from_pdf(str(file), str(destination / file.name))
            # test(str(file), str(destination / file.name))
            # create_new_pdf_without_text(str(file), str(destination / file.name))
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
