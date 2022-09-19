import io
import pathlib
import uuid
import pytesseract
from fastapi import (
Request,
File, 
UploadFile,
HTTPException,
Depends)
from fastapi.responses import HTMLResponse, FileResponse
from PIL import Image

from .config.settings import (
    app, 
    templates, 
    MEDIA_ROOT)
from .config.base import Settings, get_settings


@app.get("/", response_class=HTMLResponse)
def home(request: Request, settings:Settings = Depends(get_settings)):
    print(settings)
    return templates.TemplateResponse("home.html", {"request":request})


@app.post("/img-echo/", response_class=FileResponse)
async def img_echo_view(file:UploadFile = File(...),  settings:Settings = Depends(get_settings)):
    if not settings.echo_active:
        raise  HTTPException(detail='invalid endpoint', status_code=400)
    MEDIA_ROOT.mkdir(exist_ok=True)
    bytes_str = io.BytesIO(await file.read())
    try:
        img = Image.open(bytes_str)
    except:
        raise  HTTPException(detail='invalid image', status_code=400)
    file_name = pathlib.Path(file.filename)
    fext = file_name.suffix # .jpg .txt
    dest = MEDIA_ROOT / f"{uuid.uuid1()}{fext}"
    img.save(dest)
    return dest


@app.post("/")
async def prediction_view(file:UploadFile = File(...),  settings:Settings = Depends(get_settings)):
    bytes_str = io.BytesIO(await file.read())
    try:
        img = Image.open(bytes_str)
    except:
        raise  HTTPException(detail='invalid image', status_code=400)
    preds = pytesseract.image_to_string(img)
    predictions = [x for x in preds.split('\n')]
    return {"results": predictions, "original": preds}
