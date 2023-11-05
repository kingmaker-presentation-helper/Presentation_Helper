import firebase_admin
from firebase_admin import credentials, storage, auth, db
from PIL import Image

def login_firebase():
    cred = credentials.Certificate("presentation-helper-37f03-firebase-adminsdk-h8b0k-54cd2dfce0.json")
    print(cred)

    # Firebase database 연결
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://presentation-helper-37f03-default-rtdb.asia-southeast1.firebasedatabase.app/",
        'storageBucket': "presentation-helper-37f03.appspot.com"
                                })

def firebase_db_update(dir, value):
    cur = db.reference(dir)

    cur.update(value)

def firebase_storage_upload(file_type, file_name):
    bucket = storage.bucket()

    blob = bucket.blob(file_type + '/' + file_name)
    blob.upload_from_filename(file_name)

def firebase_storage_download(file_type, file_name):
    bucket = storage.bucket()

    blob = bucket.get_blob(file_type + '/' + file_name)
    blob.download_to_filename('download/' + file_type + "/" + file_name)


if __name__ == '__main__':

    login_firebase()

    # firebase_storage_upload('image', "test.png")
    firebase_storage_download('image', "test.png")

    # user_ref = db.reference('user')
    # user_data = user_ref.get()
    # print(user_data['이지해']['user_history'])
