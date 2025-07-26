from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
import subprocess
import os
import uuid

app = FastAPI()

@app.get("/download")
def download_instagram_reel(url: str = Query(..., description="Instagram Reel URL")):
    # Unique file name to prevent conflicts
    output_filename = f"{uuid.uuid4()}.mp4"
    output_path = f"/tmp/{output_filename}"  # Temporary directory

    try:
        # Download using yt-dlp
        command = [
            "yt-dlp",
            "-o", output_path,
            url
        ]
        subprocess.run(command, check=True)

        # Send the file back
        return FileResponse(output_path, media_type="video/mp4", filename="reel.mp4")

    except subprocess.CalledProcessError:
        raise HTTPException(status_code=400, detail="Failed to download reel. Invalid link or private content.")
    finally:
        # Optional: Clean up file after response (for production use a background task)
        pass
