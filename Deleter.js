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
  delete_where: function(table, where, callback) {

    var query='DELETE FROM '+table+' WHERE '+ where + ';';
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
