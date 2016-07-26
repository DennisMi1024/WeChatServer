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
from wechat_sdk.messages import (
    TextMessage,
    VoiceMessage,
    ImageMessage,
    VideoMessage,
    LocationMessage)

import MySQLdb


def GetQiuShiBaiKeMsg():
    db = MySQLdb.connect("localhost", "root", "dennis", "WeChat")
    cursor = db.cursor()
    sql1 = "SELECT * FROM QiuShiBaiKe ORDER BY count"
    strResult = U""
    try:
        cursor.execute(sql1)
        results = cursor.fetchone()
        if (len(results) != 0):
            # print results
            strResult = str(results[1])

        try:
            sql2 = "UPDATE QiuShiBaiKe SET count = count+1 WHERE id = %s" % results[
                0]
            cursor.execute(sql2)
            db.commit()
        except:
            db.rollback()

    except:
        pass

    cursor.close()
    db.close()

    return strResult


def LogMsg(userID, strMsg):
    strInsertMsg = str(strMsg).decode('utf8')

    db = MySQLdb.connect("localhost", "root", "dennis", "WeChat")

    cursor = db.cursor()
    sql = "INSERT INTO WeChatLog(userID,msg,Time) VALUES('%s','%s',now());" % (
        userID, strInsertMsg)

    try:
        cursor.execute(sql)
        db.commit()

    except:
        pass

    cursor.close()
    db.close()
    return


def AddUser(userID):
    db = MySQLdb.connect("localhost", "root", "dennis", "WeChat")
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
            print(results)
    except:
        pass 

    cursor.close()
    db.close()

    return


def Login(userID):
    db = MySQLdb.connect("localhost", "root", "dennis", "WeChat")
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
    db = MySQLdb.connect("localhost", "root", "dennis", "WeChat")
    cursor = db.cursor()
    OffChat(userID)
    pairID = GetPair(userID)
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
    db = MySQLdb.connect("localhost", "root", "dennis", "WeChat")
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

    db = MySQLdb.connect("localhost", "root", "dennis", "WeChat")
    cursor = db.cursor()
    sql = "UPDATE User_Info SET isChat = 0 WHERE userID like \"%s\" " % userID
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

        sql1 = "UPDATE  ChatPair SET status = 1 WHERE FromID like \"%s\" " % userID
        print sql1
    try:
        cursor.execute(sql1)
        db.commit()
    except:
        db.rollback()

        sql2 = "UPDATE ChatPair SET status = 1  WHERE ToID  like \"%s\" " % userID
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
    db = MySQLdb.connect("localhost", "root", "dennis", "WeChat")
    cursor = db.cursor()
    sql = "SELECT * FROM User_Info WHERE isLogin = 1 AND userID like \"%s\" " % userID
    bLogIn = False
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
    db = MySQLdb.connect("localhost", "root", "dennis", "WeChat")
    cursor = db.cursor()
    sql = "SELECT * FROM User_Info WHERE isChat = 1 AND userID like \"%s\" " % userID
    bLogIn = False
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
    db = MySQLdb.connect("localhost", "root", "dennis", "WeChat")
    cursor = db.cursor()
    sql = "SELECT * FROM User_Info WHERE isLogin=1 AND isChat = 0 AND userId not like \"%s\" " % userID
    pairID = ""
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
            sql = "UPDATE User_Info SET isChat = 1 WHERE userId like \"%s\" " % userID
            try:
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()

            sql = "UPDATE User_Info SET isChat = 1 WHERE userId like \"%s\" " % pairID
            try:
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()

            sql = "INSERT INTO ChatPair(FromID,ToID) VALUES('%s','%s')" % (
                userID, pairID)
            try:
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()

            sql = "INSERT INTO ChatPair(FromID,ToID) VALUES('%s','%s')" % (
                pairID, userID)
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

    db = MySQLdb.connect("localhost", "root", "dennis", "WeChat")
    cursor = db.cursor()
    sql = "SELECT * FROM ChatPair WHERE FromID like \"%s\" AND status = 0 " % userID

    toID = ""
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


def PutMessageToQueue(toID, msg):
    db = MySQLdb.connect("localhost", "root", "dennis", "WeChat")
    cursor = db.cursor()
    sql = "INSERT INTO Message(ReceiveID,msg,isSend,FromSenderTime) VALUES('%s','%s',0,now());" % (
        toID, msg)
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


