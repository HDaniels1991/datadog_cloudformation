import os
import requests


class Monitor:

    def __init__(self, api_key, app_key):
        self.base_url = 'https://api.datadoghq.eu/api/v1'
        self.headers = {
            'Content-Type': 'application/json',
            'DD-API-KEY': api_key,
            'DD-APPLICATION-KEY': app_key
        }

    def _create_query(self, functionname):
        query = 'sum(last_1h):avg:aws.lambda.errors{env:dev AND functionname:' + functionname.lower() + '}.as_count() > 0'
        return query 

    def create_monitor(self, name, message, priority, functionname, tags):
        url = os.path.join(self.base_url, 'monitor')
        data = {
            "name": name,
            "message": message,
            "priority": priority,
            "query": self._create_query(functionname),
            "tags": tags,
            "type": "query alert"
        }
        response = requests.post(url, headers=self.headers, json=data).json()
        return response['id']

    def update_monitor(self, monitor_id, name, message, priority, functionname, tags):
        url = os.path.join(self.base_url, f'monitor/{monitor_id}')
        data = {
            "name": name,
            "message": message,
            "priority": priority,
            "query": self._create_query(functionname),
            "tags": tags,
            "type": "query alert" 
        }
        response = requests.put(url, headers=self.headers, json=data).json()
        return response['id'] 

    def delete_monitor(self, monitor_id):
        url = os.path.join(self.base_url, f'monitor/{monitor_id}')
        response = requests.delete(url, headers=self.headers).json()
        return response