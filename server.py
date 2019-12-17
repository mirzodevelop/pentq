#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
import MySQLdb
import json
import hashlib
import string
import random
from random import shuffle
import jdatetime
import requests

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1600 * 1024 * 1024

def camelize(stro):
    temp=list(stro)
    temp[0]=temp[0].lower()
    return "".join(temp)

@app.route('/api')
def base():
    return "Hi there! This Is PENTO Quiz API."

@app.route('/api/authenticate', methods=['POST'])
def authenticate():
    data = request.get_json()
    print(data)
    try:
        mydb = MySQLdb.connect("localhost","root","2bacvvy","quiz" )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM User WHERE UserName='"+request.form.get('UserName')+"' AND PasswordHash='"+request.form.get('Password')+"';")
        myresult = mycursor.fetchall()

        token=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(17))
        sessid=''.join(random.choice(string.digits) for _ in range(4))

        mycursor.close()

        try:
            mydb = MySQLdb.connect("localhost","root","2bacvvy","quiz" )
            mycursor = mydb.cursor()
            sql = "DELETE FROM Session WHERE UserID='"+request.form.get('UserName')+"'"

            mycursor.execute(sql)
            mydb.commit()
        except Exception as e:
            response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"errorMessage":str(e)}),status=200,mimetype='application/json')
            return response

        try:
            mydb = MySQLdb.connect("localhost","root","2bacvvy","quiz" )
            mycursor = mydb.cursor()
            sql = "INSERT INTO Session (Token, UserID,Estate) VALUES (%s, %s, %s)"
            val = (token,request.form.get('UserName'),"Active")
            mycursor.execute(sql, val)
            mydb.commit()
        except Exception as e:
            response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"errorMessage":str(e)}),status=200,mimetype='application/json')
            return response

        if len(myresult)>0:
            response = app.response_class(response=json.dumps({"result":"OK","array":None,"item":{"sessionToken":token}}),status=200,mimetype='application/json')
            return response
        else:
            response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"errorMessage":"Wrong UserName/Password."}),status=200,mimetype='application/json')
            return response


    except Exception as e:
        print(str(e))
        response = app.response_class(response=json.dumps({"result":"error","array":None,"item":None}),status=200,mimetype='application/json')
        return response

@app.route('/api/get_user_info', methods=['GET'])
def userinfo():
    data = request.get_json()
    try:
        mydb = MySQLdb.connect("localhost","root","2bacvvy","quiz" )

        mycursor = mydb.cursor()
        mycursor2 = mydb.cursor()
        mycursor3 = mydb.cursor()

        mycursor.execute("SELECT U.DisplayName,U.Score,U.WeeklyScore,U.ReferralCode,U.AllowedPackageCount,U.UserName,U.PhoneNumber,U.Rank,U.WeeklyRank,U.Balance,U.TotalTrueAnswers,U.TotalFalseAnswers,U.TotalPaid FROM User AS U JOIN Session AS S ON S.UserID=U.UserName WHERE S.Token='"+request.headers['SessionID']+"';")
        myresult = mycursor.fetchall()

        print(myresult[0][5])

        mycursor2.execute("SELECT RequestDate,Estate,Amount,AccountName FROM MoneyRequest WHERE UserName='"+myresult[0][5]+"' ORDER BY MoneyRequestID Desc LIMIT 2;")
        myresult2 = mycursor2.fetchall()

        mycursor3.execute("SELECT * FROM WeeklyRecord WHERE UserName='"+myresult[0][5]+"';")
        myresult3 = mycursor3.fetchall()

        row_headers=[camelize(x[0]) for x in mycursor.description] #this will extract row headers
        json_data=[]
        for result in myresult:
            json_data.append(dict(zip(row_headers,result)))

        row_headers2=[camelize(x[0]) for x in mycursor2.description] #this will extract row headers
        json_data2=[]
        for result in myresult2:
            json_data2.append(dict(zip(row_headers2,result)))

        row_headers3=[camelize(x[0]) for x in mycursor3.description] #this will extract row headers
        json_data3=[]
        for result in myresult3:
            json_data3.append(dict(zip(row_headers3,result)))


        json_data[0]["moneyRequests"]=json_data2
        json_data[0]["weeklyRecords"]=json_data3
        response = app.response_class(response=json.dumps({"result":"OK","array":None,"item":json_data[0]}),status=200,mimetype='application/json')
        return response

    except Exception as e:
        print(str(e))
        response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"errorMessage":"Expired."}),status=200,mimetype='application/json')
        return response

