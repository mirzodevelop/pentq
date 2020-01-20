var mysql = require('mysql');
var sysql = require('sync-mysql');
const delay = require('delay');

var connection = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: '2bacvvy',
  database: 'quiz',
  charset : 'utf8'
});



module.exports = {
  insert_one: function(table,cols,vals,callback) {

    var col=""
    var val=""

    for (var i=0; i<cols.length;i++)
    {
      col=col+cols[i]+",";
      val=val+"'"+vals[i]+"',"
    }

    col=col.substring(0, col.length - 1);
    val=val.substring(0, val.length - 1);

    var query='INSERT INTO '+table+'('+col+") VALUES ("+val+");";
    console.log(query);
    connection.connect();

    connection.query(query , function(error, results, fields) {

      connection.end();

      if (error) throw error;

      //connection.end();
      if (connection) connection.release()

      callback(results);
    });

  },

  s_insert_one: function(table,cols,vals) {

    var col=""
    var val=""

    for (var i=0; i<cols.length;i++)
    {
      col=col+cols[i]+",";
      val=val+"'"+vals[i]+"',"
    }

    col=col.substring(0, col.length - 1);
    val=val.substring(0, val.length - 1);

    var query='INSERT INTO '+table+'('+col+") VALUES ("+val+");";
    console.log(query);

    var connection = new sysql({
      host: 'localhost',
      user: 'root',
      password: '2bacvvy',
      database: 'quiz',
      charset : 'utf8'
    });

    const result = connection.query(query);
    //connection.end()
    return result

  },

  ToPersianDigits: function() {
    return "Hola";
  }
};
