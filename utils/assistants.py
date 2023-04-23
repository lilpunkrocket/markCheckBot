import os

import requests
from urllib3 import disable_warnings, exceptions
from utils.config import settings

disable_warnings(exceptions.InsecureRequestWarning)

API = os.getenv('API')


async def get_token(login, password):
    response = requests.post(f'{API}/auth', headers={'token': ''},
                             verify=False,
                             data={'login': login, 'password': password})

    if response.status_code != 200:
        raise ValueError('Invalid username or password')

    return response.json()['message']


async def get_profile(token):
    profile = requests.get(f'{API}/student/profile', headers={'token': token,
                                                              'Host': 'mobile.rtsu.tj',
                                                              'Connection': 'Keep-Alive',
                                                              'Accept-Encoding': 'gzip',
                                                              'User-Agent': 'okhttp/3.12.0'},
                           verify=False, )
    return profile.json()


async def get_current_period(token):
    periods = requests.get(f'{API}/student/academic_years', headers={'token': token,
                                                                     'Host': 'mobile.rtsu.tj',
                                                                     'Connection': 'Keep-Alive',
                                                                     'Accept-Encoding': 'gzip',
                                                                     'User-Agent': 'okhttp/3.12.0'},
                           verify=False, )

    current_period = periods.json()[0]['ID']
    return current_period


async def get_grades(token):
    current_period = await get_current_period(token)
    grades = requests.get(f'{API}/student/grades/' + str(current_period),
                          headers={'token': token,
                                   'Host': 'mobile.rtsu.tj',
                                   'Connection': 'Keep-Alive',
                                   'Accept-Encoding': 'gzip',
                                   'User-Agent': 'okhttp/3.12.0'},
                          verify=False, )
    return grades.json()


async def get_subject(token, sub_id):
    grades = await get_grades(token)
    for sub in grades:
        if sub['SubjectID'] == sub_id:
            return sub
