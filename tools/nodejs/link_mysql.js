//nodejs
var mod = 'C:/Users/zll/AppData/Roaming/npm/node_modules/'
var mysql = require(mod + 'mysql');
var connection = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    // password: 'zll211',
    password: '02dsH19',
    database: 'actor'
});

connection.connect();

var sql = 'show tables'
// var sql = 'source E:\\game\\common\\branch\\mojie\\config\\server\\sql\\account_default.sql'


connection.query(sql, function (error, results, fields) {
    if (error) throw error;
    console.log('The tables is: ', results[0]);
});