; Script generated by the HM NIS Edit Script Wizard.

; HM NIS Edit Wizard helper defines
!define PRODUCT_NAME "Wonder Backup"
!define PRODUCT_VERSION "1.0"
!define PRODUCT_PUBLISHER "Sean Davis"
!define PRODUCT_WEB_SITE "http://wonderbackup.sourceforge.net"
!define PRODUCT_DIR_REGKEY "Software\Microsoft\Windows\CurrentVersion\App Paths\wbGUI.exe"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"

; MUI 1.67 compatible ------
!include "MUI.nsh"

; MUI Settings
!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"

; Welcome page
!insertmacro MUI_PAGE_WELCOME
; License page
!define MUI_LICENSEPAGE_CHECKBOX
!insertmacro MUI_PAGE_LICENSE "license.txt"
; Directory page
!insertmacro MUI_PAGE_DIRECTORY
; Instfiles page
!insertmacro MUI_PAGE_INSTFILES
; Finish page
!define MUI_FINISHPAGE_RUN "$INSTDIR\wbGUI.exe"
!define MUI_FINISHPAGE_SHOWREADME "$INSTDIR\README.txt"
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_INSTFILES

; Language files
!insertmacro MUI_LANGUAGE "English"

; MUI end ------

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "Setup.exe"
InstallDir "$PROGRAMFILES\Wonder Backup"
InstallDirRegKey HKLM "${PRODUCT_DIR_REGKEY}" ""
ShowInstDetails show
ShowUnInstDetails show

Section "MainSection" SEC01
  SetOutPath "$INSTDIR"
  SetOverwrite on
  File "dist\wxmsw28uh_html_vc.dll"
  File "dist\wxmsw28uh_core_vc.dll"
  File "dist\wxmsw28uh_adv_vc.dll"
  File "dist\wxbase28uh_vc.dll"
  File "dist\wxbase28uh_net_vc.dll"
  File "dist\wx._windows_.pyd"
  File "dist\wx._misc_.pyd"
  File "dist\wx._gdi_.pyd"
  File "dist\wx._core_.pyd"
  File "dist\wx._controls_.pyd"
  File "dist\wonderbackup.xml"
  File "dist\wbGUI.exe"
  CreateDirectory "$SMPROGRAMS\Wonder Backup"
  CreateShortCut "$SMPROGRAMS\Wonder Backup\Wonder Backup.lnk" "$INSTDIR\wbGUI.exe"
  CreateShortCut "$DESKTOP\Wonder Backup.lnk" "$INSTDIR\wbGUI.exe"
  File "dist\wbCLI.exe"
  File "dist\w9xpopen.exe"
  File "dist\unicodedata.pyd"
  File "dist\select.pyd"
  File "dist\README.txt"
  File "dist\python27.dll"
  File "dist\pyexpat.pyd"
  File "dist\msvcr90.dll"
  File "dist\msvcp90.dll"
  File "dist\msvcm90.dll"
  File "dist\Microsoft.VC90.MFCLOC.manifest"
  File "dist\Microsoft.VC90.MFC.manifest"
  File "dist\Microsoft.VC90.CRT.manifest"
  File "dist\Microsoft.VC90.ATL.manifest"
  File "dist\localizations.xml"
  File "dist\license.txt"
  File "dist\library.zip"
  File "dist\Icon.png"
  File "dist\Icon.ico"
  File "dist\ico16.ico"
  File "dist\gdiplus.dll"
  File "dist\bz2.pyd"
  File "dist\_ssl.pyd"
  File "dist\_socket.pyd"
  File "dist\_ctypes.pyd"
SectionEnd

Section -AdditionalIcons
  WriteIniStr "$INSTDIR\${PRODUCT_NAME}.url" "InternetShortcut" "URL" "${PRODUCT_WEB_SITE}"
  CreateShortCut "$SMPROGRAMS\Wonder Backup\Website.lnk" "$INSTDIR\${PRODUCT_NAME}.url"
  CreateShortCut "$SMPROGRAMS\Wonder Backup\Uninstall.lnk" "$INSTDIR\uninst.exe"
SectionEnd

Section -Post
  WriteUninstaller "$INSTDIR\uninst.exe"
  WriteRegStr HKLM "${PRODUCT_DIR_REGKEY}" "" "$INSTDIR\wbGUI.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\wbGUI.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
SectionEnd


Function un.onUninstSuccess
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK "$(^Name) was successfully removed from your computer."
FunctionEnd

Function un.onInit
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "Are you sure you want to completely remove $(^Name) and all of its components?" IDYES +2
  Abort
FunctionEnd

Section Uninstall
  Delete "$INSTDIR\${PRODUCT_NAME}.url"
  Delete "$INSTDIR\uninst.exe"
  Delete "$INSTDIR\_ctypes.pyd"
  Delete "$INSTDIR\_socket.pyd"
  Delete "$INSTDIR\_ssl.pyd"
  Delete "$INSTDIR\bz2.pyd"
  Delete "$INSTDIR\gdiplus.dll"
  Delete "$INSTDIR\ico16.ico"
  Delete "$INSTDIR\Icon.ico"
  Delete "$INSTDIR\Icon.png"
  Delete "$INSTDIR\library.zip"
  Delete "$INSTDIR\license.txt"
  Delete "$INSTDIR\localizations.xml"
  Delete "$INSTDIR\Microsoft.VC90.ATL.manifest"
  Delete "$INSTDIR\Microsoft.VC90.CRT.manifest"
  Delete "$INSTDIR\Microsoft.VC90.MFC.manifest"
  Delete "$INSTDIR\Microsoft.VC90.MFCLOC.manifest"
  Delete "$INSTDIR\msvcm90.dll"
  Delete "$INSTDIR\msvcp90.dll"
  Delete "$INSTDIR\msvcr90.dll"
  Delete "$INSTDIR\pyexpat.pyd"
  Delete "$INSTDIR\python27.dll"
  Delete "$INSTDIR\README.txt"
  Delete "$INSTDIR\select.pyd"
  Delete "$INSTDIR\unicodedata.pyd"
  Delete "$INSTDIR\w9xpopen.exe"
  Delete "$INSTDIR\wbCLI.exe"
  Delete "$INSTDIR\wbGUI.exe"
  Delete "$INSTDIR\wonderbackup.xml"
  Delete "$INSTDIR\wx._controls_.pyd"
  Delete "$INSTDIR\wx._core_.pyd"
  Delete "$INSTDIR\wx._gdi_.pyd"
  Delete "$INSTDIR\wx._misc_.pyd"
  Delete "$INSTDIR\wx._windows_.pyd"
  Delete "$INSTDIR\wxbase28uh_net_vc.dll"
  Delete "$INSTDIR\wxbase28uh_vc.dll"
  Delete "$INSTDIR\wxmsw28uh_adv_vc.dll"
  Delete "$INSTDIR\wxmsw28uh_core_vc.dll"
  Delete "$INSTDIR\wxmsw28uh_html_vc.dll"

  Delete "$SMPROGRAMS\Wonder Backup\Uninstall.lnk"
  Delete "$SMPROGRAMS\Wonder Backup\Website.lnk"
  Delete "$DESKTOP\Wonder Backup.lnk"
  Delete "$SMPROGRAMS\Wonder Backup\Wonder Backup.lnk"

  RMDir "$SMPROGRAMS\Wonder Backup"
  RMDir "$INSTDIR"

  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  DeleteRegKey HKLM "${PRODUCT_DIR_REGKEY}"
  SetAutoClose true
SectionEnd