@echo off&Setlocal Enabledelayedexpansion		rem ���ñ����ӳ�
REM test
REM start iexplore.exe "http://smasit.cnsuning.com/sma/sma/test/testBindingSma.htm?userId=6001861608&templateId=123618&recordCode=A63CF8B563D7A08E"
set PATH=%PATH%;%~dp0\curl		rem ������ʱ��������
chcp 65001
cd %~dp0
echo. >result.txt
set iteration=1
for /f "skip=1 tokens=1-14 delims=	" %%a in (%~dp0/test.txt) do (	rem ���������ļ���һ�����ݲ���������ȡ1-12�е�������Ϊ12������
echo ---------------------------------------------------Round:!iteration!------------------------------------------------------ >> result.txt

rem ����s��
echo  Send sma: >> result.txt
curl "http://smasit.cnsuning.com/sma/test/SendSma.do?appCode=%%h&userId=%%a&templateId=%%b&phoneNum=%%c&deliverType=%%e" >> result.txt
ping -n 2 127.1 > nul		rem �ȴ�2���ٵ�����һ������
echo. >> result.txt
echo --------------------------------------------------------------------------------------------------------------- >> result.txt
REM ��ѯs��
echo. >> result.txt
echo  Query Sma: >> result.txt
curl "http://smasit.cnsuning.com/sma/test/testQuerySma.do?appCode=%%h&userId=%%a&templateId=%%b" >> result.txt
ping -n 2 127.1 > nul
echo. >> result.txt
echo --------------------------------------------------------------------------------------------------------------- >> result.txt
REM ��s��
echo. >> result.txt
echo  Binding Sma: >> result.txt
curl "http://smasit.cnsuning.com/sma/test/SmaBinding.do?appCode=%%h&recordCode=%%d&templateId=%%b&userId=%%a" >> result.txt
ping -n 2 127.1 > nul
echo. >> result.txt
echo --------------------------------------------------------------------------------------------------------------- >> result.txt
REM ��ѯs��
echo. >> result.txt
echo  Query Sma: >> result.txt
curl "http://smasit.cnsuning.com/sma/test/testQuerySma.do?appCode=%%h&userId=%%a&templateId=%%b" >> result.txt
ping -n 2 127.1 > nul
echo. >> result.txt
echo --------------------------------------------------------------------------------------------------------------- >> result.txt
rem s��¼����֤
echo  testValSmaInput: >> result.txt
curl "http://smasit.cnsuning.com/sma/test/testValSmaInput.do?appCode=%%h&recordCode=%%d&templateId=%%b" >> result.txt
ping -n 2 127.1 > nul		rem �ȴ�2���ٵ�����һ������
echo. >> result.txt
echo --------------------------------------------------------------------------------------------------------------- >> result.txt
rem s��ʹ����֤
echo  testValSmaUse: >> result.txt
curl "http://smasit.cnsuning.com/sma/test/testSmaVal.do?appCode=%%h&recordCode=%%d&templateId=%%b&useNum=%%m&userId=%%a" >> result.txt
ping -n 2 127.1 > nul		rem �ȴ�2���ٵ�����һ������
echo. >> result.txt			
echo --------------------------------------------------------------------------------------------------------------- >> result.txt
rem s��ʹ��
echo. >> result.txt
echo Use Sma: >> result.txt
curl "http://smasit.cnsuning.com/sma/test/testSmaUse.do?channelId=%%n&appCode=%%h&recordCode=%%d&templateId=%%b&userId=%%a&activityCode=%%i" >> result.txt
ping -n 2 127.1 > nul
echo. >> result.txt
echo --------------------------------------------------------------------------------------------------------------- >> result.txt
REM ��ѯs��
echo. >> result.txt
echo  Query Sma: >> result.txt
curl "http://smasit.cnsuning.com/sma/test/testQuerySma.do?appCode=%%h&userId=%%a&templateId=%%b" >> result.txt
ping -n 2 127.1 > nul
echo. >> result.txt
echo --------------------------------------------------------------------------------------------------------------- >> result.txt
set /a iteration=iteration+1		rem ����������
)
echo "Finish,press any key to exit!"&pause>nul
start /max result.txt

goto zhushi

rem ��������
echo. >> result.txt
echo Lock sma: >> result.txt
curl "http://smasit.cnsuning.com/sma/sma/test/LockingSma.htm?userId=%%a&templateId=%%b&phoneNum=%%c&recordCode=%%d&orderId=%%f&appCode=sma&orderChildId=%%g&activityCode=%%i&activityName=%%j&productId=%%k&productName=%%l" >> result.txt
ping -n 2 127.1 > nul
echo. >> result.txt
echo --------------------------------------------------------------------------------------------------------------- >> result.txt

rem ȡ������
echo. >> result.txt
echo Unlock sma: >> result.txt
curl "http://smasit.cnsuning.com/sma/sma/test/testUnLockingSma.htm?userId=%%a&templateId=%%b&recordCode=%%d&orderId=%%f" >> result.txt
ping -n 2 127.1 > nul
echo. >> result.txt
echo --------------------------------------------------------------------------------------------------------------- >> result.txt

:zhushi