def SendMessage(userID, msg):
    toID = GetPair(userID)
    if (len(toID) > 2):
        PutMessageToQueue(toID, msg)
    else:
        print "No Chat"

    return


def GetMessage(userID):
    db = MySQLdb.connect("localhost", "root", "dennis", "WeChat")
    cursor = db.cursor()
    sql = "SELECT * FROM Message WHERE ReceiveID like \"%s\" AND isSend = 0" % userID

    strMsg = ""
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
        sql = "UPDATE Message SET isSend=1,ToReceiverTime=now() WHERE isSend=0 AND ReceiveID like \"%s\" " % userID
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


def ParserMsgOld(strMsgOrg, userID):
    LogMsg(userID, strMsgOrg)
    print(userID)
    AddUser(userID)
    strMsg = str(strMsgOrg).encode('utf8')
    strResult = U""
    if (IsLogin(userID)):
        print "***********Parse Msg***********************"
        print strMsg
        print "***********Parse Msg**********************"

        if (strMsg == "0102"):
            LogOut(userID)
            strResult = U"服务器:您已成功退出登陆"
            return strResult

        SendMessage(userID, strMsgOrg)
        if (IsChat(userID)):
            strResultMsg = GetMessage(userID)
            if (len(strResultMsg) == 0):
                strQSBK = GetQiuShiBaiKeMsg()
                strResult = U"服务器:" + strQSBK
            else:
                strResult = U"您的朋友:" + strResultMsg

        else:
            strQSBK = GetQiuShiBaiKeMsg()
            strResult = U"服务器:" + strQSBK

        return strResult
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

        strResult = U"服务器：本公众号是一个匿名聊天软件,可以与陌生人一对一的聊天，\n \
			    1,输入任意字符登陆,聊天对象随机分配\n\
				2,登陆状态下,输入0102退出登陆\n \
				\n \
				服务器:系统正在为您查找朋友，请不要着急哦"

    return strResult


# Test api
def LogMsgTest(userID, strMsg):
    print "***************Log Msg"
    print userID
    print strMsg
    strInsertMsg = str(strMsg).encode('utf8')

    db = MySQLdb.connect("localhost", "root", "dennis", "WeChatTest")

    cursor = db.cursor()

    sql = "INSERT INTO TABLE WeChatLog(userID,Time) VALUES('%s',now());" % str(
        userID).encode('utf8')

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
    db = MySQLdb.connect("localhost", "root", "dennis", "WeChatTest")
    cursor = db.cursor()
    sql1 = "SELECT * FROM User_Info WHERE userId like \"%s\" " % userID
    try:
        cursor.execute(sql1)
        results = cursor.fetchall()
        if (len(results) == 0):
            sql = "INSERT INTO User_Info(userId,isLogin,isChat,name,isScored) VALUES('%s',0,0,'nobody',1)" % userID
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
    db = MySQLdb.connect("localhost", "root", "dennis", "WeChatTest")
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
    db = MySQLdb.connect("localhost", "root", "dennis", "WeChatTest")
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
    db = MySQLdb.connect("localhost", "root", "dennis", "WeChatTest")
    cursor = db.cursor()
    sql = "UPDATE User_Info SET isChat = 1 WHERE userID like \"%s\" " % userID
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

    cursor.close()
    db.close()


def SetScorePairChatTest(userID):
    db = MySQLdb.connect("localhost", "root", "dennis", "WeChatTest")
    cursor = db.cursor()
    sql1 = "UPDATE  ChatPair SET status = 2 WHERE FromID like \"%s\" " % userID
    try:
        cursor.execute(sql1)
        db.commit()
    except:
        db.rollback()

        db.commit()
    cursor.close()
    db.close()


def UnChatPairChatTest(userID):
    db = MySQLdb.connect("localhost", "root", "dennis", "WeChatTest")
    cursor = db.cursor()
    sql1 = "UPDATE  ChatPair SET status = 1 WHERE FromID like \"%s\" " % userID
    try:
        cursor.execute(sql1)
        db.commit()
    except:
        db.rollback()

        db.commit()
    cursor.close()
    db.close()


