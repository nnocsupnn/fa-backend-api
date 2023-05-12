import os
import importlib
import inspect
import json
from fastapi import status
from fastapi.responses import Response
from sqlalchemy.ext.declarative import DeclarativeMeta

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
