import requests

url = 'http://openapi.airport.co.kr/service/rest/dailyExpectPassenger/dailyExpectPassenger'
params ={'serviceKey' : 'TKEzopLWWMJ0hEFGtXooFm+ezPURFhz9cPKbTCq+zty/r6RJzsJM5Wc+9aLgUBPHuaOJaPowbWFZ46pBeLghdQ==', 'schDate' : '20220422', 'schAirport' : 'PUS', 'schTof' : 'D', 'schHH' : '24' }

response = requests.get(url, params=params)
print(response.content)