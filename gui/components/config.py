import json

class Config:
    def __init__(self, filepath="./config.json"):
        self.config = None
        with open(filepath) as f:
            str = f.read()
            self.config = json.loads(str)
    
    
    
    