var mysql = require('mysql');
var connection = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: '2bacvvy',
  database: 'quiz'
});
connection.connect();


module.exports = {
  select_all: function(table, callback) {
    var query='SELECT * FROM '+table+';';
    console.log(query);
    connection.query(query , function(error, results, fields) {
      if (error) throw error;
      callback(results);
    });

  },

  update_where: function(table,cols,vals,where,callback) {

    var changes="";

    for (var i=0; i<cols.length;i++)
    {
      changes=changes+" "+cols[i]+"='"+vals[i]+"',";
    }

    changes=changes.substring(0, changes.length - 1);

    var query='UPDATE '+table+' SET'+changes+" WHERE "+where+";";
    console.log(query);
    connection.query(query , function(error, results, fields) {
      if (error) throw error;
      callback(results);
    });

  },


  ToShamsi: function() {
    return "HELLO";
  },

  ToPersianDigits: function() {
    return "Hola";
  }
};
