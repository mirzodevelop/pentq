var mysql = require('mysql');
var sysql = require('sync-mysql');

var query="UPDATE User SET DoneLottery='No', DoneRollCall='No' WHERE 1=1;";
console.log(query);

var connection = new sysql({
  host: 'localhost',
  user: 'root',
  password: '2bacvvy',
  database: 'quiz',
  charset : 'utf8',
  multipleStatements: true
});

const result = connection.query(query);

console.log(result);
