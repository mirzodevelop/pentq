const express = require('express')
const request = require("request");
const bodyParser = require("body-parser");
var fs = require('fs');
var path = require('path');
var dir = path.join(__dirname, 'public');
const app = express()
var cookieParser = require('cookie-parser');
var session = require('express-session');
var formidable = require('formidable');
var mysql = require('mysql');
var md5 = require('md5');

var Deleter = require("./Deleter.js");
var Selector = require("./Selector.js");
var Insertor = require("./Insertor.js");

var Iconv = require('iconv').Iconv;
var iconv = new Iconv('UTF-8', 'ISO-8859-1');

const utf8 = require('utf8');


//configs
const port = 8888;

app.set('views', __dirname + '/views');
app.use(express.static(__dirname + '/public'));

app.use(bodyParser.urlencoded({
  extended: false
}))
app.use(bodyParser.json())

app.use('/static', express.static(path.join(__dirname, 'public')))

app.use(session({
    key: 'kloche',
    secret: '1z5xdfgjkl5nbgmht',
    resave: false,
    saveUninitialized: false,
    cookie: {
        expires: 600000
    }
}));

app.use(cookieParser());

app.get('/', function(req, res) {
    console.log(req.session.user);
    if (typeof req.session.user == 'undefined')
    {
      res.redirect("/login");
    }
    res.render("main.ejs");
})

app.get('/login', function(req, res) {
    res.render("login.ejs");
})

app.get('/new_question', function(req, res) {
    res.render("new_question.ejs");
})

app.get('/delete_question', function(req, res) {
    Deleter.delete_where('Question', "QuestionID='"+req.query.id+"'", function(insert_result) {
      res.redirect("questions");
    });

})

app.post('/commit_question', function(req, res) {
  Insertor.insert_one('Question', ['QuestionStatement','OrderNum','QuestionType','ContestID'],
   [req.body.statement,0,'MultipleChoice',1], function(insert_result) {
    res.redirect("questions");
  });
})

app.get('/questions', function(req, res) {
  Selector.select_all("Question",function(select_result){
    var data={"Questions":select_result};
    console.log(data);
    res.render("questions.ejs",data);
  });
})


app.post('/checkuser', function(req, res) {
  Selector.select_all_where('Admin', "UserName='" + req.body.uname +"' AND PassHash='"+md5(req.body.passwd)+"'", function(select_result){
    if(select_result.length==1)
    {
      req.session.user=select_result[0];
      res.redirect("/");
    }
    else {
      res.redirect("login");
    }
  });
})


app.listen(port, () => console.log(`Example app listening on port ${port}!`))