def OffChatTest(userID):
    db = MySQLdb.connect("localhost", "root", "dennis", "WeChatTest")
    cursor = db.cursor()
    sql = "UPDATE User_Info SET isChat = 0 WHERE userID like \"%s\" " % userID
    print sql
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

        db.commit()
    cursor.close()
    db.close()


def IsLoginTest(userID):
    db = MySQLdb.connect("localhost", "root", "dennis", "WeChatTest")
    cursor = db.cursor()
    sql = "SELECT * FROM User_Info WHERE isLogin = 1 AND userID like \"%s\" " % userID
    bLogIn = False
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


def SetUserScored(userID):
    db = MySQLdb.connect("localhost", "root", "dennis", "WeChatTest")
    cursor = db.cursor()
    sql = "UPDATE  User_Info SET isScored = 1 WHERE userID like \"%s\" " % userID
    bLogIn = False
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print "SQL ERROR "
        print sql

    cursor.close()
    db.close()
    return bLogIn


def NotScoredTest(userID):
    db = MySQLdb.connect("localhost", "root", "dennis", "WeChatTest")
    cursor = db.cursor()
    sql = "SELECT * FROM User_Info WHERE isScored = 0 AND userID like \"%s\" " % userID
    bLogIn = False
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


def IsScoreCodeTest(strMsg):
    print "************IsScore Test"
    print strMsg
    if(strMsg == '0'):
        return True
    elif (strMsg == '1'):
        return True
    elif (strMsg == '2'):
        return True
    elif (strMsg == '3'):
        return True
    elif (strMsg == '4'):
        return True
    else:
        return False


def IsQuitChatCodeTest(strMsg):
    if (strMsg == '0102'):
        return True
    else:
        return False


def IsScoredTest(userID):
    db = MySQLdb.connect("localhost", "root", "dennis", "WeChatTest")
    cursor = db.cursor()
    sql = "SELECT * FROM User_Info WHERE isScored = 1 AND userID like \"%s\" " % userID
    bLogIn = False
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
    db = MySQLdb.connect("localhost", "root", "dennis", "WeChatTest")
    cursor = db.cursor()
    sql = "SELECT * FROM User_Info WHERE isChat = 1 AND userID like \"%s\" " % userID
    bLogIn = False
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


def SetUnScoredTest(userID):
    db = MySQLdb.connect("localhost", "root", "dennis", "WeChatTest")
    cursor = db.cursor()
    sql = "UPDATE User_Info SET isScored=0  WHERE userId  like \"%s\" " % userID
    pairID = ""
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
        print sql

    cursor.close()
    db.close()
    return


def SetScoredTest(userID):
    db = MySQLdb.connect("localhost", "root", "dennis", "WeChatTest")
    cursor = db.cursor()
    sql = "UPDATE User_Info SET isScored=1  WHERE userId  like \"%s\" " % userID
    pairID = ""
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
        print sql

    cursor.close()
    db.close()
    return


def SetUnPairTest(userID):
    return


def SetPairTest(userID):
    pairSex = GetPairSex(userID)
    db = MySQLdb.connect("localhost", "root", "dennis", "WeChatTest")
    cursor = db.cursor()
    sql = "SELECT * FROM User_Info WHERE isLogin=1 AND isChat = 0 AND isScored = 1 AND sex = pairSex AND userId not like \"%s\" " % userID
    pairID = ""
    bOK = False
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
            SetUnScoredTest(pairID)
            SetUnScoredTest(userID)
            OnChatTest(userID)
            OnChatTest(pairID)
            bOK = True
            sql = "UPDATE User_Info SET isChat = 1 WHERE userId like \"%s\" " % userID
            try:
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()

            sql = "UPDATE User_Info SET isChat = 1 WHERE userId like \"%s\" " % pairID
            try:
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()

            sql = "INSERT INTO ChatPair(FromID,ToID,status) VALUES('%s','%s',0)" % (
                userID, pairID)
            try:
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()

            sql = "INSERT INTO ChatPair(FromID,ToID,status) VALUES('%s','%s',0)" % (
                pairID, userID)
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

    return bOK

