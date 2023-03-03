from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from tempfile import NamedTemporaryFile, TemporaryDirectory
import shutil
import matplotlib.pyplot as plt
import io
import asyncio

import models as md
import methods as mt
import utils as ut

# keys for data are labels, values are floats collectively adding up to 100
def build_pie_chart(data:dict):
    labels = data.keys()
    sizes = data.values()
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%')
    ax.axis('equal')

    # Save the figure to a buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    return buffer

app = FastAPI()

origins = ["http://localhost", "http://localhost:4200"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/chordgen/custom-mode')
def custom_chordgen(req: md.CustomModeRequest):
  if len(req.mode) != 7:
    return {"error": "Invalid number of scale degrees"}, 400

  return mt.custom_chords(req.intention, req.mode)

@app.post('/chordgen/modes/{mode}')
def mode_chordgen(req: md.ModeRequest, mode):
  match mode:
    case md.Mode.major:
      return mt.major_chords(req.intention)
    case md.Mode.minor:
      return mt.minor_chords(req.intention)
    case md.Mode.dorian:
      return mt.dorian_chords(req.intention)
    case md.Mode.mixolydian:
      return mt.mixo_chords(req.intention)
    case _:
      raise HTTPException(status_code=400, detail="Invalid mode parameter")

@app.post('/pie-chart/{title}', response_class=FileResponse)
def pie_chart(data: dict, title: str):
    print(data, title)
    if sum(data.values()) != 100:
        raise HTTPException(status_code=400, detail="Data values must sum to 100")
    buffer = build_pie_chart(data)
    # Save the buffer to a temporary file
    with NamedTemporaryFile(delete=False) as f:
        f.write(buffer.getvalue())
        f.flush()
        # Return the file as a FileResponse
        headers = {"Content-Disposition": f"inline; filename={title}.png"}
        return FileResponse(f.name, media_type='image/png', filename=f'{title}.png', headers=headers)

@app.post('/api-gen/{title}', response_class=FileResponse)
async def api_gen(req: md.ApiGenRequest, title: str):
  with TemporaryDirectory() as temp_dir:
    mt.generate_api_code(req, temp_dir)
    zip_path = shutil.make_archive(title, 'zip', root_dir=temp_dir)
    response = FileResponse(zip_path, media_type="application/zip", filename=f"{title}.zip")
    loop = asyncio.get_running_loop()
    loop.create_task(ut.delete_file(zip_path, delay=2)) # change the delay as needed
    return response
    

  
    
