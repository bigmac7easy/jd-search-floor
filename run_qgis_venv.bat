@echo off
setlocal

call "C:\Program Files\QGIS 3.44.9\bin\o4w_env.bat"

set "PATH=%~dp0.venv\Scripts;%OSGEO4W_ROOT%\apps\qgis-ltr\bin;%PATH%"
set "QGIS_PREFIX_PATH=%OSGEO4W_ROOT%\apps\qgis-ltr"
set "QT_PLUGIN_PATH=%OSGEO4W_ROOT%\apps\qgis-ltr\qtplugins;%OSGEO4W_ROOT%\apps\qt5\plugins"
set "PYTHONPATH=%OSGEO4W_ROOT%\apps\qgis-ltr\python;%PYTHONPATH%"
set "GDAL_FILENAME_IS_UTF8=YES"
set "PYTHONHOME="

"%~dp0.venv\Scripts\python.exe" %*