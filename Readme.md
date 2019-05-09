# Pace and Pull Software Aid for the Seeing Eye

The entirety of the Python application is contained in "Final_app.py". As this is a Python application, there are executables being made.

## Making Executables

It is recommended to use Pyinstaller in order to make the executables desired if updating the application. Due to inclusion of additional libraries, the .spec file needs to be edited (if it was autogenerated). In the .spec file, there should be an Analysis object created, as seen below.

```
a = Analysis(['Final_app.py'],
             pathex=['/home/nek/Documents/Classes/TAD'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
```

The hiddenimports should be given a different value so that it includes the new libraries. Therefore, replace the original hiddenimports line with the following:

```
hiddenimports=['PIL', 'PIL._imagingtk', 'PIL._tkinter_finder'],
```
