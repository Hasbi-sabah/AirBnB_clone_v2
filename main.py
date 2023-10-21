#!/usr/bin/python3
"""
 Test cities access from a state
"""
from models import storage
from models.state import State
from models.city import City

print(storage.search(State, id='0e391e25-dd3a-45f4-bce3-4d1dea83f3c7'))
