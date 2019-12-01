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
  if (typeof req.session.user == 'undefined') {
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
  Deleter.delete_where('Question', "QuestionID='" + req.query.id + "'", function(insert_result) {
    res.redirect("questions");
  });

})

app.post('/commit_question', function(req, res) {
  Insertor.insert_one('Question', ['QuestionStatement', 'OrderNum', 'QuestionType', 'ContestID', 'Prize', 'AnswerTime', 'IsSaftyLevel'],
    [req.body.statement, req.body.order, 'MultipleChoice', req.body.contest, req.body.prize, req.body.time, req.body.saftey],
    function(insert_result) {
      console.log(insert_result.insertId);
      var qunum = insert_result.insertId;
      var istrue = 'No';

      Insertor.insert_one('Choice', ['QuestionID', 'Title', 'IsTrue'], [qunum, req.body.c1, (req.body.answer == 1) ? "Yes" : "No"], function(res_) {

        Insertor.insert_one('Choice', ['QuestionID', 'Title', 'IsTrue'], [qunum, req.body.c2, (req.body.answer == 2) ? "Yes" : "No"], function(res_) {

          Insertor.insert_one('Choice', ['QuestionID', 'Title', 'IsTrue'], [qunum, req.body.c3, (req.body.answer == 3) ? "Yes" : "No"], function(res_) {

            Insertor.insert_one('Choice', ['QuestionID', 'Title', 'IsTrue'], [qunum, req.body.c4, (req.body.answer == 4) ? "Yes" : "No"], function(res_) {
              res.redirect("questions");
            });
          });
        });
      });
    });
})

app.post('/commit_lottery', function(req, res) {
  Insertor.insert_one('LotteryItem', ['Title','Type','Amount'],
    [req.body.title,req.body.type,req.body.amount],
    function(insert_result) {
      res.redirect("lottery");
    });
})


app.get('/questions', function(req, res) {
  Selector.select_all("Question", function(select_result) {
    var data = {
      "Questions": select_result
    };
    console.log(data);
    res.render("questions.ejs", data);
  });
})

app.get('/new_lottery', function(req, res) {
  res.render("new_lottery.ejs");
})


app.get('/lottery', function(req, res) {
  Selector.select_all("LotteryItem", function(select_result) {
    var data = {
      "LotteryItem": select_result
    };
    console.log(data);
    res.render("lottery.ejs", data);
  });
})

app.get('/delete_lottery', function(req, res) {
  Deleter.delete_where('LotteryItem', "LotteryItemID='" + req.query.id + "'", function(insert_result) {
    res.redirect("lottery");
  });

})

app.get('/tokens', function(req, res) {
  Selector.select_all("ADSToken", function(select_result) {
    var data = {
      "Tokens": select_result
    };
    console.log(data);
    res.render("tokens.ejs", data);
  });
})

app.get('/edit_token', function(req, res) {
  Selector.select_all_where("ADSToken","ADSTokenID="+req.query.id, function(select_result) {
    var data = {
      "Token": select_result[0]
    };
    console.log(data);
    res.render("edit_tokens.ejs", data);
  });
})

app.post('/checkuser', function(req, res) {
  Selector.select_all_where('Admin', "UserName='" + req.body.uname + "' AND PassHash='" + md5(req.body.passwd) + "'", function(select_result) {
    if (select_result.length == 1) {
      req.session.user = select_result[0];
      res.redirect("/");
    } else {
      res.redirect("login");
    }
  });
})


app.listen(port, () => console.log(`Example app listening on port ${port}!`))
