on run argv
-- the 'argv' list contains the arguments passed to the script
  set shouldClone to true
  try
    set shouldClone to item 1 of argv
  on error errMsg
  end try

  log shouldClone
  my activateOmnigraffle()
  set docInfo to my getFrontdocumentInfo()
  set originalDocument to item 1 of docInfo
  set originalFilepath to item 2 of docInfo
  set destinationFilepath to item 3 of docInfo
  set OGCanvases to item 4 of docInfo
  set canvas_export_folders to item 5 of docInfo

  if shouldClone is true then
    my cloneOmnigraffleDocument(originalFilepath)
    set _path to my removeExtension(originalFilepath)
    do shell script "mkdir -p " & quoted form of _path
    set clonedDocInfo to my getFrontdocumentInfo()
    set clonedDocument to item 1 of clonedDocInfo
  end if

  my exportCanvases(OGCanvases, destinationFilepath)
  my moveExportedCanvases(canvas_export_folders, destinationFilepath)

  if shouldClone is true
    my closeOmnigraffleDocument(clonedDocument)
  else
    my closeOmnigraffleDocument(originalDocument)
  end if
end run

on activateOmnigraffle()
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

end activateOmnigraffle

on getFrontdocumentInfo()
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
    set myCanvasesLength to (length of (myCanvases as list))
    repeat with i from 1 to myCanvasesLength
      set theName to (name of item i of myCanvases) as text
      set canvasExportPath to _path & "/" & filename
      if myCanvasesLength > 1 then
        set canvasExportPath to canvasExportPath & "_" & theName
      end if
      set OGCanvases to OGCanvases & theName
      set canvas_export_folders to canvas_export_folders & canvasExportPath
    end repeat
    --close
  end tell
end tell

return {_document, originalFilepath, destinationPath, OGCanvases, canvas_export_folders}
end getFrontdocumentInfo

on cloneOmnigraffleDocument(originalFilepath)
  set filename to my getLastPathComponent(originalFilepath)
  set filenameWithoutExtension to my removeExtension(filename)
  set basefolder to my removeLastPathComponent(originalFilepath)
  set destinationDir to basefolder & "/tmp/"
  set destinationFilepath to destinationDir & filename

  do shell script "mkdir -p " & quoted form of destinationDir & " && cp -rf " & quoted form of originalFilepath & " " & quoted form of destinationFilepath
  set destinationFilePosix to POSIX file destinationFilepath

  tell application "OmniGraffle"
    set convertedDocument to open destinationFilePosix
    repeat until exists front document
      delay 0.1
    end repeat
    --set _document to front document
    --set _path to my removeExtension(path of _document)
    --set filename to my getLastPathComponent(_path)
    --tell front document
    --end tell
  end tell

end cloneOmnigraffleDocument

on exportCanvases(OGCanvases, destinationPath)
  do shell script "mkdir -p " & quoted form of destinationPath

  tell application "System Events"
    tell application process "OmniGraffle"

      repeat with i from 1 to (length of OGCanvases)
        set canvas to item i of OGCanvases

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
      end repeat
    end tell
  end tell
end exportCanvases

on moveExportedCanvases(canvas_export_folders, destinationDir)
--do shell script "rm -rf " & quoted form of destinationDir
  repeat with i from 1 to (length of (canvas_export_folders as list))
    set canvasExportFolder to item i of canvas_export_folders
    do shell script "cp -f " & quoted form of canvasExportFolder & "/*" & " " & quoted form of destinationDir & " && rm -rf " & quoted form of canvasExportFolder
  end repeat
end moveExportedCanvases

on closeOmnigraffleDocument(thedocument)
  tell application "OmniGraffle"
    tell thedocument
      close
    end tell
  end tell
end closeOmnigraffleDocument

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