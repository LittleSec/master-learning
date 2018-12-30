## Branch: release-branch
## 对比_0.py修改的地方：
# dataInfo --> dI
# np --> numpy (delete import numpy as np)
# DEPTH_LIST : list --> tuple

from flask import Flask, redirect, render_template, url_for
from flask import jsonify, request, json
from datetime import timedelta
import os
import pandas as pd
from scipy.signal import argrelextrema
import time
app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)  # 将缓存最大时间设置为1s

@app.route('/')
def hello_world():
    return render_template('layer.html')

# 以下是api，供前端ajax调用
# 以下变量用于合法性检查，暂时无用
ROOTPATH = './oceandata'  # 路径和文件名规律: ./oceandata/depth/2014-07-01.csv
SSH_GRID_PATH = 'surf_el_grid'
DEPTH_DEFAULT = '0.0m'  # 默认深度
DEPTH_LIST = ('0.0m', '8.0m', '15.0m', '30.0m', '50.0m')
OWMAGNITUDE = 1e10

def cmpGreater(a, b):
    return a > b

def cmpLess(a, b):
    return a < b

def eddyBoundary(centerI, centerJ, lonList, latList, threshold, srcSSH, eddyType):
    '''
    已知ssh阈值求八个方向阈值所在点
    '''
    pointsList = []

    if eddyType == 'warm':
        cmp = cmpLess
    else:
        cmp = cmpGreater

    j = centerJ
    while j > 0: # 左1
        if numpy.isnan(srcSSH[centerI][j-1]):
            break
        if cmp(srcSSH[centerI][j-1], threshold) or srcSSH[centerI][j-1] == threshold:
            break
        j -= 1
    pointsList.append([lonList[j], latList[centerI]])

    i = centerI
    j = centerJ
    while i > 0 and j > 0: # 左上6
        if numpy.isnan(srcSSH[i-1][j-1]):
            break
        if cmp(srcSSH[i-1][j-1], threshold) or srcSSH[i-1][j-1] == threshold:
            break
        i -= 1
        j -= 1
    pointsList.append([lonList[j], latList[i]])

    i = centerI
    while i > 0: # 上2
        if numpy.isnan(srcSSH[i-1][centerJ]):
            break
        if cmp(srcSSH[i-1][centerJ], threshold) or srcSSH[i-1][centerJ] == threshold:
            break
        i -= 1
    pointsList.append([lonList[centerJ], latList[i]])

    i = centerI
    j = centerJ
    while j < len(lonList)-1 and i > 0: # 右上7
        if numpy.isnan(srcSSH[i-1][j+1]):
            break
        if cmp(srcSSH[i-1][j+1], threshold) or srcSSH[i-1][j+1] == threshold:
            break
        i -= 1
        j += 1
    pointsList.append([lonList[j], latList[i]])

    j = centerJ
    while j < len(lonList)-1: # 右3
        if numpy.isnan(srcSSH[centerI][j+1]):
            break
        if cmp(srcSSH[centerI][j+1], threshold) or srcSSH[centerI][j+1] == threshold: 
            break
        j += 1
    pointsList.append([lonList[j], latList[centerI]])

    i = centerI
    j = centerJ
    while j < len(lonList)-1 and i < len(latList)-1: # 右下8
        if numpy.isnan(srcSSH[i+1][j+1]):
            break
        if cmp(srcSSH[i+1][j+1], threshold) or srcSSH[i+1][j+1] == threshold:
            break
        i += 1
        j += 1
    pointsList.append([lonList[j], latList[i]])

    i = centerI
    while i < len(latList)-1: # 下4
        if numpy.isnan(srcSSH[i+1][centerJ]):
            break
        if cmp(srcSSH[i+1][centerJ], threshold) or srcSSH[i+1][centerJ] == threshold:
            break
        i += 1
    pointsList.append([lonList[centerJ], latList[i]])

    i = centerI
    j = centerJ
    while i < len(latList)-1 and j > 0: # 左下5
        if numpy.isnan(srcSSH[i+1][j-1]):
            break
        if cmp(srcSSH[i+1][j-1], threshold) or srcSSH[i+1][j-1] == threshold:
            break
        i += 1
        j -= 1
    pointsList.append([lonList[j], latList[i]])

    return {"points": pointsList, "center": [lonList[centerJ], latList[centerI]], "type": eddyType}

if __name__ == '__main__':
    app.run(debug=True, port=8000)