# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 22:40:57 2018

@author: Jeru
"""
import requests
from json import JSONDecoder

http_url ="https://api-cn.faceplusplus.com/facepp/v3/detect"

key ="6Taq83cSyrNR6nBMVZTVEiGVh2qOdb9d"
secret ="7GVlL_KfmyuoR1KQaQ2li_I-s8aTbIQU"

attributes = "gender,age,beauty,ethnicity,emotion,smiling"
data = {"api_key":key, "api_secret":secret, "return_attributes":attributes}

def req_dict(files):
    response = requests.post(http_url, data=data, files=files)
    req_con = response.content.decode('utf-8')

    req_dict = JSONDecoder().decode(req_con)
    return req_dict

'''
#=== Usage ===#
filepath = "D:/dev/two_faces.jpg"
files = {"image_file":open(filepath, "rb")}
print(req_dict(files))
'''
