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
try:
    mydb = MySQLdb.connect("localhost","root","2bacvvy","quiz" )

    mycursorO = mydb.cursor()
    mycursorO.execute("SELECT Value FROM OptionParameter WHERE Tag='top_users_contest_time';")
    myresultO = mycursorO.fetchall()
    date_start=myresultO[0][0]

    mycursorE = mydb.cursor()
    mycursorE.execute("SELECT Value FROM OptionParameter WHERE Tag='top_users_contest_end';")
    myresultE = mycursorE.fetchall()
    date_end=myresultE[0][0]

    mycursorD = mydb.cursor()
    mycursorD.execute("SELECT Value FROM Hidden WHERE Tag='done_pro';")
    myresultD = mycursorD.fetchall()
    done_end=myresultD[0][0]

    date_beg_obj=jdatetime.datetime.strptime(date_start, '%Y/%m/%d-%H:%M')
    date_end_obj=jdatetime.datetime.strptime(date_end, '%Y/%m/%d-%H:%M')

    date_now_obj=jdatetime.datetime.now()

    date_beg_int=time.mktime(date_beg_obj.timetuple())
    date_end_int=time.mktime(date_end_obj.timetuple())
    date_now_int=time.mktime(date_now_obj.timetuple())

    if date_now_int > date_end_int and done_end!='Yes':
        os.system("nodejs weekly_records.js")
        mycursorD = mydb.cursor()
        sql = "UPDATE Hidden Set Value='Yes' WHERE Tag='done_pro'; "
        mycursorD.execute(sql)
        mydb.commit()


except Exception as e:
    print(str(e))
