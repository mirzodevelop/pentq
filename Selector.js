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
  select_all: function(table, callback) {
    var query='SELECT * FROM '+table+';';
    console.log(query);
    connection.query(query , function(error, results, fields) {
      if (error) throw error;
      callback(results);
    });

  },

  select_all_where: function(table, where, callback) {

    var query='SELECT * FROM '+table+' WHERE '+ where + ';';
    console.log(query);

    connection.query(query , function(error, results, fields) {
      if (error) throw error;
      callback(results);
    });
  },

  select_count_where: function(table, where, callback) {

    var query='SELECT Count(*) AS cnt FROM '+table+' WHERE '+ where + ';';
    console.log(query);

    connection.query(query , function(error, results, fields) {
      if (error) throw error;
      callback(results[0].cnt);
    });
  }

};
