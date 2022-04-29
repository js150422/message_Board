from model.upload import upload_Model
from flask import *
import boto3
import botocore
import time
import yaml




fileUpload = Blueprint('fileUpload', __name__)

with open("./test3.yaml", encoding='utf-8') as file:
    data = yaml.safe_load(file)
    regionData = data["region"]
    ACCESS_KEY = data["aws_access_key_id"]
    SECRET_KEY = data["aws_secret_access_key"]





fileUpload = Blueprint('fileUpload', __name__)


@fileUpload.route('/api/upload' ,methods=["POST"])
def upload():
    try:
        uxiTime = time.gmtime() # 取得時間元組
        uxiTimeStamp = int(time.mktime(uxiTime)) # 將時間員組轉成時間戳
        #-------------------------------資料抓取------------------------------
        file = request.files.get("files")
        fileName = request.form["name"]
        message = request.form["message"]
        content_type = request.mimetype
        #-------------------------------s3新增------------------------------
        s3Client = boto3.client('s3', region_name=regionData, aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
        s3Client.put_object(Body=file,Bucket='jane-s3',Key='messageBoard/' + f"{uxiTimeStamp}-{fileName}",ContentType=content_type)
        #-------------------------------s3核對------------------------------
        s3Resource = boto3.resource('s3', region_name=regionData, aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
        bucket = s3Resource.Bucket('jane-s3')
        bucketList = list(bucket.objects.filter(Prefix='messageBoard/'))
        lastQ = len(bucketList) - 1
        #-------------------------------s3資料確認新增成功&失敗------------------------------
        if bucketList[lastQ].key ==  'messageBoard/'+f"{uxiTimeStamp}-{fileName}":
            url = 'https://jane-s3.s3.amazonaws.com/messageBoard/'+f"{uxiTimeStamp}-{fileName}"
            result = upload_Model.databaseRecode(fileName, message, url)
            if result=="error":
                return jsonify({"error":True,"message":"伺服器錯誤"}),500
            else:
                return {'ok':True}
        else:
            return jsonify({"error":True,"message":"資料庫新增錯誤"})
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("物件不存在")
        else:
            raise


@fileUpload.route('/api/history')
def history():
    result=upload_Model.getHistory()
    if result=="error":
        return jsonify({"error":True,"message":"伺服器錯誤"}),500
    elif result==[]:
        return jsonify({"error":"沒有歷史資料"})
    else:
        return jsonify({"record":result})

@fileUpload.route('/api/newRecord/<id>')
def newUpload(id):
    result=upload_Model.getNew(id)
    if result=="error":
        return jsonify({"error":True,"message":"伺服器錯誤"}),500
    elif result==[]:
        return jsonify({"error":True,"message":"新增錯誤"})
    else:
        return jsonify({"record":result})
