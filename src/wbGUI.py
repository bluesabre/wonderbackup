# ---------------------------------------------------------------------------- #
# Wonder Backup - http://wonderbackup.sourceforge.net/
# wbGUI.py
#
# Contains the functions for the graphical user interface.
#
# Modified by Sean Davis on November 28, 2010
# ---------------------------------------------------------------------------- #

import wx

from wbBackup import *
from wbFile import *
from wbOS import *
from wbXML import *

        
### --- Backup Progress Notebook Tabs -------------------------------------- ###
        
# ------ 1. Welcome Tab ------------------------------------------------------ #
class Tab_Welcome(wx.Panel):
    """Tab_Welcome( parent )

    This is the first tab the user encounters.  It displays a welcome message and
    has a button that shows the Release Notes."""
    def __init__(self, parent, messages):
        wx.Panel.__init__(self, parent=parent)

        png = wx.Image('Icon.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        image = wx.StaticBitmap(self, -1, png, (10, 5), (png.GetWidth(), png.GetHeight()))

        info = wx.StaticText(self, -1, messages['welcome']['welcome'], style=wx.ALIGN_LEFT)
        self.extra = {}

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(image, 0.5, wx.ALL, 10)
        self.sizer.Add(info, 0.5, wx.ALL, 10)
        self.SetSizer(self.sizer)
# ---------------------------------------------------------------------------- #
            

# ------ 2. Select Backup Type Tab ------------------------------------------- #
class Tab_SelectBackupType(wx.Panel):
    """Tab_SelectBackupType( parent, list messages)

    The Select Backup Type Tab.  This tab prompts the user for the type of backup
    they wish to do.  Options are 'local', 'external', and 'preconfigured'.

    To disable any of these options, simply comment out the related items."""
    def __init__(self, parent, messages):
        wx.Panel.__init__(self, parent=parent)

        info = wx.StaticText(self, -1, messages['backup']['backup-type'], style=wx.ALIGN_LEFT)

        self.local = wx.RadioButton ( self, -1, messages['backup-option']['local'], style=wx.RB_GROUP )
        self.external = wx.RadioButton ( self, -1, messages['backup-option']['external'] )
        self.preconfigured = wx.RadioButton ( self, -1, messages['backup-option']['preconfigured'] )

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(info, 0.5, wx.ALL, 10)
        self.sizer.Add(self.local, 1, wx.ALL, 10)
        self.sizer.Add(self.external, 1, wx.ALL, 10)
        self.sizer.Add(self.preconfigured, 1, wx.ALL, 10)
        self.SetSizer(self.sizer)

    def getSelection(self):
        """getSelection() -> string

        Returns the currently select option from this tab.  Note that if options
        are disabled above, they must be disabled here as well.

        return string"""
        if self.local.GetValue() == True:
            return 'local'
        if self.external.GetValue() == True:
            return 'external'
        if self.preconfigured.GetValue() == True:
            return 'preconfigured'
# ---------------------------------------------------------------------------- #


# ------ 3. Select Source Location Tab --------------------------------------- #
class Tab_SelectSourceLocation(wx.Panel):
    """Tab_SelectSourceLocation( parent, messages ):

    The Select Source Location Tab.  This tab prompts the user for the source
    of the backup to be made.  Generally, this is the root of the partition, 
    unless an external backup, where it may be mounted anywhere.  It autodetects
    the Operating System on the particular share."""
    def __init__(self, parent, messages):
        wx.Panel.__init__(self, parent=parent)

        info = wx.StaticText(self, -1, messages['backup']['select-source'], style=wx.ALIGN_LEFT)

        self.selection = wx.StaticText(self, -1, "", style=wx.ALIGN_LEFT)
        self.detected_os_text = wx.StaticText(self, -1, "", style=wx.ALIGN_LEFT)
        self.detected_os = {}
    
        self.browse = wx.Button(self, label="Browse...")

        self.Bind(wx.EVT_BUTTON, self.select_directory(parent), self.browse)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(info, 0.5, wx.ALL, 10)
        self.sizer.Add(self.browse, 0.5, wx.ALL, 5)
        self.sizer.Add(self.selection, 1, wx.ALL, 10)
        self.sizer.Add(self.detected_os_text, 0.5, wx.ALL, 10)

        self.SetSizer(self.sizer)

    def select_directory(self, parent):
        """select_directory( parent ):

        Event handler for when a directory is selected.  It changes the text on the 
        window to represent the directory that was selected, shows the detected OS,
        and populates the users combobox on the Select Users Tab."""
        def onclick_browse(event):
            dialog = wx.DirDialog ( self, style = wx.OPEN )
            if dialog.ShowModal() == wx.ID_OK:
                self.selection.SetLabel(dialog.GetPath())
                detected = detectOS(dialog.GetPath())
                if detected == False:
                    self.detected_os_text.SetLabel("No Operating System detected at this location.")

                else:
                    self.detected_os_text.SetLabel(str(detected['readable']) + " Detected.")
                    self.detected_os = detected
                    parent.GetPage(4).clear_choices()
                    parent.GetPage(4).populate_choices(getProfiles(dialog.GetPath()))
                dialog.Destroy()
        return onclick_browse
        
    def setLocal(self, parent):
        """setLocal( parent )
        
        Sets all related fields to their proper settings as if the user had
        selected the local settings themselves."""
        detected = detectOS()
        self.detected_os_text.SetLabel(str(detected['readable']) + " Detected.")
        self.detected_os = detected
        parent.GetPage(4).clear_choices()
        if detected['family'] == 'windows':
            self.selection.SetLabel('C:\\')
            parent.GetPage(4).populate_choices(getProfiles('C:\\'))
        else:
            self.selection.SetLabel('/')
            parent.GetPage(4).populate_choices(getProfiles('/'))

    def getSelection(self):
        """getSelection() -> string

        Returns the currently selected directory.

        return string directory"""
        return str(self.selection.GetLabel())

    def getOS(self):
        """getOS() -> list

        Returns the autodetected Operating System from this tab.

        return list operating_system"""
        return self.detected_os
# ---------------------------------------------------------------------------- #


# ------ 4. Select Target Location Tab --------------------------------------- #
class Tab_SelectTargetLocation(wx.Panel):
    """Tab_SelectTargetLocation( parent, list messages )

    The Select Target Location Tab.  This tab prompts the user for where they 
    would like to store the backup.  It also alerts them to the amount of free 
    space on the device they have chosen."""
    def __init__(self, parent, messages):
        wx.Panel.__init__(self, parent=parent)

        info = wx.StaticText(self, -1, messages['backup']['select-target'], style=wx.ALIGN_LEFT)

        self.selection = wx.StaticText(self, -1, "", style=wx.ALIGN_LEFT)
        self.freespace = wx.StaticText(self, -1, "", style=wx.ALIGN_LEFT)
    
        self.browse = wx.Button(self, label="Browse...")

        self.Bind(wx.EVT_BUTTON, self.select_directory(), self.browse)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(info, 0.5, wx.ALL, 10)
        self.sizer.Add(self.browse, 0.5, wx.ALL, 5)
        self.sizer.Add(self.selection, 1, wx.ALL, 10)
        self.sizer.Add(self.freespace, 0.5, wx.ALL, 10)

        self.SetSizer(self.sizer)

    def select_directory(self):
        """select_directory()

        Event handler for when a directory is selected.  It changes the text to
        show the selected directory and how much free space is available."""
        def onclick_browse(event):
            dialog = wx.DirDialog ( self, style = wx.SAVE )
            if dialog.ShowModal() == wx.ID_OK:
                self.selection.SetLabel(dialog.GetPath())
                self.freespace.SetLabel(str(freespace(dialog.GetPath())))
                dialog.Destroy()
        return onclick_browse

    def getSelection(self):
        """getSelection() -> string

        Returns the currently selected directory.

        return string directory"""
        return str(self.selection.GetLabel())
# ---------------------------------------------------------------------------- #


# ------ 5. Select User Profile Tab ------------------------------------------ #
class Tab_SelectUser(wx.Panel):
    """Tab_SelectUser( parent, list messages ):

    The Select User tab.  This tab prompts the user to select the user profile to
    be backed up.  This list is autogenerated by the select source tab."""
    def __init__(self, parent, messages):
        wx.Panel.__init__(self, parent=parent)

        info = wx.StaticText(self, -1, messages['backup']['select-user'], style=wx.ALIGN_LEFT)
        
        self.combobox = wx.ComboBox(self, -1, size=wx.Size(250, 30), style=wx.CB_READONLY, choices = [])
        self.Bind(wx.EVT_COMBOBOX, self.set_possible_locations(parent), self.combobox)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(info, 0.5, wx.ALL, 10)
        self.sizer.Add(self.combobox, 0.5, wx.ALL, 10)
        self.SetSizer(self.sizer)

    def set_possible_locations(self, parent):
        """set_possible_locations( parent ):
        
        Event handler for when a user is selected.  It automatically discovers 
        what backup options are available, and disables those that are not
        available on the Select Locations tab."""
        def onselect_user(event):
            locations_tab = parent.GetPage(5)
            source = parent.GetPage(2).getSelection()
            os = parent.GetPage(2).getOS()
            user = self.getSelection()
            user_directory = dirString( getProfilesFolder( source ) + user )
            locations = getLocations(readXML('wonderbackup.xml'), os['family'], os['version'])
            locations_tab.enable_all()
            if os['family'] != 'windows':
                locations_tab.disable('internetexplorer')
            if os['family'] == 'windows' and os['version'] == 'xp,2003':
                locations_tab.disable('music')
                locations_tab.disable('pictures')
                locations_tab.disable('videos')
            for key in locations.keys():
                if checkLocation( user_directory + locations[key] ) != True:
                    locations_tab.disable(key)
        return onselect_user

    def populate_choices(self, choices):
        """populate_choices( list choices ):

        Adds all choices to the combobox."""
        for i in range(len(choices)):
            self.combobox.Append(choices[i])

    def clear_choices(self):
        """clear_choices()

        Removes all choices from the combobox."""
        self.combobox.Clear()

    def getSelection(self):
        """getSelection() -> string

        Returns the currently selected user.

        return string"""
        return str(self.combobox.GetValue())
# ---------------------------------------------------------------------------- #


# ------ 6. Select Locations for Backup Tab ---------------------------------- #
class Tab_SelectLocations(wx.Panel):
    """Tab_SelectLocations( parent, list messages, int start_location, int inbetween )

    The Select Backup Locations Tab.  This tab prompts the user for which categories
    they wish to backup.  Options that are not available for the specific OS are
    disabled at the Select Users tab."""
    def __init__(self, parent, messages, start_location, inbetween):
        wx.Panel.__init__(self, parent=parent)

        info = wx.StaticText(self, -1, messages['backup']['select-locations'], style=wx.ALIGN_LEFT)

        start_checkboxes = start_location
        self.desktop = wx.CheckBox(self, -1, 'Desktop', (10, start_checkboxes+inbetween))
        self.documents = wx.CheckBox(self, -1, 'Documents', (10, start_checkboxes+inbetween*2))
        self.internetexplorer = wx.CheckBox(self, -1, 'Internet Explorer', (10, start_checkboxes+inbetween*3))
        self.mozilla = wx.CheckBox(self, -1, 'Mozilla Firefox', (10,start_checkboxes+inbetween*4))
        self.music = wx.CheckBox(self, -1, 'Music', (10,start_checkboxes+inbetween*5))
        self.pictures = wx.CheckBox(self, -1, 'Pictures', (10, start_checkboxes+inbetween*6))
        self.videos = wx.CheckBox(self, -1, 'Videos', (10, start_checkboxes+inbetween*7))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(info, 0, wx.ALL, 10)
        self.SetSizer(sizer)

    def disable(self, item):
        """disable( item ):

        Disables the specified item from the selection."""
        if item == 'desktop':
            self.desktop.Disable()
        elif item == 'documents':
            self.documents.Disable()
        elif item == 'internetexplorer':
            self.internetexplorer.Disable()
        elif item == 'mozilla':
            self.mozilla.Disable()
        elif item == 'music':
            self.music.Disable()
        elif item == 'pictures':
            self.pictures.Disable()
        elif item == 'videos':
            self.videos.Disable()
        else:
            print "Cannot disable " + str(item) + " because it does not exist."

    def enable_all(self):
        """enable_all()

        Enables all possible options."""
        self.desktop.Enable()
        self.documents.Enable()
        self.internetexplorer.Enable()
        self.mozilla.Enable()
        self.music.Enable()
        self.pictures.Enable()
        self.videos.Enable()

    def getSelection(self):
        """getSelection() -> list

        Returns the currently selected backup locations as a list.

        return list selected"""
        selected = []
        if self.desktop.Value == True:
            selected.append('Desktop')
        if self.documents.Value == True:
            selected.append('Documents')
        if self.internetexplorer.Value == True:
            selected.append('Internet Explorer')
        if self.mozilla.Value == True:
            selected.append('Mozilla')
        if self.music.Value == True:
            selected.append('Music')
        if self.pictures.Value == True:
            selected.append('Pictures')
        if self.videos.Value == True:
            selected.append('Videos')
        return selected
# ---------------------------------------------------------------------------- #


# ------ 7. Select Exclusion Patterns Tab ------------------------------------ #
class Tab_SelectExclusions(wx.Panel):
    """Tab_SelectExclusions( parent, list messages, int start_location, int inbetween )

    The Select Exclusions tab.  Prompts the user for which exclusions they wish
    to enable."""
    def __init__(self, parent, messages, start_location, inbetween):
        wx.Panel.__init__(self, parent=parent)

        info = wx.StaticText(self, -1, messages['backup']['select-exclusions'], style=wx.ALIGN_LEFT)

        start_checkboxes = start_location
        self.music = wx.CheckBox(self, -1, 'Music', (10, start_checkboxes+inbetween))
        self.pictures = wx.CheckBox(self, -1, 'Pictures', (10, start_checkboxes+inbetween*2))
        self.tempfiles = wx.CheckBox(self, -1, 'Temporary Files', (10, start_checkboxes+inbetween*3))
        self.videos = wx.CheckBox(self, -1, 'Videos', (10,start_checkboxes+inbetween*4))
        self.virtualmachines = wx.CheckBox(self, -1, 'Virtual Machines', (10, start_checkboxes+inbetween*5))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(info, 0, wx.ALL, 10)
        self.SetSizer(sizer)

    def disable(self, item):
        """disable( item ):

        Disables the specified item from the selection."""
        if item == 'music':
            self.music.Disable()
        elif item == 'pictures':
            self.pictures.Disable()
        elif item == 'tempfiles':
            self.tempfiles.Disable()
        elif item == 'videos':
            self.videos.Disable()
        elif item == 'virtualmachines':
            self.virtualmachines.Disable()
        else:
            print "Cannot disable " + str(item) + " because it does not exist."

    def enable_all(self):
        """enable_all()

        Enables all possible options."""
        self.music.Enable()
        self.pictures.Enable()
        self.tempfiles.Enable()
        self.videos.Enable()
        self.virtualmachines.Enable()

    def getSelection(self):
        """getSelection() -> list

        Returns the currently selected exclusions as a list.

        return list selected"""
        selected = []
        if self.music.Value == True:
            selected.append('Music')
        if self.pictures.Value == True:
            selected.append('Pictures')
        if self.tempfiles.Value == True:
            selected.append('Temporary Files')
        if self.videos.Value == True:
            selected.append('Videos')
        if self.virtualmachines.Value == True:
            selected.append('Virtual Machines')
        return selected
# ---------------------------------------------------------------------------- #


# ------ 8. Start Backup Tab ------------------------------------------------- #        
class Tab_BackupProgress(wx.Panel):
    """Tab_BackupProgress( parent, list messages )
    
    The final tab encountered by the user.  Clicking "Start Backup" will begin
    the backup progress, disabling all buttons and tabs."""
    def __init__(self, parent, messages):
        wx.Panel.__init__(self, parent=parent)
        
        self.totalFiles = 0
        self.remainingFiles = 0
            
        self.fileSizes = {}
        self.totalSize = 0
        self.remainingSize = 0
        
        self.totalSteps = 0

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)

        self.status = wx.StaticText(self, -1, "Ready for Backup... [??/??]")
        self.progress = wx.Gauge(self, -1, 100, size=(350, 25))
        self.percentageComplete = wx.StaticText(self, -1, "0% Complete")
        self.filesRemaining = wx.StaticText(self, -1, "Click \"Start Backup\" to Begin...")
        self.currentFile = wx.StaticText(self, -1, "-----------------------------------------------------------------------------------------------------")

        hbox1.Add(self.progress, 1, wx.ALIGN_CENTRE)
        
        vbox.Add((0, 50), 0)
        vbox.Add(self.status, 0, wx.ALIGN_CENTRE)
        vbox.Add((0, 10), 0)
        vbox.Add(hbox1, 0, wx.ALIGN_CENTRE)
        vbox.Add(self.percentageComplete, 0, wx.ALIGN_CENTRE)
        vbox.Add((0, 30), 0)
        vbox.Add(self.filesRemaining, 1, wx.ALIGN_CENTRE)
        vbox.Add((0, 50), 0)
        vbox.Add(self.currentFile, 1, wx.ALIGN_CENTRE)

        self.SetSizer(vbox)
        
    def getFilesAndSizes(self, backupLocations, exclusionPatterns):
        """getFilesAndSizes( dict backupLocations, list exclusionPatterns )
        
        When called from outside of the function, sets the local variables
          fileSizes, totalSize, remainingSize, totalFiles, remainingFiles
        to their proper values."""
        for key in backupLocations.keys():
            self.totalSteps += 1
            files = getBackupFiles( backupLocations[key], exclusionPatterns )
            for j in files:
                fileSize = os.stat(j).st_size
                self.fileSizes[j] = fileSize
                self.totalSize += fileSize
                self.remainingSize += fileSize
                self.totalFiles += 1
                self.remainingFiles += 1

    def shortFilename(self, filename ):
        """shortFilename( string filename ) -> string
        
        Returns a string of the truncated filename.
        
        return string filename"""
        if len(filename) >= 35:
            newname = "..."
            for i in range(len(filename)-36, len(filename)):
                newname += filename[i]
            return newname
        return filename
                
    def setStatus(self, step, number):
        """setStatus( string step, int number )
        
        Updates the status StaticText to the current 'step' being backed up."""
        self.status.SetLabel("Backing up " + step + " [" + str(number) + "/" + str(self.totalSteps) + "]")
        
    def setProgress(self):
        """setProgress( )
        
        Updates the progress bar and percentage complete to the appropriate values."""
        value = 100-((self.remainingSize*1.0)/(self.totalSize*1.0))*100
        strValue = str(value)
        shortValue = ""
        for i in range(len(strValue)):
            if strValue[i] == '.':
                break
            shortValue += strValue[i]
        self.progress.SetValue(value)
        self.percentageComplete.SetLabel( shortValue + "% Complete" )
        
    def setFilesRemaining(self):
        """setFilesRemaining( )
        
        Updates the text for filesRemaining to current values."""
        self.filesRemaining.SetLabel( str(self.remainingFiles) + " files (" + readableSize(self.remainingSize) + ") of " + str(self.totalFiles) + " (" + readableSize(self.totalSize) + ") remaining...")
        
    def setCurrentFile(self, filename):
        """setCurrentFile( string filename )
        
        Updates the text of currentFile to 'filename'."""
        self.currentFile.SetLabel( "Copying [" + self.shortFilename(str(filename)) + "] (" + readableSize( self.fileSizes[filename] ) + ")" )
            
    def backupProgress(self, parent, backupLocations, targetDirectory, exclusionPatterns):
        """backupProgress( parent, dict backupLocations, string targetDirectory, list exclusionPatterns )
        
        Runs the backup using the specified values.
        
        An error log is generated at the targetDirectory as ErrorLog.txt"""
        try:
            ErrorLog = open(dirString(targetDirectory) + "ErrorLog.txt", 'a')
        except Exception:
            dialog = wx.MessageDialog(None, "This location does not\nappear to be writeable.", 'Write Error', wx.OK | 
                wx.ICON_EXCLAMATION)
            dialog.ShowModal()
            return False

            
        ErrorLog.write("[Wonder Backup Session " + timestamp() + "]\r\n")
        for i in range(0,7):
            parent.GetPage(i).Disable()
            parent.GetPage(i).Hide()
        self.getFilesAndSizes( backupLocations, exclusionPatterns )
        keyIndex = 0
        for key in backupLocations.keys():
            keyIndex += 1
            self.setStatus(key, keyIndex)
            if not checkLocation( dirString(targetDirectory) + key ):
                mkdir(dirString(targetDirectory) + key)
            backupFiles = getBackupFiles( backupLocations[key], exclusionPatterns )
            backupFiles.sort()
        
            FolderErrors = makeBackupFolders( backupLocations[key], dirString(targetDirectory) + key )
            
            for item in FolderErrors:
                ErrorLog.write(item + "\r\n")                
            
            targetFiles = targetFilenames( backupLocations[key], dirString( dirString(targetDirectory) + key), backupFiles )
            targetFiles.sort()
            
            for i in range(len(backupFiles)):
                self.setProgress()
                self.setFilesRemaining()
                self.setCurrentFile(backupFiles[i])
                if isfile(targetFiles[i]):
                    if getAttributes(backupFiles[i]) != getAttributes(targetFiles[i]):
                        CopyError = copy( backupFiles[i], targetFiles[i] )
                        if CopyError != True:
                            ErrorLog.write(CopyError + "\r\n")    
                else:
                    CopyError = copy( backupFiles[i], targetFiles[i] )
                    if CopyError != True:
                        ErrorLog.write(CopyError + "\r\n")    
                self.remainingFiles -= 1
                self.remainingSize -= self.fileSizes[backupFiles[i]]
                wx.Yield()
        ErrorLog.write("[END SESSION]\r\n\r\n\r\n\r\n")
        ErrorLog.close()
        self.backupComplete()
        return True
        
    def backupComplete(self):
        """backupComplete( )
        
        Updates all fields to complete values."""
        self.status.SetLabel("Backup Complete")
        self.progress.SetValue(100)
        self.percentageComplete.SetLabel("100% Complete")
        self.filesRemaining.SetLabel("")
        self.currentFile.SetLabel("")
        wx.Yield()
