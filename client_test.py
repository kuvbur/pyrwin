# -*- coding: utf-8 -*-
import requests
import json
dic = {'13333':'q111'}
data = json.dumps(dic)
r = requests.get('http://tranquil-fortress-91903.herokuapp.com/state', data = data)