@echo off&Setlocal Enabledelayedexpansion		rem 设置变量延迟
REM test
REM start iexplore.exe "http://smasit.cnsuning.com/sma/sma/test/testBindingSma.htm?userId=6001861608&templateId=123618&recordCode=A63CF8B563D7A08E"
set PATH=%PATH%;%~dp0\curl		rem 设置临时环境变量
chcp 65001
cd %~dp0
echo. >result.txt
set iteration=1
for /f "skip=1 tokens=1-14 delims=	" %%a in (%~dp0/test.txt) do (	rem 跳过参数文件第一行数据不处理，其余取1-12列的数据作为12个参数
echo ---------------------------------------------------Round:!iteration!------------------------------------------------------ >> result.txt

rem 发送s码
echo  Send sma: >> result.txt
curl "http://smasit.cnsuning.com/sma/test/SendSma.do?appCode=%%h&userId=%%a&templateId=%%b&phoneNum=%%c&deliverType=%%e" >> result.txt
ping -n 2 127.1 > nul		rem 等待2秒再调用下一个服务
echo. >> result.txt
echo --------------------------------------------------------------------------------------------------------------- >> result.txt
REM 查询s码
echo. >> result.txt
echo  Query Sma: >> result.txt
curl "http://smasit.cnsuning.com/sma/test/testQuerySma.do?appCode=%%h&userId=%%a&templateId=%%b" >> result.txt
ping -n 2 127.1 > nul
echo. >> result.txt
echo --------------------------------------------------------------------------------------------------------------- >> result.txt
REM 绑定s码
echo. >> result.txt
echo  Binding Sma: >> result.txt
curl "http://smasit.cnsuning.com/sma/test/SmaBinding.do?appCode=%%h&recordCode=%%d&templateId=%%b&userId=%%a" >> result.txt
ping -n 2 127.1 > nul
echo. >> result.txt
echo --------------------------------------------------------------------------------------------------------------- >> result.txt
REM 查询s码
echo. >> result.txt
echo  Query Sma: >> result.txt
curl "http://smasit.cnsuning.com/sma/test/testQuerySma.do?appCode=%%h&userId=%%a&templateId=%%b" >> result.txt
ping -n 2 127.1 > nul
echo. >> result.txt
echo --------------------------------------------------------------------------------------------------------------- >> result.txt
rem s码录入验证
echo  testValSmaInput: >> result.txt
curl "http://smasit.cnsuning.com/sma/test/testValSmaInput.do?appCode=%%h&recordCode=%%d&templateId=%%b" >> result.txt
ping -n 2 127.1 > nul		rem 等待2秒再调用下一个服务
echo. >> result.txt
echo --------------------------------------------------------------------------------------------------------------- >> result.txt
rem s码使用验证
echo  testValSmaUse: >> result.txt
curl "http://smasit.cnsuning.com/sma/test/testSmaVal.do?appCode=%%h&recordCode=%%d&templateId=%%b&useNum=%%m&userId=%%a" >> result.txt
ping -n 2 127.1 > nul		rem 等待2秒再调用下一个服务
echo. >> result.txt			
echo --------------------------------------------------------------------------------------------------------------- >> result.txt
rem s码使用
echo. >> result.txt
echo Use Sma: >> result.txt
curl "http://smasit.cnsuning.com/sma/test/testSmaUse.do?channelId=%%n&appCode=%%h&recordCode=%%d&templateId=%%b&userId=%%a&activityCode=%%i" >> result.txt
ping -n 2 127.1 > nul
echo. >> result.txt
echo --------------------------------------------------------------------------------------------------------------- >> result.txt
REM 查询s码
echo. >> result.txt
echo  Query Sma: >> result.txt
curl "http://smasit.cnsuning.com/sma/test/testQuerySma.do?appCode=%%h&userId=%%a&templateId=%%b" >> result.txt
ping -n 2 127.1 > nul
echo. >> result.txt
echo --------------------------------------------------------------------------------------------------------------- >> result.txt
set /a iteration=iteration+1		rem 迭代计数器
)
echo "Finish,press any key to exit!"&pause>nul
start /max result.txt

goto zhushi

rem 锁定服务
echo. >> result.txt
echo Lock sma: >> result.txt
curl "http://smasit.cnsuning.com/sma/sma/test/LockingSma.htm?userId=%%a&templateId=%%b&phoneNum=%%c&recordCode=%%d&orderId=%%f&appCode=sma&orderChildId=%%g&activityCode=%%i&activityName=%%j&productId=%%k&productName=%%l" >> result.txt
ping -n 2 127.1 > nul
echo. >> result.txt
echo --------------------------------------------------------------------------------------------------------------- >> result.txt

rem 取消锁定
echo. >> result.txt
echo Unlock sma: >> result.txt
curl "http://smasit.cnsuning.com/sma/sma/test/testUnLockingSma.htm?userId=%%a&templateId=%%b&recordCode=%%d&orderId=%%f" >> result.txt
ping -n 2 127.1 > nul
echo. >> result.txt
echo --------------------------------------------------------------------------------------------------------------- >> result.txt

:zhushi