from fastapi import FastAPI, File, UploadFile, HTTPException
from io import BytesIO
import face_recognition
import numpy as np

app = FastAPI()

def get_single_face_encoding(image_data, image_name):
    image = face_recognition.load_image_file(BytesIO(image_data))
    encodings = face_recognition.face_encodings(image)
    
    if len(encodings) == 0:
        raise ValueError(f"No face found in the {image_name}. Please pass a valid image.")
    if len(encodings) > 1:
        raise ValueError(f"Multiple faces found in the {image_name}. Please pass an image with a single face.")
    
    return np.array(encodings[0])

@app.post("/verify_faces/")
async def verify_faces(
    database_image: UploadFile = File(...),
    live_image: UploadFile = File(...)
):
    try:
        # Optional: Check if more than one file was uploaded per parameter - FastAPI handles single file uploads, so this is generally enforced.
        
        database_image_data = await database_image.read()
        live_image_data = await live_image.read()

        # Validate faces in each image
        database_encoding = get_single_face_encoding(database_image_data, "database image")
        live_encoding = get_single_face_encoding(live_image_data, "live image")

        # Compare and return result
        results = face_recognition.compare_faces([database_encoding], live_encoding)
        return {"matched": bool(results[0])}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))