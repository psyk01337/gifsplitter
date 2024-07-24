from fastapi import FastAPI, UploadFile, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import io
from PIL import Image, ImageSequence
import base64

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/split", response_class=HTMLResponse)
async def split_gif(request: Request, gif: UploadFile = Form(...), rows: int = Form(...), columns: int = Form(...)):
    try:
        gif_bytes = await gif.read()
        gif_image = Image.open(io.BytesIO(gif_bytes))

        frames = [frame.copy() for frame in ImageSequence.Iterator(gif_image)]
        width, height = gif_image.size
        grid_width = width // columns
        grid_height = height // rows

        output_paths = []
        for i in range(rows):
            for j in range(columns):
                new_frames = []
                for frame in frames:
                    cropped_frame = frame.crop((j * grid_width, i * grid_height, (j + 1) * grid_width, (i + 1) * grid_height))
                    new_frames.append(cropped_frame)

                # Save new frames to an in-memory byte stream
                output_gif_io = io.BytesIO()
                new_frames[0].save(output_gif_io, format='GIF', save_all=True, append_images=new_frames[1:], loop=0)
                output_gif_io.seek(0)

                # Encode the byte stream as base64
                output_gif_base64 = base64.b64encode(output_gif_io.read()).decode('utf-8')
                output_paths.append(output_gif_base64)

        return templates.TemplateResponse("index.html", {"request": request, "output_paths": output_paths, "rows": rows, "columns": columns})
    except Exception as e:
        return HTMLResponse(f"Error processing GIF: {e}", status_code=500)

