from fastapi import UploadFile, File, HTTPException, APIRouter
from fastapi.responses import Response
from PIL import Image
import io
from fastapi import FastAPI
from time import sleep

app = FastAPI()

@app.get("/")
def heartbeat():
    return {"message": "Estou vivo!"}

@app.post("/process-image")
async def process_image_endpoint(file: UploadFile = File(...)):
    
    image = Image.open(io.BytesIO(await file.read()))

    # Convert the image to black and white
    bw_image = image.convert("L")

    byte_arr = io.BytesIO()
    bw_image.save(byte_arr, format='PNG')
    byte_arr = byte_arr.getvalue()

    return Response(content=byte_arr, media_type="image/png")


