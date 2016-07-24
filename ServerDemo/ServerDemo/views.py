# -*- coding: utf-8 -*-
from django.shortcuts import render


import sys
reload(sys)
sys.setdefaultencoding('utf8')


from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from wechat_sdk import WechatConf
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import (TextMessage,VoiceMessage,ImageMessage,VideoMessage,LocationMessage)

import MySQLdb



def LogMsg(userID,strMsg):
	print "***************Log Msg"
	print userID 
	print strMsg
	strInsertMsg = str(strMsg).decode('utf8')
	
	db = MySQLdb.connect("localhost","root","dennis","WeChat")

	cursor = db.cursor()
	sql = "INSERT INTO WeChatLog(userID,msg,Time) VALUES('%s','%s',now());" % (userID,strInsertMsg)
    
	try:
		print sql
		cursor.execute(sql)
		db.commit()
	
	except:
		print "Error: unable to fecth data"
	
	cursor.close()
	db.close()
	return 
    

def AddUser(userID):
    db = MySQLdb.connect("localhost","root","dennis","WeChat")
    cursor = db.cursor()
    sql1 = "SELECT * FROM User_Info WHERE userId like \"%s\" " % userID
    try:
        cursor.execute(sql1)
        results = cursor.fetchall()
        if (len(results) == 0):
            sql = "INSERT INTO User_Info(userId,isLogin,isChat,name) VALUES('%s',0,0,'nobody')" % userID
            cursor.execute(sql)
            db.commit()
        else:
            print "Get Result"
            print(results)
    except:
        print "Error: unable to fecth data"
    
    cursor.close()
    db.close()
	
    return 


def Login(userID):
    db = MySQLdb.connect("localhost","root","dennis","WeChat")
    cursor = db.cursor()
    sql = "UPDATE User_Info SET isLogin = 1 WHERE userID like \"%s\" " % userID
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()


    cursor.close()
    db.close()

def LogOut(userID):
    print userID
    db = MySQLdb.connect("localhost","root","dennis","WeChat")
    cursor = db.cursor()
    OffChat(userID)
    pairID = GetPair(userID)
    print pairID 
    OffChat(pairID)
    sql = "UPDATE User_Info SET isLogin = 0 WHERE userID like \"%s\" " % userID
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()


    cursor.close()
    db.close()

def OnChat(userID):
    db = MySQLdb.connect("localhost","root","dennis","WeChat")
    cursor = db.cursor()
    sql = "UPDATE User_Info SET isChat = 1 WHERE userID like \"%s\" " % userID
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()


    cursor.close()
    db.close()




def OffChat(userID):

    print "Off Chat"
    print userID
    db = MySQLdb.connect("localhost","root","dennis","WeChat")
    cursor = db.cursor()
    sql = "UPDATE User_Info SET isChat = 0 WHERE userID like \"%s\" " % userID
    print sql
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

	sql1="UPDATE  ChatPair SET status = 1 WHERE FromID like \"%s\" " % userID
	print sql1
    try:
        cursor.execute(sql1)
        db.commit()
    except:
        db.rollback()

	sql2="UPDATE ChatPair SET status = 1  WHERE ToID  like \"%s\" " % userID
	print sql2
    try:
        cursor.execute(sql2)
        db.commit()
    except:
        db.rollback()
	
	db.commit()
    cursor.close()
    db.close()
	

def IsLogin(userID):
    db = MySQLdb.connect("localhost","root","dennis","WeChat")
    cursor = db.cursor()
    sql = "SELECT * FROM User_Info WHERE isLogin = 1 AND userID like \"%s\" " % userID
    bLogIn= False
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        if (len(results) == 0):
            bLogIn = False
        else:
            bLogIn = True
    except:
        print "SQL ERROR "
        print sql
	
	cursor.close()
	db.close()

    return bLogIn

            