@app.route('/api/lottery', methods=['GET'])
def lottery():
    data = request.get_json()
    try:
        mydb = MySQLdb.connect("localhost","root","2bacvvy","quiz" )

        mycursorP = mydb.cursor()
        mycursorP.execute("SELECT U.DoneLottery,U.UserName FROM User AS U JOIN Session AS S ON S.UserID=U.UserName WHERE S.Token='"+request.headers['SessionID']+"';")
        myresultP = mycursorP.fetchall()
        print(myresultP[0][0])

        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM LotteryItem ORDER BY RAND() LIMIT 1;")
        myresult = mycursor.fetchall()
        row_headers=[camelize(x[0]) for x in mycursor.description] #this will extract row headers
        json_data=[]
        for result in myresult:
            json_data.append(dict(zip(row_headers,result)))
        if(myresultP[0][0]=='No'):
            mycursorZ = mydb.cursor()
            sql = "UPDATE User Set DoneLottery='Yes' WHERE UserName='"+str(myresultP[0][1])+"';"
            print(sql)
            mycursorZ.execute(sql)
            mydb.commit()
            response = app.response_class(response=json.dumps({"result":"OK","array":None,"item":json_data[0]}),status=200,mimetype='application/json')
            return response
        else:
            response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"errorMessage":"از لاتاری استفاده شده"}),status=200,mimetype='application/json')
            return response
    except Exception as e:
        print(str(e))
        response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"errorMessage":str(e)}),status=200,mimetype='application/json')
        return response

@app.route('/api/money_request', methods=['POST'])
def money_request():
    data = request.get_json()
    print(data)
    print(jdatetime.date.today())
    try:
        mydb = MySQLdb.connect("localhost","root","2bacvvy","quiz" )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT U.Balance,U.UserName FROM User AS U JOIN Session AS S ON S.UserID=U.UserName WHERE S.Token='"+request.headers['SessionID']+"';")
        myresult = mycursor.fetchall()
        print(myresult[0][0])
        print(myresult[0][1])
        if(int(myresult[0][0])<int(request.form.get('Amount'))):
            response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"errorMessage":"Account balance is not enough."}),status=200,mimetype='application/json')
            return response
    except Exception as e:
        response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"errorMessage":"Expired."}),status=200,mimetype='application/json')
        return response

    try:
        mydb = MySQLdb.connect("localhost","root","2bacvvy","quiz" )
        mycursor = mydb.cursor()
        sql = "INSERT INTO MoneyRequest (Estate,BankAccount,AccountName,Amount,RequestDate,UserName) VALUES (%s, %s, %s, %s, %s,%s)"
        val = ("New",request.form.get('AccountNumber'),request.form.get('AccountName').encode("utf8"),request.form.get('Amount'),jdatetime.date.today(),myresult[0][1])
        mycursor.execute(sql, val)
        mydb.commit()

        mycursorT = mydb.cursor()
        sql = "UPDATE User SET Balance=Balance-"+str(request.form.get('Amount'))+";"
        mycursorT.execute(sql)
        mydb.commit()
        response = app.response_class(response=json.dumps({"result":"OK","array":None,"item":None}),status=200,mimetype='application/json')
        return response
    except Exception as e:
        response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"errorMessage":str(e)}),status=200,mimetype='application/json')
        return response

