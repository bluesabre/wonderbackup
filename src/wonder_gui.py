# ---------------------------------------------------------------------------- #
# Wonder Backup - http://wonderbackup.sourceforge.net/
# wonder_gui.py
#
# Contains the functions for the graphical user interface.
#
# Modified by Sean Davis on November 2, 2010
# ---------------------------------------------------------------------------- #
from wb_xml import *
import wx
from wb_backup import *
from wb_file import *
from wb_os import *
from wb_xml import *


class Notebook_Tab(wx.Panel):
    """ This is the generalized Notebook tab.  It has since been depracated and 
    will soon be removed."""
    def __init__(self, parent, message):
        wx.Panel.__init__(self, parent=parent)

        info = wx.StaticText(self, -1, message, style=wx.ALIGN_LEFT)
        self.extra = {}

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(info, 0.5, wx.ALL, 10)
        self.SetSizer(self.sizer)

    def add_to_sizer(self, what, number=1, how=wx.ALL, size=10):
        """def add_to_sizer(anything what, int number, spacing how, int size)
    
        Adds an item what to the sizer of the Notebook."""
        self.sizer.Add(what, number, how, size)

class Tab_Welcome(wx.Panel):
    """Tab_Welcome( parent )

    This is the first tab the user encounters.  It displays a welcome message and
    has a button that shows the Release Notes."""
    def __init__(self, parent, messages):
        wx.Panel.__init__(self, parent=parent)

        png = wx.Image('Icon.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        image = wx.StaticBitmap(self, -1, png, (10, 5), (png.GetWidth(), png.GetHeight()))

        self.notes = wx.Button(self, label="Release Notes")
        self.Bind(wx.EVT_BUTTON, self.release_notes(parent, messages), self.notes)

        info = wx.StaticText(self, -1, get_message(messages[5], 'welcome'), style=wx.ALIGN_LEFT)
        self.extra = {}

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(image, 0.5, wx.ALL, 10)
        self.sizer.Add(info, 0.5, wx.ALL, 10)
        self.sizer.Add(self.notes, 0.5, wx.ALL, 10)
        self.SetSizer(self.sizer)

    def release_notes(self, parent, messages):
        """release_notes(parent, list messages)

        Opens a dialog box that contains the release notes.  Has a close button
        to return to the program."""
        def onclick_notes(event):
            dialog = wx.Dialog(None, -1, "Release Notes", size=(450, 250))

            sizer = wx.BoxSizer(wx.VERTICAL)

            textbox = wx.TextCtrl(dialog, -1, '', style = wx.TE_MULTILINE | wx.TE_READONLY)

            closeButton = wx.Button(dialog, -1, 'Close', size=(70, 30))

            sizer.Add(textbox, 1, wx.EXPAND | wx.TOP | wx.RIGHT | wx.LEFT, 10)
            sizer.Add(closeButton, 0.5, wx.ALIGN_RIGHT, 10)

            dialog.SetSizer(sizer)
            dialog.ShowModal()
        return onclick_notes

class Tab_SelectBackupType(wx.Panel):
    """Tab_SelectBackupType( parent, list messages)

    The Select Backup Type Tab.  This tab prompts the user for the type of backup
    they wish to do.  Options are 'local', 'external', and 'preconfigured'.

    To disable any of these options, simply comment out the related items."""
    def __init__(self, parent, messages):
        wx.Panel.__init__(self, parent=parent)

        info = wx.StaticText(self, -1, get_message(messages[0],'backup-type'), style=wx.ALIGN_LEFT)

#        self.local = wx.RadioButton ( self, -1, get_message(messages[1],'local'), style=wx.RB_GROUP )
        self.external = wx.RadioButton ( self, -1, get_message(messages[1],'external'), style=wx.RB_GROUP )
#        self.preconfigured = wx.RadioButton ( self, -1, get_message(messages[1],'preconfigured') )

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(info, 0.5, wx.ALL, 10)
#        self.sizer.Add(self.local, 1, wx.ALL, 10)
        self.sizer.Add(self.external, 1, wx.ALL, 10)
#        self.sizer.Add(self.preconfigured, 1, wx.ALL, 10)
        self.SetSizer(self.sizer)

    def getSelection(self):
        """getSelection() -> string

        Returns the currently select option from this tab.  Note that if options
        are disabled above, they must be disabled here as well.

        return string"""
#        if self.local.GetValue() == True:
#            return 'local'
        if self.external.GetValue() == True:
            return 'external'
#        if self.preconfigured.GetValue() == True:
#            return 'preconfigured'

class Tab_SelectSourceLocation(wx.Panel):
    """Tab_SelectSourceLocation( parent, messages ):

    The Select Source Location Tab.  This tab prompts the user for the source
    of the backup to be made.  Generally, this is the root of the partition, 
    unless an external backup, where it may be mounted anywhere.  It autodetects
    the Operating System on the particular share."""
    def __init__(self, parent, messages):
        wx.Panel.__init__(self, parent=parent)

        info = wx.StaticText(self, -1, get_message(messages[0],'select-source'), style=wx.ALIGN_LEFT)

        self.selection = wx.StaticText(self, -1, "", style=wx.ALIGN_LEFT)
        self.detected_os_text = wx.StaticText(self, -1, "", style=wx.ALIGN_LEFT)
        self.detected_os = ""
    
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
                detected = detect_os(dialog.GetPath())
                if detected == False:
                    self.detected_os_text.SetLabel("No Operating System detected at this location.")

                else:
                    self.detected_os_text.SetLabel(str(detected[1]) + " Detected.")
                    self.detected_os = detected[0]
                    parent.GetPage(4).clear_choices()
                    parent.GetPage(4).populate_choices(get_users(str(self.selection.Label) + "/", self.detected_os))
                dialog.Destroy()
        return onclick_browse

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

class Tab_SelectTargetLocation(wx.Panel):
    """Tab_SelectTargetLocation( parent, list messages )

    The Select Target Location Tab.  This tab prompts the user for where they 
    would like to store the backup.  It also alerts them to the amount of free 
    space on the device they have chosen."""
    def __init__(self, parent, messages):
        wx.Panel.__init__(self, parent=parent)

        info = wx.StaticText(self, -1, get_message(messages[0],'select-target'), style=wx.ALIGN_LEFT)

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


class Tab_SelectUser(wx.Panel):
    """Tab_SelectUser( parent, list messages ):

    The Select User tab.  This tab prompts the user to select the user profile to
    be backed up.  This list is autogenerated by the select source tab."""
    def __init__(self, parent, messages):
        wx.Panel.__init__(self, parent=parent)

        info = wx.StaticText(self, -1, get_message(messages[0],'select-user'), style=wx.ALIGN_LEFT)
        
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
            user_directory = get_users_location( source, os ) + user + "/"
            locations = simple_locations(readXML("wonderbackup.xml"), os[0], os[1])
            locations_tab.enable_all()
            if os[0] != 'windows':
                locations_tab.disable('internetexplorer')
            if os[0] == 'windows' and os[1] == 'xp,2003':
                locations_tab.disable('music')
                locations_tab.disable('pictures')
                locations_tab.disable('videos')
            for i in range(len(locations)):
                if check_valid_location( user_directory + locations[i][1] ) != True:
                    locations_tab.disable(locations[i][0][0])
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


class Tab_SelectLocations(wx.Panel):
    """Tab_SelectLocations( parent, list messages, int start_location, int inbetween )

    The Select Backup Locations Tab.  This tab prompts the user for which categories
    they wish to backup.  Options that are not available for the specific OS are
    disabled at the Select Users tab."""
    def __init__(self, parent, messages, start_location, inbetween):
        wx.Panel.__init__(self, parent=parent)

        info = wx.StaticText(self, -1, get_message(messages[0],'select-locations'), style=wx.ALIGN_LEFT)

        start_checkboxes = start_location
        self.desktop = wx.CheckBox(self, -1, 'Desktop', (10, start_checkboxes+inbetween))
        self.documents = wx.CheckBox(self, -1, 'Documents', (10, start_checkboxes+inbetween*2))
        self.internetexplorer = wx.CheckBox(self, -1, 'Internet Explorer', (10, start_checkboxes+inbetween*3))
        self.mozilla = wx.CheckBox(self, -1, 'Mozilla Firefox', (10,start_checkboxes+inbetween*4))
        self.pictures = wx.CheckBox(self, -1, 'Pictures', (10, start_checkboxes+inbetween*5))
        self.videos = wx.CheckBox(self, -1, 'Videos', (10, start_checkboxes+inbetween*6))

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
        self.pictures.Enable()
        self.videos.Enable()

    def getSelection(self):
        """getSelection() -> list

        Returns the currently selected backup locations as a list.

        return list selected"""
        selected = []
        if self.desktop.Value == True:
            selected.append('desktop')
        if self.documents.Value == True:
            selected.append('documents')
        if self.internetexplorer.Value == True:
            selected.append('internetexplorer')
        if self.mozilla.Value == True:
            selected.append('mozilla')
        if self.pictures.Value == True:
            selected.append('pictures')
        if self.videos.Value == True:
            selected.append('videos')
        return selected

class Tab_SelectExclusions(wx.Panel):
    """Tab_SelectExclusions( parent, list messages, int start_location, int inbetween )

    The Select Exclusions tab.  Prompts the user for which exclusions they wish
    to enable."""
    def __init__(self, parent, messages, start_location, inbetween):
        wx.Panel.__init__(self, parent=parent)

        info = wx.StaticText(self, -1, get_message(messages[0],'select-exclusions'), style=wx.ALIGN_LEFT)

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
            selected.append('music')
        if self.pictures.Value == True:
            selected.append('pictures')
        if self.tempfiles.Value == True:
            selected.append('tempfiles')
        if self.videos.Value == True:
            selected.append('videos')
        if self.virtualmachines.Value == True:
            selected.append('virtualmachines')
        return selected

### - END TABS ------------------------------------------------------------- ###

class GuiBackupProgress(wx.Dialog):
    """GuiBackupProgress( parent, string source_location, list operating_system, string target_location, string user, list locations, list exclusions )

    The Progress Dialog box that appears when the backup begins.  It will show 
    current information as to what is currently being copied over, and how many
    files remain."""
    def __init__(self, parent, source_location, operating_system, target_location, user, locations, exclusions):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, "Wonder Backup Progress", wx.DefaultPosition, wx.Size(400, 80))
        parent.Disable()

        self.source = source_location
        self.target = target_location
        self.files = []

        xml_tree = readXML("wonderbackup.xml")

        self.profile = get_users_location( source_location, operating_system ) + user + "/"

        locations_list = simple_locations( xml_tree, operating_system[0], operating_system[1] )
        self.actual_locations = []
        for i in range(len(locations)):
            for j in range(len(locations_list)):
                if locations[i] == locations_list[j][0][0]:
                    self.actual_locations.append(self.profile + locations_list[j][1])

        self.exclusions = []

        panel = wx.Panel(self, 1)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.copyProgress = wx.StaticText(self, -1, "\tCopy Progress", style=wx.ALIGN_CENTER)
        self.filename = wx.StaticText(self, -1, "\tFilename", style=wx.ALIGN_CENTER)
        self.total = 0
        self.incrementer = 0

        sizer.Add(self.copyProgress, 0.5, wx.ALL, 10)
        sizer.Add(self.filename, 0.5, wx.ALL, 10)

        self.getFiles()

        panel.SetSizer(sizer)
        panel.Show()
        self.Centre()
        self.ShowModal()


    def getFiles(self):
        """getFiles()

        Gets the number of files to be backed up, and sets the total to that number."""
        for i in self.actual_locations:
           self.files += get_files_for_backup( i, self.exclusions )
        self.total = len(self.files)
        print self.total

 
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
#        quit.SetBitmap(wx.Bitmap('icons/exit.png')) # If I wanted there to be an image for a menu entry, this would be the code.
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
        messages = get_messages(readXML("localizations.xml"), language)
