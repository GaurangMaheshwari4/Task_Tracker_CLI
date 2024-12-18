import os
from datetime import datetime
import json

current_dir = os.path.dirname(os.path.abspath(__file__))

class CRUDUtils:
    file_path = os.path.join(current_dir, 'db', 'storage.json')
    db_path = os.path.join(current_dir, 'db')

    @classmethod
    def check_json_init(cls):
        if not os.path.exists(cls.file_path):
            os.makedirs(cls.db_path, exist_ok=True)
            with open(cls.file_path, 'w') as json_file:
                json.dump({}, json_file, indent=4) 

    @classmethod
    def read_json(cls):
        with open(cls.file_path, 'r') as json_file:
            data = json.load(json_file)
        return data
    
    @classmethod
    def write_json(cls, data):
        with open(cls.file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    @classmethod
    def add_task(cls, desc: str):
        # Initialising Json File
        cls.check_json_init()

        # Reading Content
        data = cls.read_json()

        # Setting counter
        current_counter = 1 if not len(data.get('task_list', {}).keys()) else data.get('counter', 0) + 1
        data['counter'] = current_counter

        # Adding task to task list
        current_id = str(current_counter)
        current_data = {
            'description': desc,
            'status': 'todo',
            'createdAt': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'updatedAt': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        data['task_list'] = data.get('task_list', {})
        data['task_list'][current_id] = current_data

        #Writing to Json file
        cls.write_json(data)

        return current_id
    
    @classmethod
    def update_task(cls, id: int, desc: str):
        # Initialising Json File
        cls.check_json_init()

        # Reading Content
        data = cls.read_json()

        # Updating Task Description if present
        if ('task_list' not in data.keys()) or ( str(id) not in data['task_list'].keys() ):
            return '[red]No Task with the given ID[/]'
        else:
            data['task_list'][str(id)]['description'] = desc
            data['task_list'][str(id)]['updatedAt'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        #Writing to Json file
        cls.write_json(data)

        return f'[green]Task with ID ({id}) updated[/]'
    
    @classmethod
    def delete_task(cls, id: int):
        # Initialising Json File
        cls.check_json_init()

        # Reading Content
        data = cls.read_json()

        # Deleting Task if present
        if ('task_list' not in data.keys()) or ( str(id) not in data['task_list'].keys() ):
            return '[red]No Task with the given ID[/]'
        else:
            data['task_list'].pop(str(id))

        # Writing to Json file
        cls.write_json(data)

        return f'[green]Task with ID ({id}) deleted[/]'
    
    @classmethod
    def update_task_status(cls, id: int, status: str):
        # Initialising Json File
        cls.check_json_init()

        # Reading Content
        data = cls.read_json()

        # Updating status of task if present
        if ('task_list' not in data.keys()) or ( str(id) not in data['task_list'].keys() ):
            return '[red]No Task with the given ID[/]'
        else:
            data['task_list'][str(id)]['status'] = status

        # Writing to Json file
        cls.write_json(data)

        return f'[green]Status of Task with ID ({id}) moved to {status}[/]'
    
    @classmethod
    def list_tasks(cls, status: str = 'All'):
        # Initialising Json File
        cls.check_json_init()

        # Reading Content
        data = cls.read_json()

        if ('task_list' not in data.keys()):
            data = []
        else: 
            data = [ {**value, 'id': key} for key, value in data['task_list'].items() if value['status'] == status or status == 'All' ]

        return data


