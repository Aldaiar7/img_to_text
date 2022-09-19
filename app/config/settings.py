import pathlib
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

BASE_DIR = pathlib.Path(__file__).parent.parent
MEDIA_ROOT = BASE_DIR / "uploads"
MEDIA_ROOT.mkdir(exist_ok=True)

app = FastAPI()

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
