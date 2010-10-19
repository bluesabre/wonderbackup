# ---------------------------------------------------------------------------- #
# Wonder Backup - http://wonderbackup.sourceforge.net/
# wonder_gui.py
#
# Contains the functions for the graphical user interface.
#
# Modified by Sean Davis on October 18, 2010
# ---------------------------------------------------------------------------- #

import wx

### - The Individual Tabs -------------------------------------------------- ###
class Tab_BackupType(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)

        information = '''Please select the backup type.  'Local' refers to a backup 
performed on your own computer.  'External' refers to a 
mounted media, such as an external hard drive.  You can 
also open a preconfigured backup.'''


        info = wx.StaticText(self, -1, information, style=wx.ALIGN_LEFT)


        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(info, 0, wx.ALL, 10)
        self.SetSizer(sizer)

class Tab_BackupLocations(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)

        information = '''Please select the backup location.  You can backup to 
external media or a computer on your network.'''

        info = wx.StaticText(self, -1, information, style=wx.ALIGN_LEFT)


        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(info, 0, wx.ALL, 10)
        self.SetSizer(sizer)

class Tab_SelectUsers(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)

        information = '''Please select the user you would like to backup.  The 
Operating Systemhas been automatically determined.'''

        info = wx.StaticText(self, -1, information, style=wx.ALIGN_LEFT)


        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(info, 0, wx.ALL, 10)
        self.SetSizer(sizer)

class Tab_StartBackup(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)

        information = '''When you are certain that all your settings are correct,
proceed with the backup.'''

        info = wx.StaticText(self, -1, information, style=wx.ALIGN_LEFT)


        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(info, 0, wx.ALL, 10)
        self.SetSizer(sizer)
### - END TABS ------------------------------------------------------------- ###
 
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

      # - Notebook (Tabs) ---------------------------------------------------- # 
        notebook = wx.Notebook(panel, style=wx.NB_LEFT)

        tabOne = Tab_BackupType(notebook)
        notebook.AddPage(tabOne, "1. Backup Type")
 
        tabTwo = Tab_BackupLocations(notebook)
        notebook.AddPage(tabTwo, "2. Backup Locations")
 
        tabThree = Tab_SelectUsers(notebook)
        notebook.AddPage(tabThree, "3. Select Users")

        tabFour = Tab_StartBackup(notebook)
        notebook.AddPage(tabFour, "4. Start Backup")
      # - END NOTEBOOK ------------------------------------------------------- #

      # - Navigation Panel --------------------------------------------------- #
        navigation_panel = wx.Panel(panel)

        btn_prev = wx.Button(navigation_panel, label="Previous")
        btn_next = wx.Button(navigation_panel, label="Next")
        self.Bind(wx.EVT_BUTTON, self.goPrevious(notebook), btn_prev)
        self.Bind(wx.EVT_BUTTON, self.goNext(notebook), btn_next)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(btn_prev, 1, wx.ALL, 5)
        sizer.Add(btn_next, 1, wx.ALL, 5)

        navigation_panel.SetSizer(sizer)
      # - END NAVIGATION PANEL ----------------------------------------------- #

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 5, wx.ALL|wx.EXPAND, 5)
        sizer.Add(navigation_panel, 0.5, wx.ALL|wx.EXPAND, 5)
        panel.SetSizer(sizer)
        self.Layout()
 
        self.Show()

    def goPrevious(self, notebook):
        def onclick_previous(event):
            if notebook.GetSelection() != 0:
                notebook.ChangeSelection(notebook.GetSelection()-1)
        return onclick_previous

    def goNext(self, notebook):
        def onclick_next(event):
            notebook.ChangeSelection(notebook.GetSelection()+1)
        return onclick_next

    def OnQuit(self, event):
        self.Close()

    def OnAboutBox(self, event):
        description = """Wonder Backup is an open source, Python-powered, operating system independent backup solution for use in scenarios from end-users to enterprise solutions.
"""

        licence = """Wonder Backup is free software, though licensing is a difficult
legal decision that will be left for a later point in time.

Ultimately, I wish for this software to be free for anyone and 
everyone, and hope to one day find a suitable license."""


        info = wx.AboutDialogInfo()

        info.SetIcon(wx.Icon('Icon.png', wx.BITMAP_TYPE_PNG))
        info.SetName('Wonder Backup')
        info.SetVersion('preAlpha')
        info.SetDescription(description)
        info.SetCopyright('(C) 2010 Sean Davis')
        info.SetWebSite('http://wonderbackup.sourceforge.net')
        info.SetLicence(licence)
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
