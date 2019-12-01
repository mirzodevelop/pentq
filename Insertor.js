var mysql = require('mysql');
var connection = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: '2bacvvy',
  database: 'quiz',
  charset : 'utf8'
});
connection.connect();


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

    connection.query(query , function(error, results, fields) {
      if (error) throw error;
      callback(results);
    });

  },

  ToPersianDigits: function() {
    return "Hola";
  }
};
