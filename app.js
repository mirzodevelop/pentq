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
var fileUpload=require('express-fileupload');

var Deleter = require("./Deleter.js");
var Selector = require("./Selector.js");
var Insertor = require("./Insertor.js");
var Updater = require("./Updater.js");

var Iconv = require('iconv').Iconv;
var iconv = new Iconv('UTF-8', 'ISO-8859-1');

const utf8 = require('utf8');


//configs
const port = 8888;

app.set('views', __dirname + '/views');
app.use(express.static(__dirname + '/public'));

app.use(fileUpload({
  limits: { fileSize: 50 * 1024 * 1024 },
  tempFileDir : '/usr/games/panel0/public/'
}));

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
  if (typeof req.session.user == 'undefined') {
    res.redirect("/login");
  }
  res.render("new_question.ejs");
})

app.get('/new_video', function(req, res) {
  if (typeof req.session.user == 'undefined') {
    res.redirect("/login");
  }
  res.render("new_video.ejs");
})


app.get('/delete_question', function(req, res) {
  if (typeof req.session.user == 'undefined') {
    res.redirect("/login");
  }
  Deleter.delete_where('Question', "QuestionID='" + req.query.id + "'", function(insert_result) {
    res.redirect("questions");
  });
})

app.get('/delete_package', function(req, res) {
  if (typeof req.session.user == 'undefined') {
    res.redirect("/login");
  }
  Deleter.delete_where('Package', "PackageID='" + req.query.id + "'", function(insert_result) {
    res.redirect("shop");
  });
})

app.post('/commit_question', function(req, res) {
  if (typeof req.session.user == 'undefined') {
    res.redirect("/login");
  }
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
  if (typeof req.session.user == 'undefined') {
    res.redirect("/login");
  }
  Insertor.insert_one('LotteryItem', ['Title','Type','Amount'],
    [req.body.title,req.body.type,req.body.amount],
    function(insert_result) {
      res.redirect("lottery");
    });
})

app.post('/commit_video', function(req, res) {
  if (typeof req.session.user == 'undefined') {
    res.redirect("/login");
  }
  console.log(req.files);
})

app.post('/commit_package', function(req, res) {
  if (typeof req.session.user == 'undefined') {
    res.redirect("/login");
  }
  Insertor.insert_one('Package', ['Title','Price','Quantity'],
    [req.body.title,req.body.price,req.body.quantity],
    function(insert_result) {
      res.redirect("shop");
    });
})


app.get('/questions', function(req, res) {
  if (typeof req.session.user == 'undefined') {
    res.redirect("/login");
  }
  Selector.select_all("Question", function(select_result) {
    var data = {
      "Questions": select_result
    };
    console.log(data);
    res.render("questions.ejs", data);
  });
})

app.get('/new_lottery', function(req, res) {
  if (typeof req.session.user == 'undefined') {
    res.redirect("/login");
  }
  res.render("new_lottery.ejs");
})

app.get('/new_package', function(req, res) {
  if (typeof req.session.user == 'undefined') {
    res.redirect("/login");
  }
  res.render("new_package.ejs");
})

app.get('/users', function(req, res) {
  if (typeof req.session.user == 'undefined') {
    res.redirect("/login");
  }
  Selector.select_all("User", function(select_result) {
    var data = {
      "Users": select_result
    };
    console.log(data);
    res.render("users.ejs", data);
  });
})

app.get('/lottery', function(req, res) {
  if (typeof req.session.user == 'undefined') {
    res.redirect("/login");
  }
  Selector.select_all("LotteryItem", function(select_result) {
    var data = {
      "LotteryItem": select_result
    };
    console.log(data);
    res.render("lottery.ejs", data);
  });
})


app.get('/shop', function(req, res) {
  if (typeof req.session.user == 'undefined') {
    res.redirect("/login");
  }
  Selector.select_all("Package", function(select_result) {
    var data = {
      "Packages": select_result
    };
    console.log(data);
    res.render("shop.ejs", data);
  });
})


app.get('/delete_lottery', function(req, res) {
  if (typeof req.session.user == 'undefined') {
    res.redirect("/login");
  }
  Deleter.delete_where('LotteryItem', "LotteryItemID='" + req.query.id + "'", function(insert_result) {
    res.redirect("lottery");
  });

})

app.get('/tokens', function(req, res) {
  if (typeof req.session.user == 'undefined') {
    res.redirect("/login");
  }
  Selector.select_all("ADSToken", function(select_result) {
    var data = {
      "Tokens": select_result
    };
    console.log(data);
    res.render("tokens.ejs", data);
  });
})

app.get('/edit_token', function(req, res) {
  if (typeof req.session.user == 'undefined') {
    res.redirect("/login");
  }
  Selector.select_all_where("ADSToken","ADSTokenID="+req.query.id, function(select_result) {
    var data = {
      "Token": select_result[0]
    };
    console.log(data);
    res.render("edit_tokens.ejs", data);
  });
})


app.get('/edit_package', function(req, res) {
  if (typeof req.session.user == 'undefined') {
    res.redirect("/login");
  }
  Selector.select_all_where("Package","packageID="+req.query.id, function(select_result) {
    var data = {
      "Package": select_result[0]
    };
    console.log(data);
    res.render("edit_package.ejs", data);
  });
})

app.post('/update_package', function(req, res) {
  if (typeof req.session.user == 'undefined') {
    res.redirect("/login");
  }
  Updater.update_where("Package",
  ['Title',"Quantity","Price"],[req.body.title,req.body.quantity,req.body.price],"PackageID="+req.body.id, function(select_result) {
    res.redirect("shop");
  });
})

app.post('/update_token', function(req, res) {
  if (typeof req.session.user == 'undefined') {
    res.redirect("/login");
  }
  Updater.update_where("ADSToken",
  ['Title',"Value"],[req.body.title,req.body.value],"ADSTokenID="+req.body.id, function(select_result) {
    res.redirect("tokens");
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