def IsChat(userID):
    db = MySQLdb.connect("localhost","root","dennis","WeChat")
    cursor = db.cursor()
    sql = "SELECT * FROM User_Info WHERE isChat = 1 AND userID like \"%s\" " % userID
    bLogIn= False
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        if (len(results) == 0):
            bLogIn = False
        else:
            bLogIn = True
    except:
        print "SQL ERROR "
        print sql
	
    cursor.close()
    db.close()
    return bLogIn

def SetPair(userID):
	if not IsLogin(userID):
		return ""
	if IsChat(userID):
		return ""
	db = MySQLdb.connect("localhost","root","dennis","WeChat")
	cursor = db.cursor()
	sql="SELECT * FROM User_Info WHERE isLogin=1 AND isChat = 0 AND userId not like \"%s\" " % userID
	pairID=""
	try:
		cursor.execute(sql)
		print sql
		results = cursor.fetchall()
		if (len(results) != 0):
			pairID = results[0][1]
			print "***********RESULTs*******************"
			print pairID
			print userID
			print "*****************************"
			OnChat(userID)
			OnChat(pairID)
			sql="UPDATE User_Info SET isChat = 1 WHERE userId like \"%s\" "%userID
			try:
				cursor.execute(sql)
				db.commit()
			except:
				db.rollback()
			
			sql="UPDATE User_Info SET isChat = 1 WHERE userId like \"%s\" "%pairID
			try:
				cursor.execute(sql)
				db.commit()
			except:
				db.rollback()
				
			sql="INSERT INTO ChatPair(FromID,ToID) VALUES('%s','%s')"%(userID,pairID)
			try:
				cursor.execute(sql)
				db.commit()
			except:
				db.rollback()

			sql="INSERT INTO ChatPair(FromID,ToID) VALUES('%s','%s')"%(pairID,userID)
			try:
				cursor.execute(sql)
				db.commit()
			except:
				db.rollback()
		else:
			print "*********************************"
			pairID = ""
			print pairID
			print "*********************************"
	except:
		print "SQL ERROR "
		print sql
    
	cursor.close()
	db.close()
	return 
     

def GetPair(userID):
    if IsLogin(userID):
		pass

    if IsChat(userID):
		pass


    db = MySQLdb.connect("localhost","root","dennis","WeChat")
    cursor = db.cursor()
    sql="SELECT * FROM ChatPair WHERE FromID like \"%s\" AND status = 0 " % userID

    toID=""
    try:
        cursor.execute(sql)
        results = cursor.fetchone()
        if (len(results) != 0):
            toID = results[2]
        else:
            toID = ""
            print toID
    except:
        print "SQL ERROR "
        print sql
    cursor.close()
    db.close()
    return toID
     

def PutMessageToQueue(toID,msg):
    db = MySQLdb.connect("localhost","root","dennis","WeChat")
    cursor = db.cursor()
    sql="INSERT INTO Message(ReceiveID,msg,isSend,FromSenderTime) VALUES('%s','%s',0,now());" %(toID,msg)
    try:
        print sql
        cursor.execute(sql)
        db.commit()
    except:
        print "PutMessage To QueueFailed"
        print sql
        db.rollback() 

    cursor.close()
    db.close()


def SendMessage(userID,msg):
    toID = GetPair(userID)
    if (len(toID) > 2):
        PutMessageToQueue(toID,msg)
    else:
        print "No Chat"

    return



def GetMessage(userID):
    db = MySQLdb.connect("localhost","root","dennis","WeChat")
    cursor = db.cursor()
    sql="SELECT * FROM Message WHERE ReceiveID like \"%s\" AND isSend = 0" % userID 


    strMsg=""
    try:
        print sql
        cursor.execute(sql)
        results = cursor.fetchall()

        print results
        cursor.execute(sql)
        for elem in results:
            strMsg += elem[2]
            strMsg += "\n"

        print strMsg
        sql="UPDATE Message SET isSend=1,ToReceiverTime=now() WHERE isSend=0 AND ReceiveID like \"%s\" " % userID
        try:
            print sql
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
    except:
        print "SQL ERROR"
        print sql


    cursor.close()
    db.close()
	
	
    return strMsg 



