import requests

if __name__ == '__main__':

    resultEnd=requests.get('http://0.0.0.0:5002/productos/actualizacion/{0}/{1}'.format(101,"2010-01-01 00:00:00"))
