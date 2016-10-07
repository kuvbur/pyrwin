# -*- coding: utf-8 -*-
import requests
import json
dic = {'key':'1212'}
data = json.dumps(dic)
r = requests.post('http://tranquil-fortress-91903.herokuapp.com/state', data = data)