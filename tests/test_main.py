import pytest

from src.main import main

def test_main():
    
    project = 'Oak - PRO-12766'
    s3_prefix = 'OAK/WEEKLY_MOP/'
    
    main(project, s3_prefix)
