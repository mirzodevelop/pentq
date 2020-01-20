var mysql = require('mysql');
var sysql = require('sync-mysql');
var Deleter = require("./Deleter.js");
var Selector = require("./Selector.js");
var Insertor = require("./Insertor.js");
var Updater = require("./Updater.js");
const JDate = require('jalali-date');
const jdate = new JDate;

var args = process.argv;


    Selector.select_all("Hidden", function(select_result) {
      console.log(select_result[0].Value);
      if(select_result[0].Value==='Yes')
      {
        console.log("No Update Needed!");
      }
      else {

        Selector.select_all_where("Hidden","Tag='top_users_contest_end'", function(end_time) {
          console.log(end_time[0].Value);
        });

      }
    });
