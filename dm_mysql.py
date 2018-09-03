#-*- coding: utf-8 -*-
import MySQLdb;

class  mySqlConn:
    """This class is connect to mysql"""
    def __init__(self, host="localhost", port=3306, user="root", password="", db="dbd"):
        """Construct function,
        connect to mysql,
        and set names utf8"""
        self.__mqUser__ = user
        self.__port__ = int(port)
        self.__mqPass__ = password
        self.__mqHost__ = host
        self.__mqDb__ = db
        
        self.connect();
        
    def connect(self):
        self.__conn__ = MySQLdb.connect(user=self.__mqUser__, port=self.__port__, passwd=self.__mqPass__, host=self.__mqHost__, db=self.__mqDb__)
        self.__cursor__ = self.__conn__.cursor(cursorclass = MySQLdb.cursors.DictCursor)
     
    def set_character_set(self, char_set):
        """ Execute a sql """
        self.__conn__.set_character_set(char_set)
   
    def Query(self, sql):
        """ Execute a sql """
        iRet = 0;
        try:
            iRet = self.__cursor__.execute(sql);
            self.__conn__.commit();
        except:
            try:
                self.connect();
                iRet = self.__cursor__.execute(sql);
            except Exception as e:
                print sql
                print "Sql excute faild!"
                print e;
                return -1;
        return iRet;
    
    def Execute(self, sql):
        """ Execute a sql """
        try:
            iRet = self.__cursor__.execute(sql);
            self.__conn__.commit();
        except Exception as e:
            try:
                self.connect();
                iRet = self.__cursor__.execute(sql);
                self.__conn__.commit();
            except Exception as e:
                print sql
                print "Sql excute faild!"
                print e;
                return False;
        return True;
    
    def GetMqCursor(self):
        """Get Mysql Cursor"""
        return self.__cursor__
    
    def GetFetch(self):
        """Get fetch row"""
        return self.__cursor__.fetchall()
    
    def Close(self):
        """Close the mysql connect"""
        self.__cursor__.close()