@app.route('/api/remove_two', methods=['POST'])
def remove_two():
    data = request.get_json()
    print(data)

    try:
        mydb = MySQLdb.connect("localhost","root","2bacvvy","quiz" )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT U.Rank FROM User AS U JOIN Session AS S ON S.UserID=U.UserName WHERE S.Token='"+request.headers['SessionID']+"';")
        myresult = mycursor.fetchall()
        print(myresult[0][0])
        if(int(myresult[0][0])>3):
            response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"errorMessage":"only for 1-3 ranks."}),status=200,mimetype='application/json')
            return response
    except Exception as e:
        response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"errorMessage":"Expired."}),status=200,mimetype='application/json')
        return response

    try:
        mydb = MySQLdb.connect("localhost","root","2bacvvy","quiz" )
        mycursor = mydb.cursor()
        sql = "SELECT ChoiceID FROM Choice WHERE QuestionID="+request.form.get('QID')+" and IsTrue='No' LIMIT 2;"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        row_headers=[camelize(x[0]) for x in mycursor.description] #this will extract row headers
        json_data=[]
        for result in myresult:
            json_data.append(dict(zip(row_headers,result)))
        response = app.response_class(response=json.dumps({"result":"OK","array":json_data,"item":None}),status=200,mimetype='application/json')
        return response
    except Exception as e:
        response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"errorMessage":str(e)}),status=200,mimetype='application/json')
        return response

@app.route('/api/choice_percent', methods=['POST'])
def choice_percent():
    data = request.get_json()
    print(data)

    try:
        mydb = MySQLdb.connect("localhost","root","2bacvvy","quiz" )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT U.Rank FROM User AS U JOIN Session AS S ON S.UserID=U.UserName WHERE S.Token='"+request.headers['SessionID']+"';")
        myresult = mycursor.fetchall()
        print(myresult[0][0])
        if(int(myresult[0][0])>3):
            response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"errorMessage":"only for 1-3 ranks."}),status=200,mimetype='application/json')
            return response
    except Exception as e:
        response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"errorMessage":"Expired."}),status=200,mimetype='application/json')
        return response

    try:
        a = random.randint(3, 29)
        b = random.randint(3, 50)
        d = random.randint(3, 19)
        c=100-a-b-d
        arr=[a,b,c,d]
        random.shuffle(arr)
        print(arr)
        response = app.response_class(response=json.dumps({"result":"OK","array":arr,"item":None}),status=200,mimetype='application/json')
        return response
    except Exception as e:
        response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"errorMessage":str(e)}),status=200,mimetype='application/json')
        return response

@app.route('/api/send_question_answer', methods=['POST'])
def answer():
    data = request.get_json()
    print(data)
    if str(request.form.get('ChoiceID')) == "-1":
        response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"errorMessage":"Time Limit Exceeded."}),status=200,mimetype='application/json')
        return response

    try:
        mydb = MySQLdb.connect("localhost","root","2bacvvy","quiz" )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT IsTrue FROM Choice WHERE ChoiceID='"+str(request.form.get('ChoiceID'))+"' AND QuestionID='"+str(request.form.get('QID'))+"';")
        myresult = mycursor.fetchall()
        row_headers=[camelize(x[0]) for x in mycursor.description] #this will extract row headers
        json_data=[]
        for result in myresult:
            json_data.append(dict(zip(row_headers,result)))

        mycursorQ = mydb.cursor()
        mycursorQ.execute("SELECT Prize,IsSaftyLevel,ContestID From Question WHERE QuestionID="+str(request.form.get('QID'))+";")
        myresultQ = mycursorQ.fetchall()
        print(myresultQ[0][0])

        mycursorX = mydb.cursor()
        mycursorX.execute("SELECT U.UserID,U.AllowedPackageCount FROM User AS U JOIN Session AS S ON S.UserID=U.UserName WHERE S.Token='"+request.headers['SessionID']+"';")
        myresultX = mycursorX.fetchall()
        print(myresultX[0][0])
        print(myresultX[0][1])

        trueone="0"
        falseone="1"
        if result[0]=='Yes':
            print("here!")
            trueone="1"
            falseone="0"
        if result[0]=='Yes' and myresultQ[0][1]=='Yes':
            print("here!")
            trueone="1"
            falseone="0"
            mycursorZ = mydb.cursor()
            sql = "UPDATE User Set TempScore= "+str(myresultQ[0][0])+" WHERE UserID="+str(myresultX[0][0])+";"
            print(sql)
            mycursorZ.execute(sql)
        else:
            mycursorA = mydb.cursor()
            if myresultQ[0][2]==1:
                sql = "UPDATE User Set Score=Score+TempScore , WeeklyScore=WeeklyScore+TempScore , TempScore=0 WHERE UserID="+str(myresultX[0][0])+";"
            else:
                sql = "UPDATE User Set Balance=Balance+TempScore , TempScore=0 WHERE UserID="+str(myresultX[0][0])+";"
            print(sql)
            mycursorA.execute(sql)

        mycursorL = mydb.cursor()
        sql = "INSERT INTO AnswerLog (QID,UserName,Estate) VALUES ('"+str(request.form.get('QID'))+"','"+str(myresultX[0][0])+"','"+str(result[0]=='Yes')+"');"
        print(sql)
        mycursorL.execute(sql)

        if int(myresultX[0][1])<1:
            response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"errorMessage":"Out of Allowed QUESTION"}),status=200,mimetype='application/json')
            return response
        mycursorY = mydb.cursor()
        print("true/false:")
        print(trueone)
        print(falseone)
        sql = "UPDATE User Set AllowedPackageCount= AllowedPackageCount - 1 , TotalTrueAnswers=TotalTrueAnswers+"+trueone+", TotalFalseAnswers=TotalFalseAnswers+"+falseone+" WHERE UserID="+str(myresultX[0][0])+";"
        print(sql)
        mycursorY.execute(sql)
        mydb.commit()

        response = app.response_class(response=json.dumps({"result":"OK","array":None,"item":{"isTrue":result[0]=='Yes'}}),status=200,mimetype='application/json')
        return response

    except Exception as e:
        print(str(e))
        ermsg=str(e)
        if(str(e)=="local variable 'result' referenced before assignment"):
            ermsg="گزینه ارسالی متعلق به سوال نیست."
        response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"errorMessage":ermsg}),status=200,mimetype='application/json')
        return response


