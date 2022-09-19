import shutil
import time
import io
from app.main import app
from fastapi.testclient import TestClient
from .config.settings import BASE_DIR, MEDIA_ROOT
from PIL import Image, ImageChops

client =  TestClient(app)

valid_img_extentions = ['png', 'jpeg', 'jpg']

def test_get_home():
    response = client.get("/")
    assert response.status_code == 200
    assert 'text/html' in response.headers['content-type']


def test_invalid_file_upload():
    response = client.post("/")
    assert response.status_code == 422
    assert "application/json" in response.headers['content-type']
   



def test_echo_upload():
    img_saved_path = BASE_DIR / "images"
    for path in img_saved_path.glob('*'):
        try:
            img = Image.open(path)
        except:
            img = None
        
        response = client.post("/img-echo/", files={"file": open(path, 'rb')})
        if img:
            assert response.status_code == 200
            r_stream = io.BytesIO(response.content)
            echo_img = Image.open(r_stream)
            difference = ImageChops.difference(echo_img, img).getbbox()
            assert difference is None

        else:
            assert response.status_code == 400
        

    # time.sleep(5)
    shutil.rmtree(MEDIA_ROOT)



def test_prediction_upload():
    img_saved_path = BASE_DIR / "images"
    for path in img_saved_path.glob('*'):
        try:
            img = Image.open(path)
        except:
            img = None
        
        response = client.post("/", files={"file": open(path, 'rb')})
        if img:
            assert response.status_code == 200
            data = response.json()
            assert len(data.keys()) == 2

        else:
            assert response.status_code == 400
        

    # time.sleep(5)
    shutil.rmtree(MEDIA_ROOT)