# Messages are in the format (backup_wizard, backup_options, dialogs, prompts, summary, welcome, about)
        locations = get_os_backup_locations(settings)
        exclusions = get_exclusions(settings)

      # - Notebook (Tabs) ---------------------------------------------------- # 
        notebook = wx.Notebook(panel, style=wx.NB_LEFT)
        tabWelcome = Tab_Welcome(notebook, messages )
        notebook.AddPage(tabWelcome, "Welcome")
# Select Backup Type Tab:
        tabOne = Tab_SelectBackupType(notebook, messages)
        notebook.AddPage(tabOne, "1. Backup Type")
# Select Source Location Tab:
        tabTwo = Tab_SelectSourceLocation(notebook, messages)
        notebook.AddPage(tabTwo, "2. Select Source")
# Select Target Location Tab:
        tabThree = Tab_SelectTargetLocation(notebook, messages)
        notebook.AddPage(tabThree, "3. Select Target")
# Select Users Tab:
        tabFour = Tab_SelectUser(notebook, messages)
        notebook.AddPage(tabFour, "4. Select Users")
# Select Locations Tab:
        tabFive = Tab_SelectLocations(notebook, messages, 30, 30)
        notebook.AddPage(tabFive, "5. Select Locations")
# Select Exclusions Tab:
        tabSix = Tab_SelectExclusions(notebook, messages, 30, 30)
        notebook.AddPage(tabSix, "6. Select Exclusions")
