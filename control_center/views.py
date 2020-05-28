from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

import psycopg2
import json

def index(request):
    return HttpResponse("Hello, world. You're at the control center index.")

def get_all_record(request):
    all_record_query = 'SELECT * FROM path;'
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'USER': 'postgres',
            'PASSWORD': 'admin',
            'HOST': 'localhost',
            'PORT': ' 5432',
            'NAME': 'ev3robotmanage',
        }
    }

    result_all = {'all': []}
    conn = psycopg2.connect(dbname = DATABASES['default']['NAME'], user = DATABASES['default']['USER'],
                            password = DATABASES['default']['PASSWORD'], host = DATABASES['default']['HOST'],
                            port = DATABASES['default']['PORT'])
    with conn.cursor() as cur:
        cur.execute(all_record_query)
        result = cur.fetchall()
        for row in result:
            result_all['all'].append({'start': row[0], 'finish': row[1], 'path': row[2], 'direction': row[3]})
    conn.close()

    return HttpResponse(json.dumps(result_all), content_type='application/json', status=200)

def get_path_auto(request):
    bad_request = {'Mode': 'Bad Request', 'Path': 'Bad Request', 'Move': 'Bad Request'}
    if 'start' in request.GET:
        start_pos = request.GET['start']
        # return value here
        return_dict = {'Mode': 'Auto'}
        # TODO: add Path and Move field
        # TODO: query here
    else:
        return HttpResponse(json.dumps(bad_request), status=400)


def get_path_manual(request):
    bad_request = {'Mode': 'Bad Request', 'Path': 'Bad Request', 'Move': 'Bad Request'}
    if 'start' in request.GET:
        start_pos = request.GET['start']
        # return value here
        return_dict = {'Mode': 'Manual'}
        # TODO: add Path and Move field
        # TODO: query here
    else:
        return HttpResponse(json.dumps(bad_request), status=400)
