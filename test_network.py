import requests
try:
    test1 = requests.get('https://www.baidu.com')
    print('network worked!')
    try: 
        test2 = requests.get('https://www.google.com')
    except:
        print("can't connect google")
except:
    print('network error')