@app.route('/api/get_question_for_game', methods=['POST'])
def questions():
    data = request.get_json()
    print(request.form.get('ContestID'))
    final=[]
    try:
        mydb = MySQLdb.connect("localhost","root","2bacvvy","quiz" )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT U.Rank,U.UserID FROM User AS U JOIN Session AS S ON S.UserID=U.UserName WHERE S.Token='"+request.headers['SessionID']+"';")
        myresult = mycursor.fetchall()
        print(myresult[0][0])
        userid=myresult[0][1]
        if(int(myresult[0][0])>3 and int(request.form.get('ContestID'))==2):
            response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"errorMessage":"only for 1-3 ranks."}),status=200,mimetype='application/json')
            return response
    except Exception as e:
        response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"errorMessage":"Expired."}),status=200,mimetype='application/json')
        return response
    try:
        mydb = MySQLdb.connect("localhost","root","2bacvvy","quiz" )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM Question  WHERE ContestID="+str(request.form.get('ContestID'))+" ORDER BY OrderNum;")
        myresult = mycursor.fetchall()

        sqq="SELECT QID FROM AnswerLog WHERE UserName='"+str(userid)+"';"
        print(sqq)
        mycursor.execute(sqq)
        myresult2 = mycursor.fetchall()

        print(list(myresult2))
        answered = [item[0] for item in myresult2]
        print(answered)
        print(29 in answered)

        if len(myresult)==0:
            response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"errorMessage":"ContestID "+ str(request.form.get('ContestID')) +" Not Exist." }),status=200,mimetype='application/json')
            return response
        for qu in myresult:
            try:
                mydb2 = MySQLdb.connect("localhost","root","2bacvvy","quiz" )
                mycursor2 = mydb.cursor()
                mycursor2.execute("SELECT ChoiceID,Title FROM Choice WHERE QuestionID="+str(qu[1])+";")
                myresult2 = mycursor2.fetchall()
                row_headers=[camelize(x[0]) for x in mycursor2.description] #this will extract row headers
                json_data=[]
                for result in myresult2:
                    json_data.append(dict(zip(row_headers,result)))

                if not qu[1] in answered:
                    final.append({"question":{"questionID":qu[1],"order":qu[0],"statement":qu[3],"prize":qu[6],"isSaftyLevel":qu[7]=='Yes',"answerTime":qu[8]},"choices":json_data})
            except Exception as e:
                response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"errorMessage":str(e)}),status=200,mimetype='application/json')
                return response
        response = app.response_class(response=json.dumps({"result":"OK","array":final,"item":None}),status=200,mimetype='application/json')
        return response

    except Exception as e:
        print(str(e))
        response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"errorMessage":"Empty ContestID"}),status=200,mimetype='application/json')
        return response