def IsPairQuitTest(userID):
    db = MySQLdb.connect("localhost", "root", "dennis", "WeChatTest")
    cursor = db.cursor()
    sql = "SELECT * FROM ChatPair WHERE FromID like \"%s\" AND status = 0 " % userID

    bSelfNotQuit = False

    try:
        cursor.execute(sql)
        results = cursor.fetchone()
        if (len(results) != 0):
            bSelfNotQuit = True
        else:
            bSelfNotQuit = False
    except:
        print "SQL ERROR "
        print sql

    sql1 = "SELECT * FROM ChatPair WHERE ToID like \"%s\" AND status = 0 " % userID

    bPairQuit = False

    try:
        cursor.execute(sql1)
        results = cursor.fetchone()
        if (len(results) != 0):
            bPairQuit = True
        else:
            bPair = False
    except:
        print "SQL ERROR "
        print sql

    cursor.close()
    db.close()

    if (bSelfNotQuit and bPairQuit):
        return True
    else:
        return False

# 获得打分的对象


def GetScorePairTest(userID):
    db = MySQLdb.connect("localhost", "root", "dennis", "WeChatTest")
    cursor = db.cursor()
    sql = "SELECT * FROM ChatPair WHERE FromID like \"%s\" AND status = 2 " % userID

    toID = ""
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


def GetPairTest(userID):
    db = MySQLdb.connect("localhost", "root", "dennis", "WeChatTest")
    cursor = db.cursor()
    sql = "SELECT * FROM ChatPair WHERE FromID like \"%s\" AND status = 0 " % userID

    toID = ""
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


def PutMessageToQueueTest(toID, msg):
    db = MySQLdb.connect("localhost", "root", "dennis", "WeChatTest")
    cursor = db.cursor()
    sql = "INSERT INTO Message(ReceiveID,msg,isSend,FromSenderTime) VALUES('%s','%s',0,now());" % (
        toID, msg)
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


def SendMessageTest(userID, msg):
    toID = GetPairTest(userID)
    if (len(toID) > 2):
        PutMessageToQueueTest(toID, msg)
    else:
        print "No Chat"

    return

#获得应该匹配的聊天对象的性别
def GetPairSex(userID):
    db = MySQLdb.connect("localhost", "root", "dennis", "WeChatTest")
    cursor = db.cursor()
    sql = "SELECT sex FROM User_Info WHERE userId like \"%s\"" % userID
    strMsg = ""

    pairSex=''
    try:
        cursor.execute(sql)
        results = cursor.fetchone()
        print "Get Pair Sex  userID "
        print results
        if(str(results[0])=='1'):
            pairSex = '0'
        else:
            pairSex = '1'
    except:
        print "SQL ERROR"

    cursor.close()
    db.close()

    return pairSex

def GetPairNickName(userID):
    strResult = U"您的朋友说:\n"
    return strResult

def GetMessageTest(userID):
    db = MySQLdb.connect("localhost", "root", "dennis", "WeChatTest")
    cursor = db.cursor()
    sql = "SELECT * FROM Message WHERE ReceiveID like \"%s\" AND isSend = 0" % userID

    strMsg = ""
    try:
        cursor.execute(sql)
        results = cursor.fetchall()

        cursor.execute(sql)
        for elem in results:
            strMsg += elem[2]
            strMsg += "\n"

        sql = "UPDATE Message SET isSend=1,ToReceiverTime=now() WHERE isSend=0 AND ReceiveID like \"%s\" " % userID
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
    except:
        print "Error"

    cursor.close()
    db.close()
    strResult = U""
    if(len(strMsg) != 0):
        strResult = GetPairNickName(userID)+strMsg
    else:
        strResult = strMsg
    return strResult


#登陆聊天欢迎词
def GetLoginWelcomString():
    strResult = U"服务器:\n\n您已经成功登录,系统将会自动为您查找好友\n\n退出登陆请输入0102"
    return strResult

#退出聊天欢迎词
def GetLogoutWelcomeString():
    strResult = U"服务器:\n\n您已经成功退出登陆,感谢您的使用"
    return strResult



def UpdateUserLocation(userID, longitude, lantitude, city):
    db = MySQLdb.connect("localhost", "root", "dennis", "WeChatTest")
    cursor = db.cursor()
    sql1 = "SELECT * FROM User WHERE userId like \"%s\" ;" % userID
    try:
        cursor.execute(sql1)
        results = cursor.fetchall()
        if (len(results) == 0):
            sql = "INSERT INTO User(userId,longitude,lantitude,city) VALUES(\"%s\",10.25,10.25,'%s')" % (
                userID, city)
            cursor.execute(sql)
            db.commit()
        else:
            pass

    except:
        pass

    cursor.close()
    db.close()

    return

