from dataclasses import dataclass

@dataclass
class Hosts:
    def __init__(self, env):
        self.demoqa = {
            'local': 'localhost:5555',
            'test': 'http://your_test_demoqa_env.com',
            'prod': 'https://demowebshop.tricentis.com',
        }[env]
        self.reqres = {
            'local': 'localhost:5555',
            'test': 'http://your_test_env.com',
            'prod': 'https://reqres.in/api',
        }[env]
