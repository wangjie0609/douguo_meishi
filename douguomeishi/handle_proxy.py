import requests

#114.246.2.155"
url = 'http://www.xiongmaodaili.com/xiongmao-web/api/glip?secret=542e71003a9a551319152e578817095f&orderNo=GL20181126094439JwtRMr9d&count=10&isTxt=0&proxyType=1'
response = requests.get(url=url)
print(response.text)