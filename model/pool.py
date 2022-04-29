from mysql.connector import pooling
import yaml



with open("./test3.yaml", encoding='utf-8') as file:
    data = yaml.safe_load(file)
    password = data["password"]
    server = data["server"]


dbconfig={

}

pool=pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    host = server,
    port = 3306,
    user = 'user1',
    password = password,
    database = 'messageBoard'
)
