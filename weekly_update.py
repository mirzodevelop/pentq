from flask import Flask
from flask import request
import MySQLdb
import json
import hashlib
import string
import random
from random import shuffle
import jdatetime
import datetime
import time
import requests
import os
while 1==1:
    time.sleep( 5 )
    try:
        mydb = MySQLdb.connect("localhost","root","2bacvvy","quiz" )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM User;")
        myresult = mycursor.fetchall()

        mycursorO = mydb.cursor()
        mycursorO.execute("SELECT Value FROM Hidden WHERE Tag='done_pro';")
        myresultO = mycursorO.fetchall()
        up_to_date=myresultO[0][0]

        mycursorE = mydb.cursor()
        mycursorE.execute("SELECT Value FROM OptionParameter WHERE Tag='top_users_contest_end';")
        myresultE = mycursorE.fetchall()
        date_end=myresultE[0][0]

        date_now_obj=jdatetime.datetime.now()
        date_end_obj=jdatetime.datetime.strptime(date_end, '%Y/%m/%d-%H:%M')
        date_end_int=time.mktime(date_end_obj.timetuple())
        date_now_int=time.mktime(date_now_obj.timetuple())


        mycursorR = mydb.cursor()
        mycursorR.execute("SELECT Value FROM OptionParameter WHERE Tag='top_users_num';")
        myresultR = mycursorR.fetchall()
        to_prize=myresultR[0][0]

        mycursorP = mydb.cursor()
        mycursorP.execute("SELECT Value FROM OptionParameter WHERE Tag='prize';")
        myresultP = mycursorP.fetchall()
        prize=myresultP[0][0]

        if date_now_int>date_end_int and up_to_date!='Yes':
            for usr in myresult:
                mycursorA = mydb.cursor()
                sql = "UPDATE User SET DonePro='No', Score='0', WeeklyScore='0' WHERE UserName='"+usr[5]+"';"
                print(sql)
                mycursorA.execute(sql)
            mydb.commit()

            for usr in myresult:
                mycursorA = mydb.cursor()
                sql = "INSERT INTO WeeklyRecord(Score,UserName,WeekEndData) VALUES ('"+str(usr[2])+"','"+usr[5]+"','"+jdatetime.datetime.now().strftime("%y-%m-%d")+"');"
                print(sql)
                mycursorA.execute(sql)
                if usr[8] < int(to_prize):
                    new_balance=usr[11]+int(prize)
                    mycursorB = mydb.cursor()
                    sql = "UPDATE User SET Balance="+str(new_balance)+" WHERE UserName='"+usr[5]+"';"
                    print(sql)
                    mycursorB.execute(sql)
            mydb.commit()

            mycursorY = mydb.cursor()
            sql = "UPDATE Hidden SET Value='Yes' WHERE Tag='done_pro';"
            print(sql)
            mycursorY.execute(sql)
            mydb.commit()

        else:
            print("No Update Needed!")

    except Exception as e:
        print(str(e))