def ParserMsg(strMsgOrg,userID):
	LogMsg(userID,strMsgOrg)
	print(userID)
	AddUser(userID)
	strMsg = str(strMsgOrg).encode('utf8')
	strResult=U""
	if (IsLogin(userID)):
		print "***********Parse Msg***********************"
		print strMsg
		print "***********Parse Msg**********************"

		if (strMsg == "0102"):
			LogOut(userID)
			strResult =U"服务器:您已成功退出登陆"
			return strResult

		SendMessage(userID,strMsgOrg)
		if (IsChat(userID)):
			strResultMsg = GetMessage(userID)
			if (len(strResultMsg) == 0):
				strResult=U"服务器:对方还没有给您发消息，不要着急哦"
			else:
				strResult= U"您的朋友:"+strResultMsg
		
		return  strResult
	else:
		Login(userID)
		SetPair(userID)
		"""strResult=U"服务器：本公众号是一个匿名聊天软件,可以与陌生人一对一的聊天，\n \
			    1,输入任意字符登陆
				2,登陆状态下,输入0102退出登陆\n \
				2,登陆以后，系统会自动为你查找陌生人，如果你想退出聊天,请输入0102\n\
				3,本公众号目前处于开发状态，有可能会有信息延迟或者不稳定的情况,希望大家不要着急\n\
				4,为了保证您的安全，请不要将个人信息透露给陌生人\n\
				6,未登录状态下，发送消息，将会回复本提示 \n\
				\n \
				服务器:系统正在为您查找朋友，请不要着急哦"""

		strResult=U"服务器：本公众号是一个匿名聊天软件,可以与陌生人一对一的聊天，\n \
			    1,输入任意字符登陆,聊天对象随机分配\n\
				2,登陆状态下,输入0102退出登陆\n \
				\n \
				服务器:系统正在为您查找朋友，请不要着急哦"

	
	return strResult





#Test api 
def LogMsgTest(userID,strMsg):
	print "***************Log Msg"
	print userID 
	print strMsg
	strInsertMsg = str(strMsg).encode('utf8')
	
	db = MySQLdb.connect("localhost","root","dennis","WeChatTest")

	cursor = db.cursor()

	sql = "INSERT INTO TABLE WeChatLog(userID,Time) VALUES('%s',now());" % str(userID).encode('utf8')
    
	try:
		print sql
		cursor.execute(sql)
		db.commit()
	
	except:
		print "Error: unable to fecth data"
	
	cursor.close()
	db.close()
	return 
    

def AddUserTest(userID):
    db = MySQLdb.connect("localhost","root","dennis","WeChatTest")
    cursor = db.cursor()
    sql1 = "SELECT * FROM User_Info WHERE userId like \"%s\" " % userID
    try:
        cursor.execute(sql1)
        results = cursor.fetchall()
        if (len(results) == 0):
            sql = "INSERT INTO User_Info(userId,isLogin,isChat,name) VALUES('%s',0,0,'nobody')" % userID
            cursor.execute(sql)
            db.commit()
        else:
            print "Get Result"
            print(results)
    except:
        print "Error: unable to fecth data"
    
    cursor.close()
    db.close()
	
    return 


def LoginTest(userID):
    db = MySQLdb.connect("localhost","root","dennis","WeChatTest")
    cursor = db.cursor()
    sql = "UPDATE User_Info SET isLogin = 1 WHERE userID like \"%s\" " % userID
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()


    cursor.close()
    db.close()

def LogOutTest(userID):
    print userID
    db = MySQLdb.connect("localhost","root","dennis","WeChatTest")
    cursor = db.cursor()
    OffChatTest(userID)
    pairID = GetPairTest(userID)
    print pairID 
    OffChatTest(pairID)
    sql = "UPDATE User_Info SET isLogin = 0 WHERE userID like \"%s\" " % userID
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()


    cursor.close()
    db.close()

