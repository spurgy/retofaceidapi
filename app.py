from io import BytesIO
from fastapi import FastAPI, File, UploadFile, HTTPException
import face_recognition
import numpy as np

app = FastAPI(title="Face Recognition API")

# Threshold for deciding if two faces are the same
DEFAULT_THRESHOLD = 0.6

def get_single_face_encoding(image_bytes: bytes, image_name: str) -> np.ndarray:
    """
    Load an image and return the encoding for a single detected face.
    Raise ValueError if none or multiple faces are found.
    """
    try:
        image = face_recognition.load_image_file(BytesIO(image_bytes))
    except Exception as e:
        raise ValueError(f"Could not load {image_name}: {e}")

    encodings = face_recognition.face_encodings(image)

    if len(encodings) == 0:
        raise ValueError(f"No face found in the {image_name}. Please upload a valid image.")
    if len(encodings) > 1:
        raise ValueError(f"Multiple faces found in the {image_name}. Please upload an image with a single face.")

    return np.array(encodings[0])

@app.get("/")
def root():
    return {"message": "Face Recognition API is running!"}

@app.post("/verify_faces/")
async def verify_faces(
    database_image: UploadFile = File(...),
    live_image: UploadFile = File(...)
):
    try:
        # Read image bytes
        db_bytes = await database_image.read()
        live_bytes = await live_image.read()

        # Extract face encodings
        db_encoding = get_single_face_encoding(db_bytes, "database image")
        live_encoding = get_single_face_encoding(live_bytes, "live image")

        # Compute distance
        distance = float(face_recognition.face_distance([db_encoding], live_encoding)[0])
        matched = distance <= DEFAULT_THRESHOLD

        return {
            "matched": matched,
            "distance": distance,
            "threshold": DEFAULT_THRESHOLD
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")