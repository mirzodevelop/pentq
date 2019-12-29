var mysql = require('mysql');
var sysql = require('sync-mysql');

var query="SET @rank=0, @score=-100; UPDATE User SET Rank=IF(@Score=(@Score:=Score), @Rank, @Rank:=@Rank+1) ORDER BY Score DESC;";
console.log(query);

var query2="SET @Weeklyrank=0, @Weeklyscore=-100; UPDATE User SET WeeklyRank=IF(@WeeklyScore=(@WeeklyScore:=WeeklyScore), @WeeklyRank, @WeeklyRank:=@WeeklyRank+1) ORDER BY WeeklyScore DESC;";
console.log(query2);

var connection = new sysql({
  host: 'localhost',
  user: 'root',
  password: '2bacvvy',
  database: 'quiz',
  charset : 'utf8',
  multipleStatements: true
});

const result = connection.query(query);
const result2 = connection.query(query2);

console.log(result);
console.log(result2);
