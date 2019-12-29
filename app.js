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
const readXlsxFile = require('read-excel-file/node');
var XLSX = require('xlsx');
const delay = require('delay');


var Deleter = require("./Deleter.js");
var Selector = require("./Selector.js");
var Insertor = require("./Insertor.js");
var Updater = require("./Updater.js");

var Iconv = require('iconv').Iconv;
var iconv = new Iconv('UTF-8', 'ISO-8859-1');

const utf8 = require('utf8');

function getRandomInt(max) {
  return Math.floor(Math.random() * Math.floor(max));
}

//configs
const port = 8888;

app.set('views', __dirname + '/views');
app.use(express.static(__dirname + '/public'));

app.use(fileUpload({
  useTempFiles : true,
  limits: { fileSize: 50 * 1024 * 1024 },
  tempFileDir : '/usr/games/panel0/public/videos/',
  preserveExtension:true
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

app.get('/delete_request', function(req, res) {
  if (typeof req.session.user == 'undefined') {
    res.redirect("/login");
  }
  Deleter.delete_where('MoneyRequest', "MoneyRequestID='" + req.query.id + "'", function(insert_result) {
    res.redirect("requests");
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
  fs.rename(req.files.video.tempFilePath, req.files.video.tempFilePath+'.'+req.files.video.name.split(".")[1], function(err) {
    if ( err ) console.log('ERROR: ' + err);

    Insertor.insert_one('Video', ['Title','Address'],
      [req.body.title,req.files.video.tempFilePath.replace("/usr/games/panel0/public","http://136.243.86.145:8888")+'.'+req.files.video.name.split(".")[1]],
      function(insert_result) {
        res.redirect("/videos");
      });
  });
})


app.post('/commit_banner', function(req, res) {
  if (typeof req.session.user == 'undefined') {
    res.redirect("/login");
  }
  console.log(req.files);
  fs.rename(req.files.video.tempFilePath, req.files.video.tempFilePath+'.'+req.files.video.name.split(".")[1], function(err) {
    if ( err ) console.log('ERROR: ' + err);

    Insertor.insert_one('Image', ['Title','Address'],
      [req.body.title,req.files.video.tempFilePath.replace("/usr/games/panel0/public","http://136.243.86.145:8888")+'.'+req.files.video.name.split(".")[1]],
      function(insert_result) {
        res.redirect("/banners");
      });
  });
})

app.post('/commit_excel', function(req, res) {
  if (typeof req.session.user == 'undefined') {
    res.redirect("/login");
  }
  console.log(req.files);
  fs.rename(req.files.excel.tempFilePath, req.files.excel.tempFilePath+'.'+req.files.excel.name.split(".")[1], function(err) {
    if ( err ) console.log('ERROR: ' + err);


    var workbook = XLSX.readFile(req.files.excel.tempFilePath+'.'+req.files.excel.name.split(".")[1]);
    var sheet_name_list = workbook.SheetNames;
    xlData = XLSX.utils.sheet_to_json(workbook.Sheets[sheet_name_list[0]]);

    console.log(xlData);
    var prom=4;

      for(var i=0;i<xlData.length;i++)
      {
        if(xlData.length-1 ==i){
        res.redirect("questions");
        }

        console.log(i);
        line=xlData[i];
        console.log("********");
        console.log(line);

        var xres=Insertor.s_insert_one('Question', ['QuestionStatement', 'OrderNum', 'QuestionType', 'ContestID', 'Prize', 'AnswerTime', 'IsSaftyLevel'],
          [xlData[i]["Stetement"], i, 'MultipleChoice',"1","15","10","No"]);

        console.log("XXXXXXXXX:");
        console.log(xres['insertId']);

        qunum=xres['insertId'];

        var trueans=getRandomInt(4);

        c0=line["choice1"];
        c1=line["choice2"];
        c2=line["choice3"];
        c3=line["choice4"];

        if(trueans==1)
        {
          c0=line["choice2"];
          c1=line["choice1"];
          c2=line["choice4"];
          c3=line["choice3"];
        }
        if(trueans==2)
        {
          c0=line["choice2"];
          c1=line["choice4"];
          c2=line["choice1"];
          c3=line["choice3"];
        }

        if(trueans==3)
        {
          c0=line["choice2"];
          c1=line["choice4"];
          c2=line["choice3"];
          c3=line["choice1"];
        }

        Insertor.insert_one('Choice', ['QuestionID', 'Title', 'IsTrue'], [qunum, c0, (trueans == 0) ? "Yes" : "No"], function(res_) {
            });
        Insertor.insert_one('Choice', ['QuestionID', 'Title', 'IsTrue'], [qunum, c1, (trueans == 1) ? "Yes" : "No"], function(res_) {
            });
        Insertor.insert_one('Choice', ['QuestionID', 'Title', 'IsTrue'], [qunum, c2, (trueans == 2) ? "Yes" : "No"], function(res_) {
            });
        Insertor.insert_one('Choice', ['QuestionID', 'Title', 'IsTrue'], [qunum, c3, (trueans == 3) ? "Yes" : "No"], function(res_) {
            });

      }

  });
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


app.get('/banners', function(req, res) {
  if (typeof req.session.user == 'undefined') {
    res.redirect("/login");
  }
  Selector.select_all("Image", function(select_result) {
    var data = {
      "Images": select_result
    };
    console.log(data);
    res.render("banners.ejs", data);
  });
})

app.get('/new_excel', function(req, res) {
  if (typeof req.session.user == 'undefined') {
    res.redirect("/login");
  }
  res.render("new_excel.ejs");
})

app.get('/new_banner', function(req, res) {
  if (typeof req.session.user == 'undefined') {
    res.redirect("/login");
  }
  res.render("new_banner.ejs");
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

app.get('/delete_user', function(req, res) {
  if (typeof req.session.user == 'undefined') {
    res.redirect("/login");
  }
  Deleter.delete_where('User', "UserID='" + req.query.id + "'", function(insert_result) {
    res.redirect("users");
  });

})


app.get('/delete_banner', function(req, res) {
  if (typeof req.session.user == 'undefined') {
    res.redirect("/login");
  }
  Deleter.delete_where('Image', "ImageID='" + req.query.id + "'", function(insert_result) {
    res.redirect("banners");
  });
})

app.get('/delete_video', function(req, res) {
  if (typeof req.session.user == 'undefined') {
    res.redirect("/login");
  }
  Deleter.delete_where('Video', "VideoID='" + req.query.id + "'", function(insert_result) {
    res.redirect("videos");
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

app.get('/videos', function(req, res) {
  if (typeof req.session.user == 'undefined') {
    res.redirect("/login");
  }
  Selector.select_all("Video", function(select_result) {
    var data = {
      "Videos": select_result
    };
    console.log(data);
    res.render("videos.ejs", data);
  });
})

app.get('/options', function(req, res) {
  if (typeof req.session.user == 'undefined') {
    res.redirect("/login");
  }
  Selector.select_all("OptionParameter", function(select_result) {
    var data = {
      "Options": select_result
    };
    console.log(data);
    res.render("options.ejs", data);
  });
})

app.get('/requests', function(req, res) {
  if (typeof req.session.user == 'undefined') {
    res.redirect("/login");
  }
  Selector.select_all("MoneyRequest", function(select_result) {
    var data = {
      "Requests": select_result
    };
    console.log(data);
    res.render("requests.ejs", data);
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


app.get('/edit_user', function(req, res) {
  if (typeof req.session.user == 'undefined') {
    res.redirect("/login");
  }
  Selector.select_all_where("User","USerID="+req.query.id, function(select_result) {
    var data = {
      "User": select_result[0]
    };
    console.log(data);
    res.render("edit_user.ejs", data);
  });
})


app.get('/edit_request', function(req, res) {
  if (typeof req.session.user == 'undefined') {
    res.redirect("/login");
  }
  Selector.select_all_where("MoneyRequest","MoneyRequestID="+req.query.id, function(select_result) {
    var data = {
      "MoneyRequest": select_result[0]
    };
    console.log(data);
    res.render("edit_request.ejs", data);
  });
})


app.get('/edit_option', function(req, res) {
  if (typeof req.session.user == 'undefined') {
    res.redirect("/login");
  }
  Selector.select_all_where("OptionParameter","OptionParameterID="+req.query.id, function(select_result) {
    var data = {
      "Option": select_result[0]
    };
    console.log(data);
    res.render("edit_options.ejs", data);
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

app.get('/edit_question', function(req, res) {
  if (typeof req.session.user == 'undefined') {
    res.redirect("/login");
  }
  Selector.select_all_where("Question","QuestionID="+req.query.id, function(select_result) {
    Selector.select_all_where("Choice","QuestionID="+req.query.id, function(select_results) {
    var data = {
      "Question": select_result[0],
      "Choices":select_results
    };
    console.log(data);
    res.render("edit_question.ejs", data);
  });
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


app.post('/update_request', function(req, res) {
  if (typeof req.session.user == 'undefined') {
    res.redirect("/login");
  }
  Updater.update_where("MoneyRequest",
  ['AccountName',"BankAccount","Amount"],[req.body.name,req.body.bank,req.body.amount],"MoneyRequestID="+req.body.id, function(select_result) {
    res.redirect("requests");
  });
})

app.post('/update_user', function(req, res) {
  if (typeof req.session.user == 'undefined') {
    res.redirect("/login");
  }
  Updater.update_where("User",
  ['UserName',"DisplayName","Balance","PhoneNumber","Score","WeeklyScore","AllowedPackageCount"],[req.body.uname,req.body.dname,req.body.balance,req.body.phone,req.body.score,req.body.weekly,req.body.allowed],"UserID="+req.body.id, function(select_result) {
    res.redirect("users");
  });
})

app.post('/update_question', function(req, res) {
  if (typeof req.session.user == 'undefined') {
    res.redirect("/login");
  }
  Updater.update_where("Question",
  ['QuestionStatement'],[req.body.statement],"QuestionID="+req.body.id, function(select_result) {
    Updater.update_where("Choice",
    ['Title'],[req.body.c1],"ChoiceID="+req.body.qid1, function(select_result) {
      Updater.update_where("Choice",
      ['Title'],[req.body.c2],"ChoiceID="+req.body.qid2, function(select_result) {
        Updater.update_where("Choice",
        ['Title'],[req.body.c3],"ChoiceID="+req.body.qid3, function(select_result) {
          Updater.update_where("Choice",
          ['Title'],[req.body.c4],"ChoiceID="+req.body.qid4, function(select_result) {
            res.redirect("questions");
          });
        });
      });
    });
  });
})

app.get('/paid', function(req, res) {
  if (typeof req.session.user == 'undefined') {
    res.redirect("/login");
  }
  Updater.update_where("MoneyRequest",
  ['Estate'],["Paid"],"MoneyRequestID="+req.query.id, function(select_result) {
    res.redirect("requests");
  });
})

app.get('/suspend', function(req, res) {
  if (typeof req.session.user == 'undefined') {
    res.redirect("/login");
  }
  Updater.update_where("MoneyRequest",
  ['Estate'],["Suspended"],"MoneyRequestID="+req.query.id, function(select_result) {
    res.redirect("requests");
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

app.post('/update_option', function(req, res) {
  if (typeof req.session.user == 'undefined') {
    res.redirect("/login");
  }
  Updater.update_where("OptionParameter",
  ['Title',"Value","Tag"],[req.body.title,req.body.value,req.body.tag],"OptionParameterID="+req.body.id, function(select_result) {
    res.redirect("options");
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
