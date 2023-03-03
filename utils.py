from typing import List, Union
from io import TextIOWrapper
import json
import models as md
import asyncio
import os

def generate_chunks (intent: str):
    # define intent string with spaces, punctuation, 
    # repeating characters,and capitalization removed
    lower_unique = []
    for char in intent:
        if char.isalpha() and lower_unique.__contains__(char.lower()) == False:
            lower_unique.append(char.lower())
    print('lower_unique', lower_unique)
    if len(lower_unique)<=16:
        return 'error: Intention contains too few unique characters. Please elaborate further.'
    #convert lower-case input to scale degrees using scale_degree_dict
    scale_degrees = []
    for char in lower_unique:
        scale_degrees.append(md.scale_degree_dict[char])
    print('scale_degrees', scale_degrees)

    # split scale degrees into four data chunks to be used as
    # chord generation vectors
    chunks = []
    for i in range(0, 16, 4):
        chunks.append(scale_degrees[i:i+4])
    print('chunks', chunks)
    return chunks

def validate_chunks(chunks: list[list[int]]):
    if len(chunks)!=4:
        return ValueError('not enough data chunks')
    
    for chunk in chunks:
        for i in range(4):
            if not 1<=int(chunk[i])<=7:
                return ValueError(f'{int(chunk[i])} is not in range 1-7')
    return chunks

def generate_chords(mode: List[int], intent: str):
    print('mode', mode)
    chunks = generate_chunks(intent)
    print(chunks)
    try:
        chunks = validate_chunks(chunks)
    except ValueError as e:
        return e
    # Create contrary motion by alternating max and min values
    # Subtract 1 from each to give valid array indices
    scale_degrees = [
        max(chunks[0])-1,
        min(chunks[1])-1,
        max(chunks[2])-1,
        min(chunks[3])-1
    ]
    print('scale_degrees', scale_degrees)
    # apply the chosen mode dictionary to the raw scale degrees
    chord_names = []
    for i in range(len(scale_degrees)):
        chord_names.append(mode[scale_degrees[i]])
    print('chord_names', chord_names)    
    return chord_names

def write_function(func: md.Func, f: TextIOWrapper):
    param_declarations = []
    if func.params!= None:
        for param in func.params:
            declaration = f"{param.name}"
            if param.type!= None:
                declaration += f": {param.type}"
            if param.init_null:
                declaration+= f" = None"    
            param_declarations.append(declaration)
    # assemble function declaration
    if len(param_declarations)>0:
        declaration_str = ", ".join(param_declarations).rstrip(", ")
        f.write(f"def {func.name}({declaration_str})")
    else:
        f.write(f"def {func.name}()")
    if func.return_type!= None:
        f.write(f" -> {func.return_type}")
    #close declaration
    f.write(":\n")
    #write each line of body with indentation
    for line in func.body:
        f.write(f"  {line}")
        f.write("\n")
    f.write("\n")

def write_import(imp: md.Import, f: TextIOWrapper):
    if imp.alias != None:
        f.write(f"import {imp.name} as {imp.alias}\n")
    elif imp.members != None:
        members_str = ", ".join(member for member in imp.members)
        f.write(f"from {imp.name} import {members_str}".rstrip(", "))
        f.write("\n")
    else:
        f.write(f"import {imp.name}\n")

async def delete_file(file_path: str, delay: int):
    await asyncio.sleep(delay)
    os.remove(file_path)

class SpecEncoder(json.JSONEncoder):
    _type_map = {
        md.Import: dict,
        md.Model: dict,
        md.MyEnum: dict,
        md.MyDict: dict,
        md.Ref: dict,
        md.Param: dict,
        md.Func: dict,
        md.Route: dict
    }

    def default(self, obj):
        obj_type = type(obj)
        if obj_type in self._type_map:
            return self._type_map[obj_type](obj)
        return super().default(obj)

