from datetime import date,datetime,time
from pydantic import BaseModel,ConfigDict,EmailStr,Field,field_validator
class BlogOut(BaseModel):
    id:int;title:str;slug:str;category:str|None=None;featured_image_url:str|None=None;tags:list[str]=[];views_count:int;published_at:datetime|None=None
    @field_validator('tags',mode='before')
    @classmethod
    def split_tags(cls,value):return [v.strip() for v in value.split(',') if v.strip()] if isinstance(value,str) else value
class BlogDetailOut(BlogOut):content:str;related_blogs:list[BlogOut]=[]
class EventOut(BaseModel):id:int;title:str;category:str;event_date:date;event_time:time;venue:str;image_url:str|None=None;description:str;registration_link:str|None=None;status:str
class FacultyOut(BaseModel):id:int;name:str;designation:str;specialization:str;email:EmailStr;phone:str;scholar_link:str|None=None;photo_url:str|None=None;bio:str
class GalleryOut(BaseModel):id:int;title:str;category:str;thumbnail_url:str|None=None;uploaded_at:datetime
class Page(BaseModel):total:int;page:int;limit:int;results:list
class ContactIn(BaseModel):name:str=Field(min_length=1,max_length=100);email:EmailStr;message:str=Field(min_length=10)
class TokenIn(BaseModel):email:EmailStr;password:str=Field(min_length=1)
class TokenOut(BaseModel):access_token:str;token_type:str='bearer';expires_in:int=3600
