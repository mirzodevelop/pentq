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
const port = 80;

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
  key: 'kloche2323',
  secret: '1z5xdfgjkl5nbgmoht',
  resave: false,
  saveUninitialized: false,
  cookie: {
    expires: 600000
  }
}));

app.use(cookieParser());

app.post('/', function(req, res) {
  console.log(req.body);
  console.log(req.body.status);
  console.log(typeof req.body.status);

  if(req.body.status=="10" || req.body.status=='100' || req.body.status=='101')
  {
    console.log("==============================");
    console.log(req.body.order_id.substring(0, 3));
    console.log(req.body.order_id.split("000")[1]);
    Selector.select_all_where("Package", "PackageID='"+req.body.order_id.split("000")[1]+"'" , function(package_) {

      console.log(package_[0].Quantity);
      Selector.select_all_where("User", "UserID='"+req.body.order_id.substring(0, 3)+"'" , function(user_) {

        console.log(user_[0].UserID);

        Updater.update_where("User",
        ['AllowedPackageCount'],[user_[0].AllowedPackageCount+package_[0].Quantity],"UserID="+user_[0].UserID, function(select_result) {

          Selector.select_all_where("Invoice", "OrderID='"+req.body.order_id+"'" , function(select_result) {
            var id_to_confirm=select_result[0].HashID;
            console.log("HashID:");
            console.log(id_to_confirm);
            var options = {
              method: 'POST',
              url: 'https://api.idpay.ir/v1.1/payment/verify',
              headers: {
                'Content-Type': 'application/json',
                'X-API-KEY': '55812935-e7a6-49c6-b72c-a4422cb72a03',
                'X-SANDBOX': 0,
              },
              body: {
                'order_id': req.body.order_id,
                'id': id_to_confirm,
              },
              json: true,
            };

            console.log(options);


            request(options, function (error, response, body) {
              if (error) throw new Error(error);

              console.log(body);

              res.render("payres.ejs");

            });
         });


        //res.render("payres.ejs");

        });

      });
    });

    // Selector.select_all_where("Invoice", "OrderID='"+req.body.order_id+"'" , function(select_result) {
    //   var id_to_confirm=select_result[0].HashID;
    //   console.log("HashID:");
    //   console.log(id_to_confirm);
    //   var options = {
    //     method: 'POST',
    //     url: 'https://api.idpay.ir/v1.1/payment/verify',
    //     headers: {
    //       'Content-Type': 'application/json',
    //       'X-API-KEY': '55812935-e7a6-49c6-b72c-a4422cb72a03',
    //       'X-SANDBOX': 1,
    //     },
    //     body: {
    //       'id': id_to_confirm,
    //       'order_id': req.body.order_id,
    //     },
    //     json: true,
    //   };
    //
    //   request(options, function (error, response, body) {
    //     if (error) throw new Error(error);
    //
    //     console.log(body);
    //
    //     res.send(req.body.order_id);
    //
    //   });

  //  });


  }
  else {
    res.send("Problem in payment!");
  }
})

app.listen(port, () => console.log(`Example app listening on port ${port}!`))