# Start Backup Tab
        tabSeven = Notebook_Tab(notebook, get_message(messages[0],'proceed'))
        notebook.AddPage(tabSeven, "7. Start Backup")
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
        backup_type = notebook.GetPage(1).getSelection()
        source_location = notebook.GetPage(2).getSelection()
        operating_system = notebook.GetPage(2).getOS()
        target_location = notebook.GetPage(3).getSelection()
        user = notebook.GetPage(4).getSelection()
        locations = notebook.GetPage(5).getSelection()
        exclusions = notebook.GetPage(6).getSelection()
        if source_location == "":
            self.somethingMissing("Source Location")
            return
        elif target_location == "":
            self.somethingMissing("Target Location")
            return
        elif user == "":
            self.somethingMissing("User")
            return
        elif locations == []:
            self.somethingMissing("Locations to Backup")
            return
        print "Backup Type: " + str(backup_type)
        print "Source Location: " + str(source_location)
        print "Target Location: " + str(target_location)
        print "Selected Profile: " + str(user)
        print "Locations to Back up: " + str(locations)
        print "Files to Avoid: " + str(exclusions)
        GuiBackupProgress(self, source_location, operating_system, target_location, user, locations, exclusions)



    def somethingMissing(self, what):
        """somethingMissing( string what )

        Creates a dialog box that tells what important setting is missing."""
        dialog = wx.MessageDialog(None, "Missing information for\n" + what, 'You\'re Missing Something', wx.OK | 
            wx.ICON_EXCLAMATION)
        dialog.ShowModal()        

    def goPrevious(self, notebook):
        """goPrevious( notebook )

        Event handler for when the Previous button is clicked."""
        def onclick_previous(event):
            self.btn_next.Enable()
            if notebook.GetSelection() == 1:
                self.btn_prev.Disable()
            self.btn_next.SetLabel(label="Next")
            notebook.ChangeSelection(notebook.GetSelection()-1)