def OnChatTest(userID):
    db = MySQLdb.connect("localhost","root","dennis","WeChatTest")
    cursor = db.cursor()
    sql = "UPDATE User_Info SET isChat = 1 WHERE userID like \"%s\" " % userID
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()


    cursor.close()
    db.close()



def OffChatTest(userID):

    print "Off Chat"
    print userID
    db = MySQLdb.connect("localhost","root","dennis","WeChatTest")
    cursor = db.cursor()
    sql = "UPDATE User_Info SET isChat = 0 WHERE userID like \"%s\" " % userID
    print sql
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

	sql1="UPDATE  ChatPair SET status = 1 WHERE FromID like \"%s\" " % userID
	print sql1
    try:
        cursor.execute(sql1)
        db.commit()
    except:
        db.rollback()

	sql2="UPDATE ChatPair SET status = 1  WHERE ToID  like \"%s\" " % userID
	print sql2
    try:
        cursor.execute(sql2)
        db.commit()
    except:
        db.rollback()
	
	db.commit()
    cursor.close()
    db.close()
	

def IsLoginTest(userID):
    db = MySQLdb.connect("localhost","root","dennis","WeChatTest")
    cursor = db.cursor()
    sql = "SELECT * FROM User_Info WHERE isLogin = 1 AND userID like \"%s\" " % userID
    bLogIn= False
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        if (len(results) == 0):
            bLogIn = False
        else:
            bLogIn = True
    except:
        print "SQL ERROR "
        print sql
	
	cursor.close()
	db.close()

    return bLogIn

            


def NotScoredTest(userID):
    db = MySQLdb.connect("localhost","root","dennis","WeChatTest")
    cursor = db.cursor()
    sql = "SELECT * FROM ChatPair WHERE isScored = 0 AND FromID like \"%s\" " % userID
    bLogIn= False
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        if (len(results) == 0):
            bLogIn = False
        else:
            bLogIn = True
    except:
        print "SQL ERROR "
        print sql
	
    cursor.close()
    db.close()
    return bLogIn

def IsScoreCode(strMsg):
	if(strMsg=='0'):
		return True
	elif (strMsg=='1'):
		return True
	elif (strMsg=='2'):
		return True
	elif (strMsg=='3'):
		return True

def IsQuitChatCode(strMsg):
	if (strMsg=='0102'):
		return True
	else:
		return False


def IsScoredTest(userID):
    db = MySQLdb.connect("localhost","root","dennis","WeChatTest")
    cursor = db.cursor()
    sql = "SELECT * FROM User_Info WHERE isScored = 1 AND userID like \"%s\" " % userID
    bLogIn= False
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        if (len(results) == 0):
            bLogIn = False
        else:
            bLogIn = True
    except:
        print "SQL ERROR "
        print sql
	
    cursor.close()
    db.close()
    return bLogIn

def IsChatTest(userID):
    db = MySQLdb.connect("localhost","root","dennis","WeChatTest")
    cursor = db.cursor()
    sql = "SELECT * FROM User_Info WHERE isChat = 1 AND userID like \"%s\" " % userID
    bLogIn= False
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        if (len(results) == 0):
            bLogIn = False
        else:
            bLogIn = True
    except:
        print "SQL ERROR "
        print sql
	
    cursor.close()
    db.close()
    return bLogIn