# ---------------------------------------------------------------------------- #

### - END TABS ------------------------------------------------------------- ###




### --- Graphical User Interface for Wonder Backup ------------------------- ###
class WonderGUI(wx.Frame):
    """
    Frame that holds all other widgets.  The primary interface of Wonder Backup.
    """
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, wx.ID_ANY, "Wonder Backup", size=(600,400) )

      # - Menu Bar ----------------------------------------------------------- #
        menubar = wx.MenuBar()

        file = wx.Menu() # File Menu
        imp = wx.MenuItem(file, 1, '&Import')
        exp = wx.MenuItem(file, 2, '&Export')
        quit = wx.MenuItem(file, 3, '&Quit\tCtrl+Q')
        file.AppendItem(imp)
        file.AppendItem(exp)
        file.AppendItem(quit)
        self.Bind(wx.EVT_MENU, self.OnQuit, id=3)
        menubar.Append(file, '&File')

        tools = wx.Menu() # Tools Menu
        xml = wx.MenuItem(tools, 4, '&View XML File')
        tools.AppendItem(xml)
        menubar.Append(tools, '&Tools')

        help = wx.Menu() # Help Menu
        about = wx.MenuItem(help, 5, '&About')
        self.Bind(wx.EVT_MENU, self.OnAboutBox, id=5)
        help.AppendItem(about)
        menubar.Append(help, '&Help')

        self.SetMenuBar(menubar)
        panel = wx.Panel(self)
      # - END MENU BAR ------------------------------------------------------- #

        language = 'en'
        settings = readXML("wonderbackup.xml")
        messages = getMessages(readXML("localizations.xml"), language)
        exclusions = getExclusions(settings)

      # - Notebook (Tabs) ---------------------------------------------------- # 
        if detectOS()['family'] == 'linux':
            notebook = wx.Notebook(panel, style=wx.NB_LEFT)
        else:
            notebook = wx.Notebook(panel, style=wx.NB_TOP)
        self.current_page = 1
        tabWelcome = Tab_Welcome(notebook, messages )
        notebook.AddPage(tabWelcome, "Welcome")
