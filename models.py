from pydantic import BaseModel
from typing import List
from enum import Enum

# Dictionaries
scale_degree_dict = {
    "a": 1,
    "b": 2,
    "c": 3,
    "d": 4,
    "e": 5,
    "f": 6,
    "g": 7,
    "h": 1,
    "i": 2,
    "j": 3,
    "k": 4,
    "l": 5,
    "m": 6,
    "n": 7,
    "o": 1,
    "p": 2,
    "q": 3,
    "r": 4,
    "s": 5,
    "t": 6,
    "u": 7,
    "v": 1,
    "w": 2,
    "x": 3,
    "y": 4,
    "z": 5,
}

major = {
    0: 'C',
    1: 'Dm',
    2: 'Em',
    3: 'F',
    4: 'G',
    5: 'Am',
    6: 'Bdim7'
}

minor = {
    0: 'Am',
    1: 'Bdim7',
    2: 'C',
    3: 'Dm',
    4: 'E(m)',
    5: 'F',
    6: 'G'
}

dorian = {
    0: 'Dm',
    1: 'Em',
    2: 'F',
    3: 'G',
    4: 'Am',
    5: 'Bdim7',
    6: 'C'
}

mixolydian = {
    0: 'G',
    1: 'Am',
    2: 'Bdim7',
    3: 'C',
    4: 'Dm',
    5: 'Em',
    6: 'F'
}
# Enums
class Mode(str, Enum):
  major = 'major'
  minor = 'minor'
  dorian = 'dorian'
  mixolydian = 'mixolydian'

class RESTMethod(str, Enum):
  get = 'get'
  post = 'post'
  put = 'put'
  delete = 'delete'

class ContentType(str, Enum):
  json = 'application/json'
  txt = 'text/plain'
  html = 'text/html'
  png = 'image/png'
  jpg = 'image/jpeg'
  gif = 'image/gif'
  mp3 = 'audio/mpeg'
  wav = 'audio/wav'
  mp4 = 'video/mp4'
  py = 'text/x-python'
  js = 'application/javascript'
  multipart = 'multipart/form-data'
  zp = 'application/zip'
  


class Import(BaseModel):
  name: str
  main: bool = False
  methods: bool = False
  models: bool = False
  utils: bool = False
  alias: str|None = None
  members: List[str]|None = None

class Model(BaseModel):
  name: str
  struct: dict

class MyEnum(BaseModel):
  name: str
  type: str
  members: dict

class MyDict(BaseModel):
  name: str
  value: dict

class Ref(BaseModel):
  name: str
  ref: str
  list: bool = False
  items: List[str]|None = None

class Param(BaseModel):
  name: str
  type: str|None = None
  init_null: bool = False

class Func(BaseModel):
  name: str
  params: List[Param]|None = None
  return_type: str|None = None
  body: List[str]
  main: bool = False
  utils: bool = False
  handler: bool = False
  method:bool = False

class Route(BaseModel):
  path: str
  method: RESTMethod
  req_model: str|None = None
  req_body_type: ContentType = ContentType.json
  handler: Func
  res_model: Model|MyEnum|None = None
  res_body_type: ContentType = ContentType.json

class ModeRequest(BaseModel):
  intention: str

class CustomModeRequest(BaseModel):
  intention: str
  mode: List[str]

class ApiGenRequest(BaseModel):
  env_map: dict|None = None
  import_map: List[Import]|None = None
  func_map: List[Func]
  model_map: List[Model]|None = None
  enum_map: List[MyEnum]|None = None,
  dict_map: List[MyDict]|None = None,
  ref_map: List[Ref]|None = None,
  route_map: List[Route]

#Ref Lists
file_responses = [
  ContentType.mp3, 
  ContentType.mp4, 
  ContentType.wav, 
  ContentType.jpg, 
  ContentType.zp, 
  ContentType.png, 
  ContentType.gif, 
  ContentType.py, 
  ContentType.js
]  