@app.route('/api/register_new_user', methods=['POST'])
def register_new_user():
    #data = request.get_json()
    print(request.form)
    #hsh = hashlib.md5(data["Password"])
    if len(request.form.get('Password'))<8:
        response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"Error Message":"password must contain at least 8 characters."}),status=200,mimetype='application/json')
        return response
    if len(request.form.get('DisplayName'))<5:
        response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"Error Message":"display name must contain at least 5 characters."}),status=200,mimetype='application/json')
        return response
    if len(request.form.get('UserName'))<6:
        response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"Error Message":"username must contain at least 6 characters."}),status=200,mimetype='application/json')
        return response
    token=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(17))

    try:
        mydb = MySQLdb.connect("localhost","root","2bacvvy","quiz" )
        mycursor = mydb.cursor()
        sql = "INSERT INTO Session (Token, UserID,Estate) VALUES (%s, %s, %s)"
        val = (token,request.form.get('UserName'),"Active")
        mycursor.execute(sql, val)
        mydb.commit()
    except Exception as e:
        response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"errorMessage":str(e)}),status=200,mimetype='application/json')
        return response
    try:
        rcode=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
        mydb = MySQLdb.connect("localhost","root","2bacvvy","quiz" )
        mycursor = mydb.cursor()
        sql = "INSERT INTO User (UserName, Score,WeeklyScore,PasswordHash,DisplayName,AllowedPackageCount,PhoneNumber,Rank,WeeklyRank,ReferralCode,Balance,TotalTrueAnswers,TotalFalseAnswers,TotalPaid,TempScore,DoneLottery) VALUES (%s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (request.form.get('UserName'), "0","0",request.form.get('Password'),request.form.get('DisplayName'),"3",request.form.get('PhoneNumber'),"1","1",rcode,"0","0","0","0","0","No")
        mycursor.execute(sql, val)
        mydb.commit()

        response = app.response_class(response=json.dumps({"result":"OK","array":None,"item":{"sessionToken":token}}),status=200,mimetype='application/json')
        return response
    except Exception as e:
        response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"errorMessage":str(e)}),status=200,mimetype='application/json')
        return response

@app.route('/api/guest_session', methods=['POST'])
def guest_session():
    token=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(17))
    usrnme='guest_'+''.join(random.choice(string.digits) for _ in range(8))
    try:
        mydb = MySQLdb.connect("localhost","root","2bacvvy","quiz" )
        mycursor = mydb.cursor()
        sql = "INSERT INTO Session (Token, UserID,Estate) VALUES (%s, %s, %s)"
        val = (token,usrnme,"Active")
        mycursor.execute(sql, val)
        mydb.commit()
    except Exception as e:
        response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"errorMessage":str(e)}),status=200,mimetype='application/json')
        return response
    try:
        rcode=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
        mydb = MySQLdb.connect("localhost","root","2bacvvy","quiz" )
        mycursor = mydb.cursor()
        sql = "INSERT INTO User (UserName, Score,WeeklyScore,PasswordHash,DisplayName,AllowedPackageCount,PhoneNumber,Rank,WeeklyRank,ReferralCode,Balance,TotalTrueAnswers,TotalFalseAnswers,TotalPaid,TempScore,DoneLottery) VALUES (%s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (usrnme, "0","0","","","3","","1","1","","0","0","0","0","0","No")
        mycursor.execute(sql, val)
        mydb.commit()

        response = app.response_class(response=json.dumps({"result":"OK","array":None,"item":{"sessionToken":token}}),status=200,mimetype='application/json')
        return response
    except Exception as e:
        response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"errorMessage":str(e)}),status=200,mimetype='application/json')
        return response

