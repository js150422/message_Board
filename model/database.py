from modle.pool import pool
from mysql.connector import errors

def databaseRecode(fileName, message, url):
	try:
		db = pool.get_connection()
		cursor = db.cursor(dictionary=True)
		cursor.execute( """CREATE TABLE `messageBoard`(
						`id` bigint auto_increment,
						`fileName` varchar(255),
						`message` varchar(255),
						`s3-URL` varchar(255),
						PRIMARY KEY(`id`),
						INDEX (fileName)
					);""")
		result = cursor.fetchone()
		db.commit()
	except errors.Error as e:
		print("error",e)
	finally:
		cursor.close()
		db.close()