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

from graffle2pdftex.omnigraffle import OmniGraffle

# graffle2pdftex_applescript = """
# set delayMultiplier to 1
# tell application "System Events"
# 	set omnigraffleIsOpen to ((bundle identifier of processes) contains "com.omnigroup.OmniGraffle7")
# end tell
#
# set omnigraffleDelay to 1
# if omnigraffleIsOpen is false then
# 	set omnigraffleDelay to 0
# end if
#
# set launchdelay to omnigraffleDelay
#
# tell application "OmniGraffle"
# 	activate
# end tell
# delay launchdelay
#
# --set destinationPath to POSIX path of alias ((path to home folder as text) & "OmniGraffle:PDF_Tex")
# tell application "System Events" to set frontmost of process "OmniGraffle" to true
# tell application "System Events" to click UI element "OmniGraffle" of list 1 of application process "Dock"
#
# delay launchdelay * delayMultiplier
#
# set OGCanvases to []
# set canvas_export_folders to []
# tell application "OmniGraffle"
# 	set _document to front document
# 	set originalFilepath to path of _document
# 	set _path to my removeExtension(originalFilepath)
# 	set basefolder to my removeLastPathComponent(originalFilepath)
# 	set filename to my getLastPathComponent(_path)
# 	set destinationPath to _path
# 	tell front document
# 		set myCanvases to (every canvas as list)
# 		repeat with i from 1 to (length of (myCanvases as list))
# 			set theName to (name of item i of myCanvases) as text
# 			set canvasExportPath to _path & "/" & filename & "_" & theName
# 			set OGCanvases to OGCanvases & theName
# 			set canvas_export_folders to canvas_export_folders & canvasExportPath
# 		end repeat
# 		--close
# 	end tell
# end tell
#
# (*
# do shell script "mkdir -p " & quoted form of _path
# set destinationDir to basefolder & "/tmp/"
# set destinationFilepath to destinationDir & filename & ".graffle"
#
# do shell script "mkdir -p " & quoted form of destinationDir & " && cp -rf " & quoted form of originalFilepath & " " & quoted form of destinationFilepath
# set theOPMLFilePosix to POSIX file destinationFilepath
#
# -- https://www.macscripter.net/t/converting-from-alias-to-path-path-to-alias/49846/2
# tell application "OmniGraffle"
# 	--do shell script "open -n " & quoted form of POSIX path of theOPMLFilePosix & " & "
# 	--log theOPMLFilePosix as alias as Unicode text
# 	set convertedDocument to open theOPMLFilePosix
# 	repeat until exists front document
# 		delay 0.1
# 	end repeat
# 	set _document to front document
# 	set _path to my removeExtension(path of _document)
# 	set filename to my getLastPathComponent(_path)
# 	tell front document
# 	end tell
# end tell
# *)
#
# set destinationFilepath to originalFilepath
# set theOPMLFilePosix to POSIX file destinationFilepath
#
# tell application "System Events"
# 	tell application process "OmniGraffle"
#
# 		repeat with i from 1 to (length of OGCanvases)
# 			set canvas to item i of OGCanvases
# 			--set outputPDFPath to destinationPath & "/" & filename & "_" & canvas & "/" & filename & "_" & canvas & ".pdf"
#
# 			click menu item canvas of menu 1 of menu item "Display Canvas" of menu 1 of menu bar item "View" of menu bar 1
# 			click menu item "Export to Pdf_Tex" of menu 1 of menu bar item "Automation" of menu bar 1
#
# 			repeat until exists sheet 1 of window 1
# 				delay 0.1
# 			end repeat
# 			tell sheet 1 of window 1
# 				keystroke "g" using {command down, shift down}
# 				repeat until exists sheet 1
# 					delay 0.1
# 				end repeat
# 				tell sheet 1
# 					keystroke destinationPath
# 					keystroke return
# 				end tell
# 				try
# 					repeat while exists sheet 1
# 						delay 0.1
# 					end repeat
# 				end try
# 				click UI element "Save"
# 				try
# 					click UI element "Replace" of sheet 1
# 				on error errorMessage
# 				end try
# 			end tell
#
# 			--log outputPDFPath
# 			--repeat until my fileExists(outputPDFPath)
# 			--	delay 0.1 -- wait for 0.1 second
# 			--end repeat
#
#
# 		end repeat
#
# 	end tell
# end tell
#
# -- https://www.macscripter.net/t/converting-from-alias-to-path-path-to-alias/49846/2
# tell application "OmniGraffle"
# 	tell front document
# 		close
# 	end tell
# end tell
#
# do shell script "rm -rf " & quoted form of destinationDir
# repeat with i from 1 to (length of (canvas_export_folders as list))
# 	set canvasExportFolder to item i of canvas_export_folders
# 	do shell script "cp -f " & quoted form of canvasExportFolder & "/*" & " " & quoted form of destinationPath & " && rm -rf " & quoted form of canvasExportFolder
# end repeat
#
# on removeExtension(theString)
# 	set lastPeriod to 0
# 	set n to count of characters of theString
# 	repeat with i from 1 to n
# 		if character i of theString is "." then
# 			set lastPeriod to i
# 		end if
# 	end repeat
#
# 	if lastPeriod is not 0 then
# 		set theString to characters 1 thru (lastPeriod - 1) of theString
# 		set theString to theString as text
# 	else
# 		--there isn't an extension
# 	end if
#
# 	return theString
# end removeExtension
#
# on getLastPathComponent(thePath)
# 	set tid to AppleScript's text item delimiters
# 	set AppleScript's text item delimiters to "/"
# 	set pathComponents to text items of thePath
# 	set AppleScript's text item delimiters to tid
# 	return last item of pathComponents
# end getLastPathComponent
#
#
# on removeLastPathComponent(thePath)
# 	set tid to AppleScript's text item delimiters
# 	set AppleScript's text item delimiters to "/"
# 	set pathComponents to text items of thePath
# 	set countOfComponents to count of pathComponents
# 	if countOfComponents > 1 then
# 		set newPath to text items 1 thru (countOfComponents - 1) of pathComponents as text
# 	else
# 		set newPath to ""
# 	end if
# 	set AppleScript's text item delimiters to tid
# 	return newPath
# end removeLastPathComponent
#
#
# on fileExists(filePath)
# 	try
# 		set fileRef to filePath as alias
# 		return true
# 	on error
# 		return false
# 	end try
# end fileExists
# """


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
        ogscriptPath = pathlib.Path(__file__).resolve().parent / "graffle2pdftex.applescript"
        osascript.osascript(str(ogscriptPath))
        # osascript.osascript(graffle2pdftex_applescript)

        # for file in tmpGrafflePath.rglob('*.pdf*'):
        #     shutil.copy(str(file), str(destination))

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
