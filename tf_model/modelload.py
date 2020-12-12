import boto3, os
import numpy as np
import pandas as pd
from PIL import Image
from keras.models import load_model
from keras.preprocessing.image import load_img


# Lambda 내에 있는 환경변수로 설정
ACCESS_KEY = os.environ.get('ACCESS_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')

def downloadFromS3(strBucket, s3_path, local_path):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY
    )
    s3_client.download_file(strBucket, s3_path, local_path)


'''테스트중'''
def download_s3_object(strBucket, s3_path):
    import io
    file_obj = io.BytesIO()
    s3_client = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY
    )
    s3_client.download_fileobj(strBucket, s3_path, file_obj)
    return file_obj
'''테스트중'''

def uploadToS3(bucket, s3_path, local_path):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY
    )
    s3_client.upload_file(local_path, bucket, s3_path)


def pridict(img_local_path):
    # model = load_model('/tmp/cat_dog_small_cnn_model.h5')
    model = load_model('./cat_dog_small_cnn_model.h5')

    def cal_prob():    
        image_w = 150
        image_h = 150

        test_img_arr=[]
        print('=========== Loading images ===========')
        img = Image.open(img_local_path)
        img = img.convert("RGB")
        img = img.resize((image_w, image_h)) 
        # print(img.shape)
        data = np.asarray(img)
        data = data/255                
        test_img_arr.append(data)  
        test_img_arr = np.array(test_img_arr) 
        print('=========== Calculating probability ===========')
        result = model.predict(test_img_arr)
        print('model 완료, shape: {}'.format(result.shape))

        return result

    def score(s):
        if s >= 0.5:
            return 1
        else:
            return 0

    cal_result = cal_prob()

    df = pd.DataFrame({'path': img_local_path, 
                    'y': np.array([a for a in map(score, cal_result)]).ravel()}, 
                        columns = ['path','y']) 
    print(df)
    
def lambda_handler(event, context):
    bucket_name = event['Records'][0]['bucket']['name']
    file_path = event['Records'][0]['s3']['object']['key']
    file_name = file_path.split('/')[-1]
    
    '''테스트중'''
    pack2 = download_s3_object(bucket_name, 'pack2.zip')

    import zipfile
    zip_ref = zipfile.ZipFile(pack2)
    zip_ref.extractall('/tmp')
    zip_ref.close()

    import sys
    sys.path.append("/tmp")
    '''테스트중'''

    # 측정할 이미지 가져오기 & 쓰기
    downloadFromS3(bucket_name, file_path, '/tmp/'+file_name)
    # 학습된 모델 가져오기 & 쓰기
    downloadFromS3(bucket_name, 'cat_dog_small_cnn_model.h5', '/tmp/cat_dog_small_cnn_model.h5')
    # 파일 경로 전달
    pridict('/tmp/'+file_name)

# pridict('./dog.jpg')