# Select Backup Type Tab:
        tabOne = Tab_SelectBackupType(notebook, messages)
        notebook.AddPage(tabOne, "Backup Type")
# Select Source Location Tab:
        tabTwo = Tab_SelectSourceLocation(notebook, messages)
        notebook.AddPage(tabTwo, "Select Source")
# Select Target Location Tab:
        tabThree = Tab_SelectTargetLocation(notebook, messages)
        notebook.AddPage(tabThree, "Select Target")
# Select Users Tab:
        tabFour = Tab_SelectUser(notebook, messages)
        notebook.AddPage(tabFour, "Select Users")
# Select Locations Tab:
        tabFive = Tab_SelectLocations(notebook, messages, 30, 30)
        notebook.AddPage(tabFive, "Select Locations")
# Select Exclusions Tab:
        tabSix = Tab_SelectExclusions(notebook, messages, 30, 30)
        notebook.AddPage(tabSix, "Select Exclusions")
# Start Backup Tab
        tabSeven = Tab_BackupProgress( notebook, messages )
        notebook.AddPage(tabSeven, "Start Backup")
        for i in range(1,8):
            notebook.GetPage(i).Hide()
      # - END NOTEBOOK ------------------------------------------------------- #

      # - Navigation Panel --------------------------------------------------- #
        navigation_panel = wx.Panel(panel)

        self.btn_prev = wx.Button(navigation_panel, label="Previous")
        self.btn_prev.Disable()
        self.btn_next = wx.Button(navigation_panel, label="Next")
        self.Bind(wx.EVT_BUTTON, self.goPrevious(notebook), self.btn_prev)
        self.Bind(wx.EVT_BUTTON, self.goNext(notebook), self.btn_next)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnNotebookPageChanging(notebook), notebook)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnNotebookPageChange(notebook, self.btn_prev, self.btn_next), notebook)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.btn_prev, 1, wx.ALL, 5)
        sizer.Add(self.btn_next, 1, wx.ALL, 5)

        navigation_panel.SetSizer(sizer)
      # - END NAVIGATION PANEL ----------------------------------------------- #

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 5, wx.ALL|wx.EXPAND, 5)
        sizer.Add(navigation_panel, 0.5, wx.ALL|wx.EXPAND, 5)
        panel.SetSizer(sizer)
        self.Layout()
 
        self.Show()

    def getBackupSettings(self, notebook):
        """getBackupSettings( notebook )

        Gets all current settings and invokes a dialog box is any of the settings 
        are missing."""
        selectedBackupType = notebook.GetPage(1).getSelection()
        selectedSourceLocation = notebook.GetPage(2).getSelection()
        sourceOS = notebook.GetPage(2).getOS()
        selectedTargetLocation = dirString( notebook.GetPage(3).getSelection() )
        selectedUser = notebook.GetPage(4).getSelection()
        selectedLocations = notebook.GetPage(5).getSelection()
        selectedExclusions = notebook.GetPage(6).getSelection()
        if selectedSourceLocation == "":
            self.somethingMissing("Source Location")
            return
        elif selectedTargetLocation == "":
            self.somethingMissing("Target Location")
            return
        elif selectedUser == "":
            self.somethingMissing("User")
            return
        elif selectedLocations == []:
            self.somethingMissing("Locations to Backup")
            return

        xmldoc = readXML("wonderbackup.xml")
        messages = getMessages(xmldoc, 'en')
            
        userProfile = dirString( getProfilesFolder( selectedSourceLocation ) + selectedUser )
            
        allLocations = getLocations( xmldoc, sourceOS['family'], sourceOS['version'] )
        backupLocations = {}
        for each in selectedLocations:
            if checkLocation( dirString( userProfile + allLocations[each] ) ):
                backupLocations[each] = dirString( userProfile + allLocations[each] )
                if len(selectedTargetLocation) >= len(backupLocations[each]):
                    if backupLocations[each] in selectedTargetLocation:
                        strStart = ""
                        for i in range(len(backupLocations[each])):
                            strStart = strStart + backupLocations[each][i]
                        if strStart == backupLocations[each]:
                            dialog = wx.MessageDialog(None, "You cannot backup to a folder\nyou're making a backup of.", 'Forbidden Backup', wx.OK | 
                                wx.ICON_EXCLAMATION)
                            dialog.ShowModal()
                            return False
                
        allExclusions = getExclusions( xmldoc )
        backupExclusions = []
        for each in selectedExclusions:
            for i in range(len(allExclusions[each])):
                backupExclusions.append(allExclusions[each][i])
        backupExclusions.sort()

        return notebook.GetPage(7).backupProgress(notebook, backupLocations, selectedTargetLocation, backupExclusions)



    def somethingMissing(self, what):
        """somethingMissing( string what )

        Creates a dialog box that tells what important setting is missing."""
        dialog = wx.MessageDialog(None, "Missing information for\n" + what, 'You\'re Missing Something', wx.OK | 
            wx.ICON_EXCLAMATION)
        dialog.ShowModal()
        
    def OnNotebookPageChanging(self, notebook):
        def OnPageChange(event):
            current_page = notebook.GetSelection()
            self.current_page = current_page
        return OnPageChange
        
    def OnNotebookPageChange(self, notebook, btn_prev, btn_next):
        def OnPageChange(event):
            new_page = notebook.GetSelection()
            if btn_next.Label != "Close":
                btn_next.SetLabel("Next")
            if btn_next.Label == "Close":
                notebook.ChangeSelection(self.current_page)
            elif new_page == 0:
                btn_prev.Disable()
            else:
                btn_prev.Enable()
                btn_prev.Show()
                if new_page == 7:
                    btn_next.SetLabel("Start Backup")
            self.current_page = notebook.GetSelection()
        return OnPageChange

    def goPrevious(self, notebook):
        """goPrevious( notebook )

        Event handler for when the Previous button is clicked."""
        def onclick_previous(event):
            self.btn_next.Enable()
            if notebook.GetSelection() == 3 and notebook.GetPage(1).getSelection() == 'local':
                self.btn_prev.Disable()
                notebook.ChangeSelection(1)
            else:
                if notebook.GetSelection() == 1:
                    self.btn_prev.Disable()
                self.btn_next.SetLabel(label="Next")
                notebook.ChangeSelection(notebook.GetSelection()-1)
        return onclick_previous

    def goNext(self, notebook):
        """goNext( notebook ):

        Event handler for when the Next button is clicked."""
        def onclick_next(event):
            self.btn_prev.Enable()
            if self.btn_next.Label == "Close":
                self.Close()
            if self.btn_next.Label == "Start Backup":
                self.btn_prev.Disable()
                self.btn_prev.Hide()
                self.btn_next.Disable()
                if self.getBackupSettings(notebook):
                    self.btn_next.Enable()
                    self.btn_next.SetLabel("Close")
                else:
                    self.btn_prev.Enable()
                    self.btn_prev.Show()
                    self.btn_next.Enable()
            if notebook.GetSelection() == 1:
                if notebook.GetPage(1).getSelection() == 'local':
                    notebook.GetPage(notebook.GetSelection()+2).Show()
                    notebook.ChangeSelection(notebook.GetSelection()+2)
                    notebook.GetPage(2).setLocal(notebook)
                else:
                    notebook.GetPage(notebook.GetSelection()+1).Show()
                    if notebook.GetSelection() == 6:
                        self.btn_next.SetLabel(label="Start Backup")
                    notebook.ChangeSelection(notebook.GetSelection()+1)
            else:
                if notebook.GetSelection() != 7:
                    notebook.GetPage(notebook.GetSelection()+1).Show()
                if notebook.GetSelection() == 6:
                    self.btn_next.SetLabel(label="Start Backup")
                try:
                    notebook.ChangeSelection(notebook.GetSelection()+1)
                except Exception:
                    False
        return onclick_next

    def OnQuit(self, event):
        """onQuit( event )

        Event handler for when 'quit' is called."""
        self.Close()

    def OnAboutBox(self, event):
        """OnAboutBox( event )

        Shows the About dialog."""
        messages = getMessages(readXML("localizations.xml"), 'en')

        info = wx.AboutDialogInfo()

        info.SetIcon(wx.Icon('Icon.png', wx.BITMAP_TYPE_PNG))
        info.SetName('Wonder Backup')
        info.SetVersion(messages['about']['version'])
        info.SetDescription(messages['about']['description'])
        info.SetCopyright('(C) 2010 Sean Davis')
        info.SetWebSite('http://wonderbackup.sourceforge.net')
        info.SetLicence(messages['about']['license'])
        info.AddDeveloper('Sean Davis')
        info.AddDocWriter('Sean Davis')
        info.AddArtist('Sean Davis')
        info.AddTranslator('Sean Davis')

        wx.AboutBox(info)
 
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = WonderGUI()
    app.MainLoop()
