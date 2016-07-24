import MySQLdb
class WeChatDb:
    def __init__(self,ip,userName,passwd,DBName):
        self.mysqlIp=ip
        self.userName=userName
        self.passwd=passwd
        self.DBName=DBName
        self.db = MySQLdb.connect(ip,userName,passwd,DBName)
        self.cursor = self.db.cursor()
    def AddUser(self,UserId):
        try:
            sql="select * from User_Info"
            cursor.execute(sql)
            print "Execute Sql"
            data = cursor.fetchall()
            print "Database version : %s " % data
        except:
            print "Add User Failed"
            
            
    def Close(self):
        self.db.close()


def ParserMsg(strMsg,userID):
    strResult=""
    if (strMsg[0] == '1'):
		strResult = "Send   Message"
		return strResult
    if (strMsg[0] == '2'):
		pstrResult = "Get Message"

		return strResult
    if (strMsg[0] == '3'):
		strResult =   "Log In"

		return strResult
    if (strMsg[0] == '4'):
		strResult = "Login out"
		return strResult

    if (strMsg[0] == '5'):
		strResult =  "On Chat"

		return strResult
    if (strMsg[0] == '6'):
		strResult = "Off Chat"
		return strResult
    if (strMsg[0] != '6'):
		strResult = "Off Chat"
		return strResult

def AddUser(userID):
    db = MySQLdb.connect("localhost","root","dennis","WeChat")
    cursor = db.cursor()
    sql = "SELECT * FROM User_Info WHERE userId like \"%s\" " % userID
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        if (len(results) == 0):
            sql = "INSERT INTO User_Info(userId,isLogin,isChat,name) VALUES('%s',0,0,'nobody')" % userID
            cursor2=db.cursor()
            cursor2.execute(sql)
            db.commit()
            cursor2.close()
        else:
            print "Get Result"
            print(results)
    except:
        print "Error: unable to fecth data"
    
    cursor.close()
    db.close()



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
    db = MySQLdb.connect("localhost","root","dennis","WeChat")
    cursor = db.cursor()
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
    db = MySQLdb.connect("localhost","root","dennis","WeChat")
    cursor = db.cursor()
    sql = "UPDATE User_Info SET isChat = 0 WHERE userID like \"%s\" " % userID
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

	sql="DELETE FROM ChatPair WHERE FromID like \"%s\" OR ToID like \"%s\""%(userID,userID)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

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
    return bLogIn

def SetPair(userID):
	if not IsLogin(userID):
		return ""
	if IsChat(userID):
		return ""
	db = MySQLdb.connect("localhost","root","dennis","WeChat")
	cursor = db.cursor()
	sql="SELECT * FROM User_Info WHERE isLogin=1 AND isChat = 0 AND userId not like \"%s\""%userID
	pairID=""
	try:
		cursor.execute(sql)
		results = cursor.fetchone()
		if (len(results) != 0):
			pairID = results[0][1]
			OnChat(userID)
			OnChat(pairID)
			sql="UPDATE TABLE SET isChat = 1 WHERE userId like \"%s\" "%userID
			try:
				cursor.execute(sql)
				db.commit()
			except:
				db.rollback()
			
			sql="UPDATE TABLE SET isChat = 1 WHERE userId like \"%s\" "%pairID
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
			pairID = ""
			print pairID
	except:
		print "SQL ERROR "
		print sql
    
	cursor.close()
	db.close()
	return 
     

def GetPair(userID):
    if not IsLogin(userID):
        return ""
    if not IsChat(userID):
        return ""


    db = MySQLdb.connect("localhost","root","dennis","WeChat")
    cursor = db.cursor()
    sql="SELECT * FROM ChatPair WHERE FromID like \"%s\""%userID

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
    sql="INSERT INTO Message(ReceiveID,msg,isSend) VALUES('%s','%s',0)" %(toID,msg) 

    try:
        print sql
        cursor.execute(sql)
        db.commit()
    except:
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

        for elem in results:
            strMsg += elem[2]

        print strMsg
        sql="UPDATE Message SET isSend=1 WHERE isSend=0 AND ReceiveID like \"%s\" " % userID
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


def Test():
    myDict = dict()
    print myDict

    myList = list()
    print myList

"""print "*******************************************"
AddUser('Start')
print "*******************************************"
AddUser('stop')
print "*******************************************"
Login('Start')

print "*******************************************"
Login('stop')
print "*******************************************"
LogOut('stop')


print "*******************************************"
OnChat('Start')
print "*******************************************"
OffChat('stop')
print "*******************************************"


print IsChat('Start')
print "*******************************************"
print IsLogin('Stop')
print "*******************************************"
print IsChat('stop')
print "*******************************************"
print IsLogin('Start')

print "*******************************************"
print "GetPair Test  User :Stop "
print GetPair('Stop')


print "*******************************************"
print "GetPair Test  User :Start "
print GetPair('Start')


print "*******************************************"
print "Send Message Test"
SendMessage('Stop','I have finished')
SendMessage('Start','I have finished')

print "*******************************************"
print "Get Message Test"
print GetMessage('Stop')
print GetMessage('Start')

print GetMessage('Stop')
#weChatMySql = WeChatDb("localhost","root","dennis","WeChat")

#weChatMySql = WeChatDb("localhost","root","dennis","WeChat")

#weChatMySql.AddUser("Hello")
#weChatMySql.Close("""

ParserMsg("1 hello world",'Start')
ParserMsg("2 hello world",'Stop')

