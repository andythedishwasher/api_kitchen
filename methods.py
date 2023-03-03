import os
import json
import utils as ut
import models as md

#chord generation API
def major_chords(intention: str):
    try:
        chords = ut.generate_chords(md.major, intention)
    except ValueError as e:
        return e
    return chords

def minor_chords(intention: str):
    try:
        chords = ut.generate_chords(md.minor, intention)
    except ValueError as e:
        return e
    return chords

def dorian_chords(intention: str):
    try:
        chords = ut.generate_chords(md.dorian, intention)
    except ValueError as e:
        return e
    return chords

def mixo_chords(intention: str):
    try:
        chords = ut.generate_chords(md.mixolydian, intention)
    except ValueError as e:
        return e
    return chords

def custom_chords(intention: str, custom_mode: dict[str, str]):
    try:
        chords = ut.generate_chords(custom_mode, intention)
    except ValueError as e:
        return e
    return chords

# API Generator API
def generate_models_py(req: md.ApiGenRequest, temp_dir: str) -> None:
    models_file_path = os.path.join(temp_dir, 'models.py')

    with open(models_file_path, 'w') as f:
        f.write('from pydantic import BaseModel\n')
        if req.enum_map!=None:
            f.write('from enum import Enum\n')
        if any(imp.models for imp in req.import_map):
            for imp in req.import_map:
                if imp.models:
                    ut.write_import(imp, f)
        f.write('\n')

        f.write('# Enums\n')
        for enum in req.enum_map:
            f.write(f'class {enum.name}({enum.type}, Enum):\n')
            for key_value in enum.members.items():
                key, value = key_value
                f.write(f'  {key} = "{value}"\n')

        f.write('# Models\n')
        for model in req.model_map:
            f.write(f'class {model.name}(BaseModel):\n')
            for key_value in model.struct.items():
                key, value = key_value
                f.write(f'  {key}: {value}\n')
            f.write('\n')

def generate_methods_py(req: md.ApiGenRequest, temp_dir: str) -> None:
    methods_file_path = os.path.join(temp_dir, 'methods.py')
    
    with open(methods_file_path, 'w') as f:
        for imp in req.import_map:
            if imp.methods:
                ut.write_import(imp, f)
        if req.model_map!=None:
            f.write('import models as md\n')
        if any(func.utils for func in req.func_map):
            f.write('import utils as ut\n')
        for func in req.func_map:
            if func.method:
                ut.write_function(func, f)

def generate_utils_py(req: md.ApiGenRequest, temp_dir: str) -> None:
    utils_file_path = os.path.join(temp_dir, 'utils.py')

    with open(utils_file_path, 'w') as f:
        for imp in req.import_map:
            if imp.utils:
                ut.write_import(imp, f)
        f.write('import models as md')
        f.write("\n")
        
        for func in req.func_map:
            if func.utils:
                ut.write_function(func, f)


def generate_main_py(req: md.ApiGenRequest, temp_dir: str) -> None:
    main_file_path = os.path.join(temp_dir, 'main.py')

    with open(main_file_path, 'w') as f:
        f.write('from fastapi import FastAPI, HTTPException\n')
        f.write('from fastapi.responses import FileResponse\n')
        f.write('from fastapi.middleware.cors import CORSMiddleware\n')
        if req.model_map!= None:
            f.write('import models as md\n')
        if any(func.method for func in req.func_map):
            f.write('import methods as mt\n')
        if req.env_map!=None:
            f.write('from dotenv import load_dotenv\n')
            f.write('load_dotenv()\n\n')
        for imp in req.import_map:
            if imp.main:
                ut.write_import(imp, f)
        f.write('\n')
        f.write('app = FastAPI()\n')
        f.write('app.add_middleware(CORSMiddleware, allow_origins=[\"*\"], allow_credentials=True, allow_methods=[\"*\"], allow_headers=[\"*\"])\n')

        for func in req.func_map:
            # if main is true, function will be included in main.py.
            # This is helpful for libraries like matplotlib that prefer to be imported
            # in the main thread directly.
            if func.main:
                ut.write_function(func, f)

        for route in req.route_map:
            file_responses = [md.ContentType.mp3, md.ContentType.mp4, md.ContentType.wav, md.ContentType.jpg, md.ContentType.zp, md.ContentType.png, md.ContentType.gif, md.ContentType.py, md.ContentType.js]
            match route.method:
                case md.RESTMethod.get:
                    f.write(f'@app.get("{route.path}"')
                case md.RESTMethod.post:
                    f.write(f'@app.post("{route.path}"')
                case md.RESTMethod.put:
                    f.write(f'@app.put("{route.path}"')
                case md.RESTMethod.delete:
                    f.write(f'@app.delete("{route.path}"')
            if file_responses.__contains__(route.res_body_type):
                f.write(', response_class=FileResponse')
                #close route decorator
            f.write(')\n')
            #write handler function
            ut.write_function(route.handler, f)
                    
def generate_env(req: md.ApiGenRequest, temp_dir: str):
    if req.env_map!= None: 
        env_file_path = os.path.join(temp_dir, '.env')
        with open(env_file_path, 'w') as f:
            for key_value in req.env_map.items():
                key, value = key_value
                f.write(f'{key}="{value}"\n')

def generate_json_spec(spec: md.ApiGenRequest, temp_dir: str):
    spec_file_path = os.path.join(temp_dir, 'spec.json')
    with open(spec_file_path, 'w') as f:
        f.write(json.dumps(dict(spec), indent=4, cls=ut.SpecEncoder))
        
def generate_api_code(req: md.ApiGenRequest, temp_dir: str):
    if req.env_map != None:
        generate_env(req, temp_dir)
    if req.model_map!= None:
        generate_models_py(req, temp_dir)
    if any(func.method for func in req.func_map):
        generate_methods_py(req, temp_dir)
    if any(func.utils for func in req.func_map):
        generate_utils_py(req, temp_dir)   
    generate_main_py(req, temp_dir)
    generate_json_spec(req, temp_dir)
