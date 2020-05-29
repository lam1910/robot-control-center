from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.http import HttpResponse
from .models import Order

import psycopg2
import json

# for test environment on local machine only
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'USER': 'postgres',         # change username for your machine
            'PASSWORD': 'admin',        # change the password for your machine
            'HOST': 'localhost',
            'PORT': ' 5432',            # default port
            'NAME': 'ev3robotmanage',   # change name when you see fit
        }
    }

def index(request):
    return HttpResponse("Hello, world. You're at the control center index.")

def get_all_record(request):
    all_record_query = 'SELECT * FROM path;'

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

# all POST request must be csrf_exempt on this project
@csrf_exempt
def push_order(request):

    bad_request = {'Mode': 'Bad Request', 'Path': 'Bad Request', 'Move': 'Bad Request'}
    if request.method == 'POST':
        if 'start' in request.POST:
            a = request.POST['start']
            if 'finish' in request.POST:
                b = request.POST['finish']
            else:
                return HttpResponse(json.dumps(bad_request), status=400)
        else:
            return HttpResponse(json.dumps(bad_request), status=400)
        get_new_id = 'select id from control_center_order order by id desc LIMIT 1;'
        conn = psycopg2.connect(dbname=DATABASES['default']['NAME'], user=DATABASES['default']['USER'],
                                password=DATABASES['default']['PASSWORD'], host=DATABASES['default']['HOST'],
                                port=DATABASES['default']['PORT'])
        with conn.cursor() as cur:
            cur.execute(get_new_id)
            result = cur.fetchone()[0]
        conn.close()
        p = Order(id = result + 1, start = a, finish = b)
        p.save()

        return HttpResponse("Your response", status = 200)
    else:
        return HttpResponse(json.dumps(bad_request), status=400)

def get_path_auto(request):
    bad_request = {'Mode': 'Bad Request', 'Path': 'Bad Request', 'Move': 'Bad Request'}
    if 'start' in request.GET:
        start_pos = request.GET['start']
        # return value here
        return_dict = {'Mode': 'Auto'}
        select_request_incomplete = 'SELECT * FROM control_center_order WHERE status = \'incomplete\' ORDER BY id ' \
                                    'DESC LIMIT 1;'

        conn = psycopg2.connect(dbname=DATABASES['default']['NAME'], user=DATABASES['default']['USER'],
                                password=DATABASES['default']['PASSWORD'], host=DATABASES['default']['HOST'],
                                port=DATABASES['default']['PORT'])
        with conn.cursor() as cur:
            cur.execute(select_request_incomplete)
            tmp = cur.fetchone()
            this_pos, end_pos = tmp[0], tmp[2]

        with conn.cursor() as cur:
            cur.execute("SELECT * FROM path WHERE path.start=%s AND path.finish=%s;", (start_pos, end_pos))
            result = cur.fetchone()

        conn.close()
        return_dict['Path'] = result[2]
        return_dict['Move'] = result[3]
        return HttpResponse(json.dumps(return_dict), status=200)
    else:
        return HttpResponse(json.dumps(bad_request), status=400)


# the manual mode must be switched on both the server and the robot
def get_path_manual(request):
    bad_request = {'Mode': 'Bad Request', 'Path': 'Bad Request', 'Move': 'Bad Request'}
    if 'start' in request.GET:
        start_pos = request.GET['start']
        # return value here
        return_dict = {'Mode': 'Manual'}
        # TODO: add Path and Move field
    else:
        return HttpResponse(json.dumps(bad_request), status=400)

# TODO: on click for each button on manual mode