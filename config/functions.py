import os
import importlib
import inspect
from sqlalchemy.ext.declarative import DeclarativeMeta
from dotenv import dotenv_values
import re
from datetime import date, datetime


config = dotenv_values(".env")

def load_classes_from_folder(folder_path):
    class_list = []
    
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.py') and file_name != '__init__.py':
            module_name = file_name[:-3]
            module_path = os.path.join(folder_path, file_name)
            
            module = importlib.import_module(module_name)
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj):
                    class_list.append(obj)
    
    return class_list


def nullCheckingResponse(obj):
    return { "status": "404", "data": "None" } if len(obj) <= 0 else obj


def serialize_model(model):
    if isinstance(model.__class__, DeclarativeMeta):
        result = {}
        for column in model.__table__.columns:
            result[column.name] = getattr(model, column.name)

        for relation in model.__mapper__.relationships:
            related_obj = getattr(model, relation.key)
            if related_obj is not None:
                if relation.uselist:
                    result[relation.key] = [serialize_model(obj) for obj in related_obj]
                else:
                    result[relation.key] = serialize_model(related_obj)
        return result
    else:
        return None

def make_code_string(input_string):
    # Remove non-alphanumeric characters and convert spaces to underscores
    cleaned_string = re.sub(r'\W+', '', input_string).replace(' ', '_')

    # Ensure the resulting string starts with a letter
    if cleaned_string and not cleaned_string[0].isalpha():
        cleaned_string = 'A' + cleaned_string

    # Truncate the string to a desired length (e.g., 10 characters)
    code_string = cleaned_string[:10]

    # Convert the string to uppercase
    code_string = code_string.upper()

    return code_string

'''
Mapping Object

@param source the source of the object
@param dest the destination of the object
@return object
'''
def mapToObject(source, dest, sub1 = None, sub2 = None) -> any:
    objectResponse = dest()
    
    for field, value in vars(source).items():
        if type(value) in (int, float, str, bool, list, tuple, dict, date, datetime):
            if hasattr(objectResponse, field):
                setattr(objectResponse, field, value)
        elif sub1 != None:
            # Level 1
            sub1Property = sub1()
            for sub1Field, sub1Value in vars(value).items():
                if type(sub1Value) in (int, float, str, bool, list, tuple, dict, date, datetime):
                    if hasattr(sub1Property, sub1Field):
                        setattr(sub1Property, sub1Field, sub1Value)
                elif sub2 != None:
                    # Level 2
                    sub2Property = sub2()
                    for sub2Field, sub2Value in vars(sub1Value).items():
                        if hasattr(sub2Property, sub2Field):
                            setattr(sub2Property, sub2Field, sub2Value)
                            
                    if hasattr(objectResponse, sub1Value):
                        setattr(objectResponse, sub1Value, sub2Property)
                        
            if hasattr(objectResponse, field):
                setattr(objectResponse, field, sub1Property)
    
    return objectResponse