# 判断用户是否未打分


def IsUserNotScored(userID):
    if(IsLoginTest(userID) and NotScoredTest(userID)):
        return True
    else:
        return False

# 判断用户是否在聊天


def IsUserOnChatNow(userID):
    if (IsLoginTest(userID) and IsChatTest(userID)):
        if (IsScoredTest(userID)):
            return True
        else:
            return False

    else:
        return False


def UpdateUserScore(userID, strCode):
    db = MySQLdb.connect("localhost", "root", "dennis", "WeChatTest")
    cursor = db.cursor()
    strUpdate = U""
    if(strCode == '0'):
        strUpdate = '-5'
    elif (strCode == '1'):
        strUpdate = '-3'
    elif (strCode == '2'):
        strUpdate = '+0'
    elif (strCode == '3'):
        strUpdate = '+2'
    elif (strCode == '4'):
        strUpdate = '+4'
    else:
        strUpdate = '+0'

    sql = "UPDATE User_Info SET score=score%s WHERE userId like \"%s\" " % (
        strUpdate, userID)

    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

    cursor.close()
    db.close()
    return


def GetSetPairOKString():
    strResult = U"服务器已经为您找到聊天的朋友，您可以开始聊天了"
    return strResult


def GetScoreRequest():
    strResult = U"服务器:您已经退出聊天,请发送以下数字为对方打分\n\
			    0-----扣除对方5分\n\
				1-----扣除对方3分\n\
				2-----对方分数不变\n\
				3-----对方加2分\n\
				4-----对方加4分"

    return strResult

# 用户登陆并且聊天时进行处理


def ProcessUser_Login_Chat(userID, strMsg):
    strResult = U""
    if(IsQuitChatCodeTest(strMsg)):
        OffChatTest(userID)
        SetScorePairChatTest(userID)
        strResult = GetScoreRequest()
    else:
        SendMessageTest(userID, strMsg)
        strResult = GetMessageTest(userID)
        if (len(strResult) == 0):
            strResult = "服务器：\n"+GetQiuShiBaiKeMsg()
    return strResult


def ProcessUser_Login_NotChat(userID, strMsg):
    strResult = U""
    if(IsScoredTest(userID)):
        if (IsQuitChatCodeTest(strMsg)):
            OffChatTest(userID)
            LogOutTest(userID)
            strResult=GetLogoutWelcomeString()
        else:
            if (SetPairTest(userID)):
                strResult = GetSetPairOKString()
            else:
                strResult = "服务器:\n"+GetQiuShiBaiKeMsg() 
    else:
        if(IsScoreCodeTest(strMsg)):
            pairID = GetScorePairTest(userID)
            UpdateUserScore(pairID, strMsg)
            SetScoredTest(userID)
            OffChatTest(userID)
            LogOutTest(userID)
            strResult = U"服务器：感谢您为对方打分"
        else:
            strResult = GetScoreRequest()

    return strResult

# 用户登录时进行处理


def ProcessUser_Login(userID, strMsg):
    strResult = U""
    if(IsChatTest(userID)):
        strResult = ProcessUser_Login_Chat(userID, strMsg)
    else:
        strResult = ProcessUser_Login_NotChat(userID, strMsg)

    return strResult

# 用户未登陆后进行处理


def ProcessUser_NotLogin(userID, strMsg):
    strResult = GetLoginWelcomString()
    LoginTest(userID)
    SetPairTest(userID)

    return strResult

# 是否有用户未匹配


def IsUserSetSexTest(userID):
    db = MySQLdb.connect("localhost", "root", "dennis", "WeChatTest")
    cursor = db.cursor()
    sql = "SELECT * FROM User_Info WHERE isSexed = 1 AND userID like \"%s\" " % userID
    bLogIn = False
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        if (len(results) == 0):
            bLogIn = False
        else:
            bLogIn = True
    except:
        pass

    cursor.close()
    db.close()

    return bLogIn


def IsSexSetCodeTest(strMsg):
    if (strMsg == '0'):
        return True
    elif (strMsg == '1'):
        return True
    else:
        return False


