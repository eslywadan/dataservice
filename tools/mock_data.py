import json


def get_mock_data(file_name='sample', type=json):
    if file_name == 'sample':
        dat = {
          'userid': 1,
          'id': 1,
          'title': 'Make the bed',
          'completed': False
        }
    
    return dat
    