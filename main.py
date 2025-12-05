from fastapi import FastAPI, File, UploadFile, Response
from rembg import remove
from PIL import Image
import io
import uvicorn
import os

app = FastAPI(
    title="Clothing Brand Background Remover",
    description="An API to remove backgrounds from clothing images using U2NET."
)

@app.get("/")
def read_root():
    return {"message": "Background Remover API is running. POST to /remove-background to use it."}

@app.post("/remove-background")
async def remove_background(file: UploadFile = File(...)):
    """
    Upload an image file, and this endpoint will return the image
    with the background removed (transparent PNG).
    """
    # Read the image file uploaded by the user
    image_data = await file.read()
    
    # Process the image using rembg
    # rembg expects bytes and returns bytes
    output_data = remove(image_data)

    # Return the processed image as a response
    return Response(content=output_data, media_type="image/png")

if __name__ == "__main__":
    # Get port from environment variable (required for Railway)
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)