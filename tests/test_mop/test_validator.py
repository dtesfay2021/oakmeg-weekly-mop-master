import pytest

from src.mop.validator import validate_project

def test_validate_project():
    
    vals_to_test = [
        'Oak - PRO-12766',
        'test',
        "'OR 1=1"
    ]
    
    for val in vals_to_test:
        validate_project(val)