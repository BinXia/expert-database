# coding=UTF-8
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json
from apps import dbconn


# Create your views here.
def PullComboInfo(request):
	try:
		database = dbconn()
		cursor = database.cursor()
		respondData = list()

		cursor.execute('SELECT DISTINCT {0} FROM experts'.format(request.GET['type']))
		data = cursor.fetchall()
		respondData = map(lambda x:x[0],data)
		cursor.close()
		database.close()

		message = json.dumps(respondData);
		response = HttpResponse(message,content_type='application/json');
		response['Access-Control-Allow-Origin'] = '*';
		return response;

	except Exception, e:
		print e
		response = HttpResponse(json.dumps({"error":"Hey, man error!"}),content_type='application/json');
		response['Access-Control-Allow-Origin'] = '*';
		return response;







@csrf_exempt
def ShowExpertList(request):
	try:
		respondData = dict()
		search = dict()
		start = 0
		length = 0
		order = dict()
		columns = list()

		# load request from front end
		for key,value in json.loads(request.body).items():
			if key == 'search':
				search = value
			elif key == 'draw':
				respondData['draw'] = int(value)
			elif key == 'start':
				start = int(value)
			elif key == 'length':
				length = int(value)
			elif key == 'order':
				order = value[0]
			elif key == 'columns':
				columns = value


		database = dbconn()
		cursor = database.cursor()

		if len(search['value']) == 0:
			cursor.execute('SELECT {0},{1},{2},{3},{4},{5},{6},{7},{8} FROM experts ORDER BY CONVERT({9} USING gbk) {10}'.format(
				filter(lambda x:x['data']==0,columns)[0]['name'],
				filter(lambda x:x['data']==1,columns)[0]['name'],
				filter(lambda x:x['data']==2,columns)[0]['name'],
				filter(lambda x:x['data']==3,columns)[0]['name'],
				filter(lambda x:x['data']==4,columns)[0]['name'],
				filter(lambda x:x['data']==5,columns)[0]['name'],
				filter(lambda x:x['data']==6,columns)[0]['name'],
				filter(lambda x:x['data']==7,columns)[0]['name'],
				filter(lambda x:x['data']==8,columns)[0]['name'],
				filter(lambda x:x['data']==order['column'],columns)[0]['name'],
				order['dir']
				)
			)

			data = cursor.fetchall()
			respondData['recordsTotal'] = len(data)
			respondData['recordsFiltered'] = len(data)
			respondData['data'] = list()
			for datum in data[start:start+length]:
				respondData['data'].append(list(datum))

		else:
			cursor.execute('SELECT count(*) FROM experts')
			data = cursor.fetchall()
			respondData['recordsTotal'] = data[0]
			cursor.close()

			cursor = database.cursor()
			cursor.execute('SELECT {0},{1},{2},{3},{4},{5},{6},{7},{8} FROM experts WHERE CONCAT_WS(",",{0},{1},{2},{3},{4},{5},{6},{7},{8}) LIKE \'%{9}%\' ORDER BY CONVERT({10} USING gbk) {11}'.format(
				filter(lambda x:x['data']==0,columns)[0]['name'],
				filter(lambda x:x['data']==1,columns)[0]['name'],
				filter(lambda x:x['data']==2,columns)[0]['name'],
				filter(lambda x:x['data']==3,columns)[0]['name'],
				filter(lambda x:x['data']==4,columns)[0]['name'],
				filter(lambda x:x['data']==5,columns)[0]['name'],
				filter(lambda x:x['data']==6,columns)[0]['name'],
				filter(lambda x:x['data']==7,columns)[0]['name'],
				filter(lambda x:x['data']==8,columns)[0]['name'],
				search['value'].encode('UTF-8'),
				filter(lambda x:x['data']==order['column'],columns)[0]['name'],
				order['dir']
				)
			)
			data = cursor.fetchall()
			respondData['recordsFiltered'] = len(data)
			respondData['data'] = list()
			for datum in data:
				respondData['data'].append(list(datum))

		cursor.close()
		database.close()

		
		message = json.dumps(respondData);
		response = HttpResponse(message,content_type='application/json');
		response['Access-Control-Allow-Origin'] = '*';
		return response;

	except Exception, e:
		print e
		response = HttpResponse(json.dumps({"error":"Hey, man error!"}),content_type='application/json');
		response['Access-Control-Allow-Origin'] = '*';
		return response;