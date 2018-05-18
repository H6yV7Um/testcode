@echo off
set  vpnDestPath=C:\Program Files\OpenVPN\config
set  vpnTempPath=C:\vpn_client_conf\openvpn_x86_64_and_conf_new\ConfigFilesForClient
set  vpnBackPath=C:\backup_openvpn_config

echo ######################################################################
echo #### 1.To update vpn client conf and help you install clinet      ####
echo #### 2.Ensure the path vpn installed is default                   ####
echo ######################################################################
pause 

rem add persistent routes 
C:\windows\system32\route.exe -p ADD 10.8.0.0 MASK 255.255.0.0 192.168.10.1

rem  just for runing muti times
if exist "c:\openvpn_x86_64_and_conf_new.rar" (del "c:\openvpn_x86_64_and_conf_new.rar")
if exist "C:\vpn_client_conf" (rmdir /s /q "C:\vpn_client_conf")
if exist "C:\backup_openvpn_config" (rmdir /s /q "C:\backup_openvpn_config")
if exist "c:\dlvpn.vbs" (del "c:\dlvpn.vbs")
if exist "c:\Rar.exe" (del "c:\Rar.exe")
rem downlaod files from lego01 server
echo Set xPost = CreateObject("Microsoft.XMLHTTP") >c:\dlvpn.vbs 
echo xPost.Open "GET",  "http://szwg-waimai-lego01.szwg01.baidu.com:8797/static/openvpn_x86_64_and_conf_new.rar",0 >>c:\dlvpn.vbs 
echo xPost.Send() >>c:\dlvpn.vbs 
echo Set sGet = CreateObject("ADODB.Stream") >>c:\dlvpn.vbs 
echo sGet.Mode = 3 >>c:\dlvpn.vbs 
echo sGet.Type = 1 >>c:\dlvpn.vbs 
echo sGet.Open() >>c:\dlvpn.vbs 
echo sGet.Write(xPost.responseBody) >>c:\dlvpn.vbs 
echo sGet.SaveToFile "c:\openvpn_x86_64_and_conf_new.rar",2 >>c:\dlvpn.vbs
echo MsgBox "Files Downloaded Completely ! ",0,"Tips" >>c:\dlvpn.vbs
cscript c:\dlvpn.vbs
del   c:\dlvpn.vbs

rem downlaod files from lego01 server
echo Set xPost = CreateObject("Microsoft.XMLHTTP") >c:\dlvpn.vbs 
echo xPost.Open "GET",  "http://szwg-waimai-lego01.szwg01.baidu.com:8797/static/Rar.exe",0 >>c:\dlvpn.vbs 
echo xPost.Send() >>c:\dlvpn.vbs 
echo Set sGet = CreateObject("ADODB.Stream") >>c:\dlvpn.vbs 
echo sGet.Mode = 3 >>c:\dlvpn.vbs 
echo sGet.Type = 1 >>c:\dlvpn.vbs 
echo sGet.Open() >>c:\dlvpn.vbs 
echo sGet.Write(xPost.responseBody) >>c:\dlvpn.vbs 
echo sGet.SaveToFile "c:\Rar.exe",2 >>c:\dlvpn.vbs
echo MsgBox "Rar Files Downloaded Completely ! ",0,"Rar Tips" >>c:\dlvpn.vbs
cscript c:\dlvpn.vbs
del   c:\dlvpn.vbs
 
rem  unzip files
c:\Rar.exe x c:\openvpn_x86_64_and_conf_new.rar  c:\vpn_client_conf\
echo unzip done!
rem installed client 
start /wait C:\vpn_client_conf\openvpn_x86_64_and_conf_new\ClientInstaller\openvpn-install-2.3.11-I601-x86_64.exe /s /v/qn
rem  backup old confs if exists
cd   C:\
mkdir backup_openvpn_config
if exist "%vpnDestPath%\ca.crt"       (copy "%vpnDestPath%\ca.crt"      "%vpnBackPath%\ca.crt")
if exist "%vpnDestPath%\client.crt"   (copy "%vpnDestPath%\client.crt"  "%vpnBackPath%\client.crt")
if exist "%vpnDestPath%\client.key"   (copy "%vpnDestPath%\client.key"  "%vpnBackPath%\client.key")
if exist "%vpnDestPath%\client.ovpn"  (copy "%vpnDestPath%\ca.crt"      "%vpnBackPath%\client.ovpn")
echo backup done!
rem  update new conf
copy "%vpnTempPath%\ca.crt"       "%vpnDestPath%\ca.crt"
copy "%vpnTempPath%\client.crt"   "%vpnDestPath%\client.crt"
copy "%vpnTempPath%\client.key"   "%vpnDestPath%\client.key"
copy "%vpnTempPath%\client.ovpn"  "%vpnDestPath%\client.ovpn"
echo update done!
echo just start up openvpn and connect to the server 
echo following the user's guide that we give
pause
