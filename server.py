from flask import Flask
from flask import request
import MySQLdb
import json
import hashlib
import string
import random

app = Flask(__name__)

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
        mycursor.execute("SELECT U.DisplayName,U.Score,U.WeeklyScore,U.AllowedPackageCount,U.UserName,U.PhoneNumber,U.Rank,U.WeeklyRank FROM User AS U JOIN Session AS S ON S.UserID=U.UserName WHERE S.Token='"+request.headers['SessionID']+"';")
        myresult = mycursor.fetchall()
        row_headers=[camelize(x[0]) for x in mycursor.description] #this will extract row headers
        json_data=[]
        for result in myresult:
            json_data.append(dict(zip(row_headers,result)))
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
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM LotteryItem ORDER BY RAND() LIMIT 1;")
        myresult = mycursor.fetchall()
        row_headers=[camelize(x[0]) for x in mycursor.description] #this will extract row headers
        json_data=[]
        for result in myresult:
            json_data.append(dict(zip(row_headers,result)))
        response = app.response_class(response=json.dumps({"result":"OK","array":None,"item":json_data[0]}),status=200,mimetype='application/json')
        return response

    except Exception as e:
        print(str(e))
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
        mycursor.execute("SELECT IsTrue FROM Choice WHERE ChoiceID='"+str(request.form.get('ChoiceID'))+"';")
        myresult = mycursor.fetchall()
        row_headers=[camelize(x[0]) for x in mycursor.description] #this will extract row headers
        json_data=[]
        for result in myresult:
            json_data.append(dict(zip(row_headers,result)))
        response = app.response_class(response=json.dumps({"result":"OK","array":None,"item":{"isTrue":result[0]=='Yes'}}),status=200,mimetype='application/json')
        return response

    except Exception as e:
        print(str(e))
        response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"errorMessage":str(e)}),status=200,mimetype='application/json')
        return response


@app.route('/api/get_question_for_game', methods=['POST'])
def questions():
    data = request.get_json()
    print(request.form.get('ContestID'))
    final=[]
    try:
        mydb = MySQLdb.connect("localhost","root","2bacvvy","quiz" )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM Question  WHERE ContestID="+str(request.form.get('ContestID'))+";")

        myresult = mycursor.fetchall()
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
    data = request.get_json()
    print(data)
    hsh = hashlib.md5(data["Password"])
    if len(data["Password"])<8:
        response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"Error Message":"password must contain at least 8 characters."}),status=200,mimetype='application/json')
        return response
    if len(data["DisplayName"])<5:
        response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"Error Message":"display name must contain at least 5 characters."}),status=200,mimetype='application/json')
        return response
    if len(data["UserName"])<6:
        response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"Error Message":"username must contain at least 6 characters."}),status=200,mimetype='application/json')
        return response
    token=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(17))

    try:
        mydb = MySQLdb.connect("localhost","root","2bacvvy","quiz" )
        mycursor = mydb.cursor()
        sql = "INSERT INTO Session (Token, UserID,Estate) VALUES (%s, %s, %s)"
        val = (token,data["UserName"],"Active")
        mycursor.execute(sql, val)
        mydb.commit()
    except Exception as e:
        response = app.response_class(response=json.dumps({"result":"Error","array":None,"item":None,"errorMessage":str(e)}),status=200,mimetype='application/json')
        return response


    try:
        mydb = MySQLdb.connect("localhost","root","2bacvvy","quiz" )
        mycursor = mydb.cursor()
        sql = "INSERT INTO User (UserName, Score,WeeklyScore,PasswordHash,DisplayName,AllowedPackageCount,PhoneNumber,Rank,WeeklyRank) VALUES (%s, %s, %s, %s, %s, %s,%s,%s,%s)"
        val = (data["UserName"], "0","0",data["Password"],data["DisplayName"],"3",data["PhoneNumber"],"1","1")
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


@app.route('/api/withdraw',methods=['POST'])
def withdraw():
    data = request.get_json()
    try:
        mydb = MySQLdb.connect("localhost","root","2bacvvy","quiz" )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT U.UserID FROM User AS U JOIN Session AS S ON S.UserID=U.UserName WHERE S.Token='"+request.headers['SessionID']+"';")
        myresult = mycursor.fetchall()
        mycursor.execute("SELECT Prize FROM Question WHERE QuestionID="+request.form.get('QID')+";")
        myresult2 = mycursor.fetchall()
        print(myresult[0][0])
        print(myresult2[0][0])

        sql = "UPDATE User Set Score= Score + %s WHERE UserID=%s;"
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

@app.route('/api/get_all_lotteries')
def get_all_lotteries():
    ret=""""""
    try:
        mydb = MySQLdb.connect("localhost","root","2bacvvy","quiz" )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM LotteryItem WHERE Estate='active';")
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
        mycursor.execute("SELECT UserName,WeeklyScore,Score,Rank,WeeklyRank FROM User ORDER BY Score;")
        myresult = mycursor.fetchall()

        row_headers=[camelize(x[0]) for x in mycursor.description] #this will extract row headers
        json_data=[]
        for result in myresult:
            json_data.append(dict(zip(row_headers,result)))
        response = app.response_class(response=json.dumps({"result":"OK","array":json_data,"item":None}),status=200,mimetype='application/json')
        return response
    except Exception as e:
        response = app.response_class(response=json.dumps({"result":"OK","array":json_data,"item":None}),status=200,mimetype='application/json')
        return json.dumps({"result":"OK","array":json_data,"item":None})

    return ret


if __name__ == '__main__':
    app.run(port=8000,host='0.0.0.0')
