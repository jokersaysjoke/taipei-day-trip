import mysql.connector

dbconfig = {
    "user" : "root",
    "password" : "00000000",
    "host" : "localhost",
    "database" : "TAIPEI",
}
# create connection pool
connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name = "wehelp_pool",
    pool_size = 15,
    pool_reset_session = True,
    **dbconfig
)