def SetScoredTest(userID):
	if not IsLoginTest(userID):
		return ""
	if IsChatTest(userID):
		return ""
	db = MySQLdb.connect("localhost","root","dennis","WeChatTest")
	cursor = db.cursor()
	sql="SELECT * FROM User_Info WHERE isLogin=1 AND isChat = 0 AND userId not like \"%s\" " % userID
	pairID=""
	try:
		cursor.execute(sql)
		print sql
		results = cursor.fetchall()
		if (len(results) != 0):
			pairID = results[0][1]
			print "***********RESULTs*******************"
			print pairID
			print userID
			print "*****************************"
			OnChatTest(userID)
			OnChatTest(pairID)
			sql="UPDATE User_Info SET isChat = 1 WHERE userId like \"%s\" "%userID
			try:
				cursor.execute(sql)
				db.commit()
			except:
				db.rollback()
			
			sql="UPDATE User_Info SET isChat = 1 WHERE userId like \"%s\" "%pairID
			try:
				cursor.execute(sql)
				db.commit()
			except:
				db.rollback()
				
			sql="INSERT INTO ChatPair(FromID,ToID) VALUES('%s','%s')"%(userID,pairID)
			try:
				cursor.execute(sql)
				db.commit()
			except:
				db.rollback()

			sql="INSERT INTO ChatPair(FromID,ToID) VALUES('%s','%s')"%(pairID,userID)
			try:
				cursor.execute(sql)
				db.commit()
			except:
				db.rollback()
		else:
			print "*********************************"
			pairID = ""
			print pairID
			print "*********************************"
	except:
		print "SQL ERROR "
		print sql
    
	cursor.close()
	db.close()
	return 

def SetPairTest(userID):
	if not IsLoginTest(userID):
		return ""
	if IsChatTest(userID):
		return ""
	db = MySQLdb.connect("localhost","root","dennis","WeChatTest")
	cursor = db.cursor()
	sql="SELECT * FROM User_Info WHERE isLogin=1 AND isChat = 0 AND userId not like \"%s\" " % userID
	pairID=""
	try:
		cursor.execute(sql)
		print sql
		results = cursor.fetchall()
		if (len(results) != 0):
			pairID = results[0][1]
			print "***********RESULTs*******************"
			print pairID
			print userID
			print "*****************************"
			OnChatTest(userID)
			OnChatTest(pairID)
			sql="UPDATE User_Info SET isChat = 1 WHERE userId like \"%s\" "%userID
			try:
				cursor.execute(sql)
				db.commit()
			except:
				db.rollback()
			
			sql="UPDATE User_Info SET isChat = 1 WHERE userId like \"%s\" "%pairID
			try:
				cursor.execute(sql)
				db.commit()
			except:
				db.rollback()
				
			sql="INSERT INTO ChatPair(FromID,ToID) VALUES('%s','%s')"%(userID,pairID)
			try:
				cursor.execute(sql)
				db.commit()
			except:
				db.rollback()

			sql="INSERT INTO ChatPair(FromID,ToID) VALUES('%s','%s')"%(pairID,userID)
			try:
				cursor.execute(sql)
				db.commit()
			except:
				db.rollback()
		else:
			print "*********************************"
			pairID = ""
			print pairID
			print "*********************************"
	except:
		print "SQL ERROR "
		print sql
    
	cursor.close()
	db.close()
	return 
     

def GetPairTest(userID):
    if IsLoginTest(userID):
		pass

    if IsChatTest(userID):
		pass


    db = MySQLdb.connect("localhost","root","dennis","WeChat")
    cursor = db.cursor()
    sql="SELECT * FROM ChatPair WHERE FromID like \"%s\" AND status = 0 " % userID

    toID=""
    try:
        cursor.execute(sql)
        results = cursor.fetchone()
        if (len(results) != 0):
            toID = results[2]
        else:
            toID = ""
            print toID
    except:
        print "SQL ERROR "
        print sql
    cursor.close()
    db.close()
    return toID
     

def PutMessageToQueueTest(toID,msg):
    db = MySQLdb.connect("localhost","root","dennis","WeChatTest")
    cursor = db.cursor()
    sql="INSERT INTO Message(ReceiveID,msg,isSend,FromSenderTime) VALUES('%s','%s',0,now());" %(toID,msg)
    try:
        print sql
        cursor.execute(sql)
        db.commit()
    except:
        print "PutMessage To QueueFailed"
        print sql
        db.rollback() 

    cursor.close()
    db.close()