#            notebook.GetPage(notebook.GetSelection()+1).Disable()
        return onclick_previous

    def goNext(self, notebook):
        """goNext( notebook ):

        Event handler for when the Next button is clicked."""
        def onclick_next(event):
            self.btn_prev.Enable()
            if self.btn_next.Label == "Start Backup":
                self.getBackupSettings(notebook)
            if notebook.GetSelection() == 1:
                if notebook.GetPage(1).getSelection() == 'local':
                    notebook.GetPage(notebook.GetSelection()+2).Show()
                    notebook.ChangeSelection(notebook.GetSelection()+2)
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
                notebook.ChangeSelection(notebook.GetSelection()+1)
        return onclick_next

    def OnQuit(self, event):
        """onQuit( event )

        Event handler for when 'quit' is called."""
        self.Close()

    def OnAboutBox(self, event):
        """OnAboutBox( event )

        Shows the About dialog."""
        messages = get_messages(readXML("localizations.xml"), 'en')

        info = wx.AboutDialogInfo()

        info.SetIcon(wx.Icon('Icon.png', wx.BITMAP_TYPE_PNG))
        info.SetName('Wonder Backup')
        info.SetVersion(get_message(messages[6], 'version'))
        info.SetDescription(get_message(messages[6], 'description'))
        info.SetCopyright('(C) 2010 Sean Davis')
        info.SetWebSite('http://wonderbackup.sourceforge.net')
        info.SetLicence(get_message(messages[6], 'license'))
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
