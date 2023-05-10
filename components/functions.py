import os
import importlib
import inspect

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