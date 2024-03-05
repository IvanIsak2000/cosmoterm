import sqlalchemy
from pydantic import BaseModel

"""Sqlite бд для храния целей отправки"""

class Target():
    __tablename__ = 'target'

    name: str
    host: str
    port: int



def add_target(name, host, port):
    pass

def get_targets():
    class Target(BaseModel):
        id: int
        name: str
        host: str
        port: int
        
        ...
    
    #  fake data are: 
    return Target(id=0, name="jjodf", host='localhost', port=5008), Target(id=1, name="hjjhf", host='localhost', port=5008), Target(id=2, name='I', host='localhost', port=8000)

def remove_target():
    pass
