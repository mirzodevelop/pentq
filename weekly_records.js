var mysql = require('mysql');
var sysql = require('sync-mysql');
var Deleter = require("./Deleter.js");
var Selector = require("./Selector.js");
var Insertor = require("./Insertor.js");
var Updater = require("./Updater.js");
const JDate = require('jalali-date');
const jdate = new JDate;

Selector.select_all("User", function(select_result) {
  for(var i=0; i<select_result.length;i++)
  {
    console.log(select_result[i]);

    Insertor.insert_one('WeeklyRecord', ['Score','UserName','WeekEndData'],
      [select_result[i].WeeklyScore,select_result[i].UserName,jdate.format('YYYY-MM-DD')],
      function(insert_result) {
        return "done!";
      });

  }

});
