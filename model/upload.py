from cmath import nan
from model.pool import pool
from mysql.connector import errors




class uploadModel:
    def databaseRecode(self, fileName, message, url):
        try:
            db = pool.get_connection()
            cursor = db.cursor(dictionary=True)
            cursor.execute( """INSERT INTO `messageBoard` ( fileName, message, `s3-URL`)VALUES ( %s, %s, %s);""",( fileName, message, url,))
            db.commit()
        except errors.Error as e:
            print("error",e)
        finally:
            cursor.close()
            db.close()

    def getHistory(self):
        try:
            db = pool.get_connection()
            cursor = db.cursor(dictionary=True)
            sql_search = "SELECT `id`,`fileName`, `message`, `s3-URL` FROM `messageBoard`;"
            cursor.execute(sql_search)
            result = cursor.fetchall()
            db.commit()
            return result
        except errors.Error as e:
            print("error",e)
        finally:
            cursor.close()
            db.close()

    def getNew(self, id):
        try:
            db = pool.get_connection()
            cursor = db.cursor(dictionary=True)
            sql_search = "SELECT `id`,`fileName`, `message`, `s3-URL` FROM `messageBoard` WHERE `id`= '%s';"%(int(id))
            cursor.execute(sql_search)
            result = cursor.fetchone()
            db.commit()
            return result
        except errors.Error as e:
            print("error",e)
        finally:
            cursor.close()
            db.close()

upload_Model=uploadModel()

# file.save('./static/tmp/'+filename)
# s3Client.upload_file(Filename='./static/tmp/' + filename,Bucket = 'jane-s3',Key = 'messageBoard/' + f"{uxiTimeStamp}-{filename}")
# os.remove('./static/tmp/'+filename)