def SendMessageTest(userID,msg):
    toID = GetPairTest(userID)
    if (len(toID) > 2):
        PutMessageToQueueTest(toID,msg)
    else:
        print "No Chat"

    return



def GetMessageTest(userID):
    db = MySQLdb.connect("localhost","root","dennis","WeChatTest")
    cursor = db.cursor()
    sql="SELECT * FROM Message WHERE ReceiveID like \"%s\" AND isSend = 0" % userID 


    strMsg=""
    try:
        print sql
        cursor.execute(sql)
        results = cursor.fetchall()

        print results
        cursor.execute(sql)
        for elem in results:
            strMsg += elem[2]
            strMsg += "\n"

        print strMsg
        sql="UPDATE Message SET isSend=1,ToReceiverTime=now() WHERE isSend=0 AND ReceiveID like \"%s\" " % userID
        try:
            print sql
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
    except:
        print "SQL ERROR"
        print sql


    cursor.close()
    db.close()
	
	
    return strMsg 


def UpdateUserLocation(userID,longitude,lantitude,city):
    print "Update User Location "
    print userID
    print longitude
    print lantitude
    print city
    db = MySQLdb.connect("localhost","root","dennis","WeChatTest")
    cursor = db.cursor()
    sql1 = "SELECT * FROM User WHERE userId like \"%s\" ;" % userID
    print sql1
    try:
        cursor.execute(sql1)
        results = cursor.fetchall()
        if (len(results) == 0):
            sql = "INSERT INTO User(userId,longitude,lantitude,city) VALUES(\"%s\",10.25,10.25,'%s')" % (userID,city)
            cursor.execute(sql)
            print sql
            db.commit()
        else:
            print "Get Result"
            print(results)
    except:
        print "Error: unable to fecth data"
    
    cursor.close()
    db.close()
	
    return 
#判断用户是否在聊天
def IsUserOnChatNow(userID):
	if (IsLoginTest(userID) and IsChatTest(userID)):
		if (IsScoredTest(userID)):
			return True
		else:
			return False

	else:
		return False

#是否有用户未匹配

def ParserMsgTest(strMsgOrg,userID):
	LogMsgTest(userID,strMsgOrg)
	AddUserTest(userID)
	if(IsUserOnChatNow(userID)):
		LoginTest(userID)
		pass
	else:
		pass

	strMsg = str(strMsgOrg).encode('utf8')
	strResult=U""
	if (IsLoginTest(userID)):
		print "***********Parse Msg***********************"
		print strMsg
		print "***********Parse Msg**********************"

		if (strMsg == "0102"):
			LogOutTest(userID)
			strResult =U"服务器:您已成功退出登陆"
			return strResult

		SendMessageTest(userID,strMsgOrg)
		if (IsChatTest(userID)):
			strResultMsg = GetMessageTest(userID)
			if (len(strResultMsg) == 0):
				strResult=U"服务器:对方还没有给您发消息，不要着急哦"
			else:
				strResult= U"您的朋友:"+strResultMsg
		
		return  strResult
	else:
		LoginTest(userID)
		SetPairTest(userID)
		"""strResult=U"服务器：本公众号是一个匿名聊天软件,可以与陌生人一对一的聊天，\n \
			    1,输入任意字符登陆
				2,登陆状态下,输入0102退出登陆\n \
				2,登陆以后，系统会自动为你查找陌生人，如果你想退出聊天,请输入0102\n\
				3,本公众号目前处于开发状态，有可能会有信息延迟或者不稳定的情况,希望大家不要着急\n\
				4,为了保证您的安全，请不要将个人信息透露给陌生人\n\
				6,未登录状态下，发送消息，将会回复本提示 \n\
				\n \
				服务器:系统正在为您查找朋友，请不要着急哦"""

		strResult=U"服务器：本公众号是一个匿名聊天软件,可以与陌生人一对一的聊天，\n \
			    1,输入任意字符登陆,聊天对象随机分配\n\
				2,登陆状态下,输入0102退出登陆\n \
				\n \
				服务器:系统正在为您查找朋友，请不要着急哦"

	
	return strResult