@app.route('/api/get_admob_tokens')
def get_admob_tokens():
    ret=""""""
    try:
        mydb = MySQLdb.connect("localhost","root","2bacvvy","quiz" )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM ADSToken;")
        myresult = mycursor.fetchall()

        row_headers=[camelize(x[0]) for x in mycursor.description] #this will extract row headers
        json_data=[]
        for result in myresult:
            json_data.append(dict(zip(row_headers,result)))
        response = app.response_class(response=json.dumps({"result":"OK","array":json_data,"item":None}),status=200,mimetype='application/json')
        return response
    except Exception as e:
        response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"errorMessage":str(e)}),status=200,mimetype='application/json')
        return response

    return ret

@app.route('/api/get_options')
def get_options():
        ret=""""""
        try:
            mydb = MySQLdb.connect("localhost","root","2bacvvy","quiz" )
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM OptionParameter;")
            myresult = mycursor.fetchall()

            row_headers=[camelize(x[0]) for x in mycursor.description] #this will extract row headers
            json_data=[]
            for result in myresult:
                json_data.append(dict(zip(row_headers,result)))
            response = app.response_class(response=json.dumps({"result":"OK","array":json_data,"item":None}),status=200,mimetype='application/json')
            return response
        except Exception as e:
            response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"errorMessage":str(e)}),status=200,mimetype='application/json')
            return response

        return ret

@app.route('/api/skip', methods=['POST'])
def skip():
    ret=""""""
    response = app.response_class(response=json.dumps({"result":"OK","array":None,"item":None}),status=200,mimetype='application/json')
    return response

@app.route('/api/others_answers', methods=['POST'])
def others_answers():
    ret=""""""
    a=random.randint(3, 35)
    b=random.randint(3, 35)
    c=random.randint(3, 35)
    d=100-a-b-c
    response = app.response_class(response=json.dumps({"result":"OK","array":shuffle([a,b,c,d]),"item":None}),status=200,mimetype='application/json')
    return response


@app.route('/api/withdraw',methods=['POST'])
def withdraw():
    data = request.get_json()
    try:
        mydb = MySQLdb.connect("localhost","root","2bacvvy","quiz" )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT U.UserID FROM User AS U JOIN Session AS S ON S.UserID=U.UserName WHERE S.Token='"+request.headers['SessionID']+"';")
        myresult = mycursor.fetchall()
        mycursor.execute("SELECT Prize,	ContestID FROM Question WHERE QuestionID="+request.form.get('QID')+";")
        myresult2 = mycursor.fetchall()
        print(myresult[0][0])
        print(myresult2[0][0])
        print(myresult2[0][1])

        if myresult2[0][1]==1:
            sql = "UPDATE User Set Score= Score + %s WHERE UserID=%s;"
            val = (str(myresult2[0][0]),str(myresult[0][0]))
            mycursor.execute(sql, val)
            mydb.commit()
        else:
            sql = "UPDATE User Set Balance= Balance + %s WHERE UserID=%s;"
            val = (str(myresult2[0][0]),str(myresult[0][0]))
            mycursor.execute(sql, val)
            mydb.commit()

        json_data=[]
        response = app.response_class(response=json.dumps({"result":"OK","array":None,"item":None}),status=200,mimetype='application/json')
        return response

    except Exception as e:
        print(str(e))
        response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"errorMessage":"Expired."}),status=200,mimetype='application/json')
        return response

@app.route('/api/reward_for_video',methods=['POST'])
def reward_for_video():
    data = request.get_json()
    try:
        mydb = MySQLdb.connect("localhost","root","2bacvvy","quiz" )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT U.UserID FROM User AS U JOIN Session AS S ON S.UserID=U.UserName WHERE S.Token='"+request.headers['SessionID']+"';")
        myresult = mycursor.fetchall()
        print(myresult[0][0])

        sql = "UPDATE User Set AllowedPackageCount= AllowedPackageCount + %s WHERE UserID=%s;"
        val = ("1",str(myresult[0][0]))
        mycursor.execute(sql, val)
        mydb.commit()

        json_data=[]
        response = app.response_class(response=json.dumps({"result":"OK","array":None,"item":None}),status=200,mimetype='application/json')
        return response

    except Exception as e:
        print(str(e))
        response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"errorMessage":"Expired."}),status=200,mimetype='application/json')
        return response


