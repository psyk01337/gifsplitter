from fastapi import FastAPI, UploadFile, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import io
from PIL import Image, ImageSequence
import base64

# Initialize the FastAPI app
app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates directory
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    """
    Serve the main HTML form for uploading and splitting GIFs.

    Args:
        request (Request): The request object.

    Returns:
        TemplateResponse: The HTML form template.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/split", response_class=HTMLResponse)
async def split_gif(request: Request, gif: UploadFile = Form(...), rows: int = Form(...), columns: int = Form(...)):
    """
    Split the uploaded GIF into a grid of smaller GIFs.

    Args:
        request (Request): The request object.
        gif (UploadFile): The uploaded GIF file.
        rows (int): The number of rows to split the GIF into.
        columns (int): The number of columns to split the GIF into.

    Returns:
        TemplateResponse: The HTML template with the split GIFs.
        HTMLResponse: Error message if GIF processing fails.
    """
    try:
        # Read the uploaded GIF file
        gif_bytes = await gif.read()
        gif_image = Image.open(io.BytesIO(gif_bytes))

        # Extract frames from the GIF
        frames = [frame.copy() for frame in ImageSequence.Iterator(gif_image)]
        width, height = gif_image.size
        grid_width = width // columns
        grid_height = height // rows

        output_paths = []

        # Process each grid cell
        for i in range(rows):
            for j in range(columns):
                new_frames = []
                for frame in frames:
                    cropped_frame = frame.crop(
                        (
                            j * grid_width,
                            i * grid_height,
                            (j + 1) * grid_width,
                            (i + 1) * grid_height
                        )
                    )
                    new_frames.append(cropped_frame)

                # Save new frames to an in-memory byte stream
                output_gif_io = io.BytesIO()
                new_frames[0].save(
                    output_gif_io,
                    format='GIF',
                    save_all=True,
                    append_images=new_frames[1:],
                    loop=0
                )
                output_gif_io.seek(0)

                # Encode the byte stream as base64
                output_gif_base64 = base64.b64encode(output_gif_io.read()).decode('utf-8')
                output_paths.append(output_gif_base64)

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "output_paths": output_paths,
                "rows": rows,
                "columns": columns
            }
        )
    except Exception as e:
        return HTMLResponse(f"Error processing GIF: {e}", status_code=500)
