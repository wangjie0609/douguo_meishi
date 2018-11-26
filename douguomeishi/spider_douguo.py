import requests
import json
from multiprocessing import Queue
from handel_mongo import mongn_info
from concurrent.futures import ThreadPoolExecutor
#创建队列
queue_list = Queue


def handel_requests(url,data):
    header = {
    'client':'4',
    'version':'6928.2',
    'device':'MI 8 Lite',
    'sdk':'27,8.1.0',
    'imei':'869041047137959',
    'channel':'miui',
    # 'mac':'02:00:00:00:00:00',
    'resolution':'2150*1080',
    'dpi':'2.75',
    # 'android-id':'04a7d1a8b6ef350a',
    # 'pseudo-id':'2d9a619d',
    'brand':'Xiaomi',
    'scale':'2.75',
    'timezone':'28800',
    'language':'zh',
    'cns':'13',
    'carrier':'%E4%B8%AD%E5%9B%BD%E8%81%94%E9%80%9A',
    'imsi':'460015020506488',
    'user-agent':'Mozilla/5.0 (Linux; Android 8.1.0; MI 8 Lite Build/OPM1.171019.019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36',
    'reach':'1',
    'newbie':'0',
    # 'lon':'118.606653',
    # 'lat':'24.878731',
    # 'cid':'350500',
    'Content-Type':'application/x-www-form-urlencoded; charset=utf-8',
    'Accept-Encoding':'gzip, deflate',
    'Connection':'Keep-Alive',
    # 'Cookie':'duid=57834252',
    'Host':'api.douguo.net',
    # 'Content-Length':'68',
    }
    proxy = {'http': 'http://H211EATS9O5745KC:F8FFBC929EB7D5A7@http-cla.abuyun.com:9030'}

    response = requests.post(url = url,headers = header,data=data,proxies=proxy)
    return response

def handle_index():
    url = 'http://api.douguo.net/recipe/flatcatalogs'
    data = {
    'client':'4',
    # '_session':'1542896919572869041047137959',
    # 'v':'1503650468',
    '_vs':'2305',
    }

    response = handel_requests(url=url,data=data)

    index_response_dict = json.loads(response.text)
    for index_item in index_response_dict['result']['cs']:
        for index_item_1 in index_item['cs']:
            for item in index_item_1['cs']:

                data_2 = {
                    'client':'4',
                  # '_session'='1542896919572869041047137959',
                    'keyword':item['name'],
                    'order':'3',
                    '_vs':'400',
                }
                queue_list.put(data_2)


def handle_caipu_list(data):
    print('当前处理的食材',data['keyword'])
    caipu_list_url = 'http://api.douguo.net/recipe/v2/search/0/20'
    caipu_list_response = handel_requests(url=caipu_list_url,data=data)
    caipu_list_response_dict = json.loads(caipu_list_response.text)
    for item in caipu_list_response_dict['result']['list']:
        caipu_info = {}
        caipu_info['shicai'] = data['keyword']
        if item['type'] == 13:
            caipu_info['user_name'] = item['r']['an']
            caipu_info['shicai_id'] = item['r']['id']
            caipu_info['describe'] = item['r']['cookstory'].replace('\n', '').replace(' ','')
            caipu_info['caipu_name'] = item['r']['n']
            caipu_info['zuoliao'] = item['r']['major']
            detail_url= 'http://api.douguo.net/recipe/detail/' + str(caipu_info['shicai_id'])
            detail_data = {
                'client':'4',
                # '_session':'1543071492568869041047137959',
                'author_id':'0',
                '_vs':'2803',
                '_ext':'{"query":{"kw":+ caipu_info["shicai"] +,"src":"2803","idx":"1","type":"13","id":+caipu_info["shicai_id"]+}}',
            }
            detail_response = handel_requests(url=detail_url,data=detail_data)
            # print(detail_response.text)
            detail_response_dict = json.loads(detail_response.text)
            caipu_info['tips'] = detail_response_dict['result']['recipe']['tips']
            caipu_info['cook_step'] = detail_response_dict['result']['recipe']['cookstep']
            print('当前入库的菜谱',caipu_info['caipu_name'])
            mongn_info.insert_item(caipu_info)
        else:
            continue


handle_index()
pool = ThreadPoolExecutor(max_workers=2)
while queue_list.qsize()>0:
    pool.submit(handle_caipu_list,queue_list.get())