@app.route('/api/get_all_lotteries')
def get_all_lotteries():
    ret=""""""
    try:
        mydb = MySQLdb.connect("localhost","root","2bacvvy","quiz" )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM LotteryItem;")
        myresult = mycursor.fetchall()

        row_headers=[camelize(x[0]) for x in mycursor.description] #this will extract row headers
        json_data=[]
        for result in myresult:
            json_data.append(dict(zip(row_headers,result)))
        response = app.response_class(response=json.dumps({"result":"OK","array":json_data,"item":None}),status=200,mimetype='application/json')
        return response
    except Exception as e:
        response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"errorMessage":str(e)}),status=200,mimetype='application/json')
        return response

    return ret

@app.route('/api/get_shop_items')
def get_shop_items():
    ret=""""""
    try:
        mydb = MySQLdb.connect("localhost","root","2bacvvy","quiz" )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM Package;")
        myresult = mycursor.fetchall()

        row_headers=[camelize(x[0]) for x in mycursor.description] #this will extract row headers
        json_data=[]
        for result in myresult:
            json_data.append(dict(zip(row_headers,result)))
        response = app.response_class(response=json.dumps({"result":"OK","array":json_data,"item":None}),status=200,mimetype='application/json')
        return response
    except Exception as e:
        response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"errorMessage":str(e)}),status=200,mimetype='application/json')
        return response
    return ret

@app.route('/api/leaderboard')
def leaderboard():
    ret=""""""
    try:
        mydb = MySQLdb.connect("localhost","root","2bacvvy","quiz" )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT UserName,WeeklyScore,Score,Rank,WeeklyRank FROM User ORDER BY Score DESC;SET @rank=0, @score=-100; UPDATE User SET Rank=IF(@Score=(@Score:=Score), @Rank, @Rank:=@Rank+1) ORDER BY Score DESC;")
        myresult = mycursor.fetchall()

        row_headers=[camelize(x[0]) for x in mycursor.description] #this will extract row headers
        json_data=[]
        for result in myresult:
            json_data.append(dict(zip(row_headers,result)))
        response = app.response_class(response=json.dumps({"result":"OK","array":json_data,"item":None}),status=200,mimetype='application/json')
        return response
    except Exception as e:
        response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"errorMessage":str(e)}),status=200,mimetype='application/json')
        return response

    return ret

@app.route('/api/payment',methods=['POST'])
def payment():
    try:
        reqstr='''{
          "order_id": "#ORDERID#",
          "amount": #AMOUNT#,
          "name": "#NAME#",
          "phone": "09382198592",
          "mail": "",
          "desc": "",
          "callback": "http://barande.clashofwin.com",
          "reseller": null
        }'''

        mydb = MySQLdb.connect("localhost","root","2bacvvy","quiz" )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT U.UserID FROM User AS U JOIN Session AS S ON S.UserID=U.UserName WHERE S.Token='"+request.headers['SessionID']+"';")
        myresult = mycursor.fetchall()
        print(myresult[0][0])

        mycursorP = mydb.cursor()
        mycursorP.execute("SELECT Title,Price From Package WHERE PackageID="+str(request.form.get('PID'))+";")
        myresultP = mycursorP.fetchall()
        print(myresultP[0][0])
        print(myresultP[0][1])

        payload=reqstr.replace("#AMOUNT#",str(myresultP[0][1])).replace("#NAME#",str(myresultP[0][0])).replace("#ORDERID#",str(myresult[0][0]*10000+int(request.form.get('PID'))))
        print(payload)

        headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': '55812935-e7a6-49c6-b72c-a4422cb72a03',
        }
        r = requests.post("https://api.idpay.ir/v1.1/payment", data=payload, headers=headers)
        print(json.loads(r.text)['link'])
        response = app.response_class(response=json.dumps({"result":"OK","array":None,"item":json.loads(r.text)['link']}),status=200,mimetype='application/json')
        return response
    except Exception as e:
        response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"errorMessage":str(e)}),status=200,mimetype='application/json')
        return response

if __name__ == '__main__':
    app.run(port=8000,host='0.0.0.0')
