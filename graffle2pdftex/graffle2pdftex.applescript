set delayMultiplier to 1
tell application "System Events"
	set omnigraffleIsOpen to ((bundle identifier of processes) contains "com.omnigroup.OmniGraffle7")
end tell

set omnigraffleDelay to 1
if omnigraffleIsOpen is false then
	set omnigraffleDelay to 0
end if

set launchdelay to omnigraffleDelay

tell application "OmniGraffle"
	activate
end tell
delay launchdelay

--set destinationPath to POSIX path of alias ((path to home folder as text) & "OmniGraffle:PDF_Tex")
tell application "System Events" to set frontmost of process "OmniGraffle" to true
tell application "System Events" to click UI element "OmniGraffle" of list 1 of application process "Dock"

delay launchdelay * delayMultiplier

set OGCanvases to []
set canvas_export_folders to []
tell application "OmniGraffle"
	set _document to front document
	set originalFilepath to path of _document
	set _path to my removeExtension(originalFilepath)
	set basefolder to my removeLastPathComponent(originalFilepath)
	set filename to my getLastPathComponent(_path)
	set destinationPath to _path
	tell front document
		set myCanvases to (every canvas as list)
		repeat with i from 1 to (length of (myCanvases as list))
			set theName to (name of item i of myCanvases) as text
			set canvasExportPath to _path & "/" & filename & "_" & theName
			set OGCanvases to OGCanvases & theName
			set canvas_export_folders to canvas_export_folders & canvasExportPath
		end repeat
		--close
	end tell
end tell

(*
do shell script "mkdir -p " & quoted form of _path
set destinationDir to basefolder & "/tmp/"
set destinationFilepath to destinationDir & filename & ".graffle"

do shell script "mkdir -p " & quoted form of destinationDir & " && cp -rf " & quoted form of originalFilepath & " " & quoted form of destinationFilepath
set theOPMLFilePosix to POSIX file destinationFilepath

-- https://www.macscripter.net/t/converting-from-alias-to-path-path-to-alias/49846/2
tell application "OmniGraffle"
	--do shell script "open -n " & quoted form of POSIX path of theOPMLFilePosix & " & "
	--log theOPMLFilePosix as alias as Unicode text
	set convertedDocument to open theOPMLFilePosix
	repeat until exists front document
		delay 0.1
	end repeat
	set _document to front document
	set _path to my removeExtension(path of _document)
	set filename to my getLastPathComponent(_path)
	tell front document
	end tell
end tell
*)

set destinationFilepath to originalFilepath
set theOPMLFilePosix to POSIX file destinationFilepath

tell application "System Events"
	tell application process "OmniGraffle"
		
		repeat with i from 1 to (length of OGCanvases)
			set canvas to item i of OGCanvases
			--set outputPDFPath to destinationPath & "/" & filename & "_" & canvas & "/" & filename & "_" & canvas & ".pdf"
			
			click menu item canvas of menu 1 of menu item "Display Canvas" of menu 1 of menu bar item "View" of menu bar 1
			click menu item "Export to Pdf_Tex" of menu 1 of menu bar item "Automation" of menu bar 1
			
			repeat until exists sheet 1 of window 1
				delay 0.1
			end repeat
			tell sheet 1 of window 1
				keystroke "g" using {command down, shift down}
				repeat until exists sheet 1
					delay 0.1
				end repeat
				tell sheet 1
					keystroke destinationPath
					keystroke return
				end tell
				try
					repeat while exists sheet 1
						delay 0.1
					end repeat
				end try
				click UI element "Save"
				try
					click UI element "Replace" of sheet 1
				on error errorMessage
				end try
			end tell
			
			--log outputPDFPath
			--repeat until my fileExists(outputPDFPath)
			--	delay 0.1 -- wait for 0.1 second
			--end repeat
			
			
		end repeat
		
	end tell
end tell

-- https://www.macscripter.net/t/converting-from-alias-to-path-path-to-alias/49846/2
tell application "OmniGraffle"
	tell front document
		close
	end tell
end tell

do shell script "rm -rf " & quoted form of destinationDir
repeat with i from 1 to (length of (canvas_export_folders as list))
	set canvasExportFolder to item i of canvas_export_folders
	do shell script "cp -f " & quoted form of canvasExportFolder & "/*" & " " & quoted form of destinationPath & " && rm -rf " & quoted form of canvasExportFolder
end repeat

on removeExtension(theString)
	set lastPeriod to 0
	set n to count of characters of theString
	repeat with i from 1 to n
		if character i of theString is "." then
			set lastPeriod to i
		end if
	end repeat
	
	if lastPeriod is not 0 then
		set theString to characters 1 thru (lastPeriod - 1) of theString
		set theString to theString as text
	else
		--there isn't an extension
	end if
	
	return theString
end removeExtension

on getLastPathComponent(thePath)
	set tid to AppleScript's text item delimiters
	set AppleScript's text item delimiters to "/"
	set pathComponents to text items of thePath
	set AppleScript's text item delimiters to tid
	return last item of pathComponents
end getLastPathComponent


on removeLastPathComponent(thePath)
	set tid to AppleScript's text item delimiters
	set AppleScript's text item delimiters to "/"
	set pathComponents to text items of thePath
	set countOfComponents to count of pathComponents
	if countOfComponents > 1 then
		set newPath to text items 1 thru (countOfComponents - 1) of pathComponents as text
	else
		set newPath to ""
	end if
	set AppleScript's text item delimiters to tid
	return newPath
end removeLastPathComponent


on fileExists(filePath)
	try
		set fileRef to filePath as alias
		return true
	on error
		return false
	end try
end fileExists