# Create your views here.

MyConf=WechatConf(
		token='dennismi1024gmail',
		appid='wxc86a795a9cb7a1e4',
		appsecret='8a952ff560c18ededefb568a779129d6',
		encrypt_mode='YOUR_MODE',
		encoding_aes_key='oTrKxpp2S3RwB090SDnoVaiFRIADIGHBhOF4B7ZkcBJ',
		)

ChatForFunConf=WechatConf(
		token='dennismi1024gmail',
		appid='wxcb80882bbbbe9c80',
		appsecret='9fb82f088d37f072daacbd156fcc7b24',
		encrypt_mode='YOUR_MODE',
		encoding_aes_key='fQZM0PHIlIviBBq8cd9al4KRBysNz0T5a5D6VagoEo0',
		)

# Create your views here.


def wechat_home(request):
	print("Get Message")
	signature=request.GET.get('signature')
	timestamp=request.GET.get('timestamp')
	nonce = request.GET.get('nonce')
	wechat_instance = WechatBasic(conf=MyConf)
	reply_text=""
	if not wechat_instance.check_signature(signature=signature,timestamp=timestamp,nonce=nonce):
		return HttpResponseBadRequest('Verify Failed')
	else:
		if request.method == 'GET':
			response = request.GET.get('echostr','error')
		else:
			try:
				wechat_instance.parse_data(request.body)
				message = wechat_instance.get_message()
				if isinstance(message,TextMessage):
					reply_text=str(message.content).encode('utf8')
					reply_text=ParserMsgTest(reply_text,message.source)
				elif isinstance(message,ImageMessage):
					reply_text=str(message.picurl).encode('utf8')
					reply_text=ParserMsgTest(reply_text,message.source)
				elif isinstance(message,LocationMessage):
					print "********Location **********************"
					print message.location
					print message.label

					print "********Location **********************"
					reply_text=str(message.label).encode('utf8')
					UpdateUserLocation(message.source,message.location[1],message.location[0],message.label)
					reply_text=ParserMsgTest(reply_text,message.source)
				else:
					reply_text=U"服务器:目前只支持文字消息,非常抱歉"	

				response = wechat_instance.response_text(content=reply_text)
			except ParseError:
				return HttpResponseBadRequest("Invalid XML Data")
		return HttpResponse(response,content_type='application/xml')

def wechatChatForFun(request):
	print("Get Message")
	signature=request.GET.get('signature')
	timestamp=request.GET.get('timestamp')
	nonce = request.GET.get('nonce')
	wechat_instance = WechatBasic(conf=ChatForFunConf)
	reply_text=""
	if not wechat_instance.check_signature(signature=signature,timestamp=timestamp,nonce=nonce):
		return HttpResponseBadRequest('Verify Failed')
	else:
		if request.method == 'GET':
			response = request.GET.get('echostr','error')
		else:
			try:
				wechat_instance.parse_data(request.body)
				message = wechat_instance.get_message()
				if isinstance(message,TextMessage):
					reply_text=str(message.content).encode('utf8')
					reply_text=ParserMsg(reply_text,message.source)
				elif isinstance(message,ImageMessage):
					reply_text=str(message.picurl).encode('utf8')
					reply_text=ParserMsg(reply_text,message.source)
				elif isinstance(message,LocationMessage):
					reply_text=str(message.label).encode('utf8')
					reply_text=ParserMsg(reply_text,message.source)
				else:
					reply_text=U"服务器:目前只支持文字消息,非常抱歉"	

				response = wechat_instance.response_text(content=reply_text)
			except ParseError:
				return HttpResponseBadRequest("Invalid XML Data")
		return HttpResponse(response,content_type='application/xml')