def UpdateUserSexTest(userID, strMsg):
    db = MySQLdb.connect("localhost", "root", "dennis", "WeChatTest")
    cursor = db.cursor()
    sql = "UPDATE User_Info SET Sex=%s,isSexed=1  WHERE userId  like \"%s\" " % (strMsg, userID)
    pairID = ""
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    cursor.close()
    db.close()
    return


def GetSetSexRequestString():
    strResult = U"服务器:我还不知道你是帅哥还是美女呢,发送以下信息告诉我吧\n\
                0-----我是美女\n\
                1-----我是帅哥\n"

    return strResult


def ProcessUser_NotSetSex(userID, strMsg):
    strResult = U""
    if (IsSexSetCodeTest(strMsg)):
        UpdateUserSexTest(userID, strMsg)
        strResult = U"服务器：您已经成功设置性别，再次发送消息，即可聊天"
    else:
        strResult = GetSetSexRequestString()

    return strResult


def ProcessUser_SetSex(userID, strMsg):
    strResult = U"ProcessUser_SetTex"
    if (IsLoginTest(userID)):
        strResult = ProcessUser_Login(userID, strMsg)
    else:
        strResult = ProcessUser_NotLogin(userID, strMsg)
    return strResult


def ParserMsgTest(strMsgOrg, userID):
    LogMsgTest(userID, strMsgOrg)
    AddUserTest(userID)
    strMsg = str(strMsgOrg).encode('utf8')

    strResult = U"Test"
    if (IsUserSetSexTest(userID)):
        strResult = ProcessUser_SetSex(userID,strMsg)
    else:
        strResult = ProcessUser_NotSetSex(userID,strMsg)

    return strResult


# Create your views here.

MyConf = WechatConf(
    token='dennismi1024gmail',
    appid='wxc86a795a9cb7a1e4',
    appsecret='8a952ff560c18ededefb568a779129d6',
    encrypt_mode='YOUR_MODE',
    encoding_aes_key='oTrKxpp2S3RwB090SDnoVaiFRIADIGHBhOF4B7ZkcBJ',
)

ChatForFunConf = WechatConf(
    token='dennismi1024gmail',
    appid='wxcb80882bbbbe9c80',
    appsecret='9fb82f088d37f072daacbd156fcc7b24',
    encrypt_mode='YOUR_MODE',
    encoding_aes_key='fQZM0PHIlIviBBq8cd9al4KRBysNz0T5a5D6VagoEo0',
)

# Create your views here.


def ParserMsg(userID,strMsg):
    return ParserMsgTest(userID,strMsg)

def wechat_home(request):
    signature = request.GET.get('signature')
    timestamp = request.GET.get('timestamp')
    nonce = request.GET.get('nonce')
    wechat_instance = WechatBasic(conf=MyConf)
    reply_text = ""
    if not wechat_instance.check_signature(
            signature=signature, timestamp=timestamp, nonce=nonce):
        return HttpResponseBadRequest('Verify Failed')
    else:
        reply_text = "Test"
    response = wechat_instance.response_text(content=reply_text)
    return HttpResponse(response, content_type='application/xml')


def wechatChatForFun(request):
    signature = request.GET.get('signature')
    timestamp = request.GET.get('timestamp')
    nonce = request.GET.get('nonce')
    wechat_instance = WechatBasic(conf=ChatForFunConf)
    reply_text = ""
    if not wechat_instance.check_signature(
            signature=signature, timestamp=timestamp, nonce=nonce):
        return HttpResponseBadRequest('Verify Failed')
    else:
        if request.method == 'GET':
            response = request.GET.get('echostr', 'error')
        else:
            try:
                wechat_instance.parse_data(request.body)
                message = wechat_instance.get_message()
                if isinstance(message, TextMessage):
                    reply_text = str(message.content).encode('utf8')
                    reply_text = ParserMsg(reply_text, message.source)
                elif isinstance(message, ImageMessage):
                    reply_text = str(message.picurl).encode('utf8')
                    reply_text = ParserMsg(reply_text, message.source)
                elif isinstance(message, LocationMessage):
                    reply_text = str(message.label).encode('utf8')
                    reply_text = ParserMsg(reply_text, message.source)
                else:
                    reply_text = U"服务器:目前只支持文字消息,非常抱歉"

                response = wechat_instance.response_text(content=reply_text)
            except ParseError:
                return HttpResponseBadRequest("Invalid XML Data")
        return HttpResponse(response, content_type='application/xml')
