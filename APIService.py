import datetime

import requests
import functools

from requests.adapters import HTTPAdapter
from urllib3 import Retry

from MyLink import MyLink


class APIService:

    def __init__(self, login, password):
        self.login: str = login
        self.password: str = password
        self.session = self.Auth()
        self.cars = self.GetCars()
        self.link = MyLink(
            'login',
            'password',
            'password',
            'password?'
        )

    def Auth(self):
        session = requests.Session()
        session.request = functools.partial(session.request, timeout=3600)
        retries = Retry(total=200,
                        backoff_factor=0.1,
                        status_forcelist=[500, 502, 503, 504])
        session.mount('https://', HTTPAdapter(max_retries=retries))
        session.mount('http://', HTTPAdapter(max_retries=retries))

        answer = session.post('somelink', data={
            'login': self.login,
            'pass': self.password
        })

        print('APIStax: авторизовался')

        return session

    def IsFineExist(self, sign):

        return len(self.link.Select('fines', "sign='" + sign + "'")) != 0

    def AddFine(self, fine, type):

        if 'originalAmount' in fine:
            origAmount = fine['originalAmount']
        else:
            origAmount = fine['amount']

        if 'discountDate' in fine:
            disc = fine['discountDate']
        else:
            disc = ''

        time = datetime.datetime.strptime(fine['billDate'], '%Y-%m-%dT%H:%M:%S%z')
        time = time + datetime.timedelta(hours=3)

        offense = 'Не указано'

        for arg in fine['resoluton']['addAttrs']:
            if arg['name'] == 'offenseDate':
                offense = arg['value']

        isPaid = 0
        if fine['resoluton']['isPaid']:
            isPaid = 1

        self.link.Insert('fines', {
            'sign': fine['signature'],
            'billId': fine['billId'],
            'discountDate': disc,
            'from_org': fine['sourceShortName'],
            'numberPlate': fine['document']['numberPlate'],
            'sts_serial': fine['document']['series'],
            'sts_number': fine['document']['number'],
            'amount': fine['amount'],
            'originalAmount': origAmount,
            'billDate': int(time.timestamp()),
            'supplierFullName': fine['supplierFullName'],
            'billName': fine['billName'],
            'sourceFullName': fine['supplierFullName'],
            'car_name': fine['document']['carName'],
            'type': type,
            'resolution': fine['resoluton']['billNumber'],
            'isPaid': isPaid,
            'offenseDate': offense
        })

    def UpdateFine(self, fine):

        if 'originalAmount' in fine:
            origAmount = fine['originalAmount']
        else:
            origAmount = fine['amount']

        if 'discountDate' in fine:
            disc = fine['discountDate']
        else:
            disc = ''

        offense = 'Не указано'

        for arg in fine['resoluton']['addAttrs']:
            if arg['name'] == 'offenseDate':
                offense = arg['value']

        time = datetime.datetime.strptime(fine['billDate'], '%Y-%m-%dT%H:%M:%S%z')
        time = time + datetime.timedelta(hours=3)

        isPaid = 0
        if fine['resoluton']['isPaid']:
            isPaid = 1

        self.link.Update('fines', {
            'billId': fine['billId'],
            'discountDate': disc,
            'from_org': fine['sourceShortName'],
            'numberPlate': fine['document']['numberPlate'],
            'sts_serial': fine['document']['series'],
            'sts_number': fine['document']['number'],
            'amount': fine['amount'],
            'originalAmount': origAmount,
            'billDate': int(time.timestamp()),
            'supplierFullName': fine['supplierFullName'],
            'billName': fine['billName'],
            'sourceFullName': fine['sourceFullName'],
            'car_name': fine['document']['carName'],
            'type': 'gosuslugi',
            'resolution': fine['resoluton']['billNumber'],
            'isPaid': isPaid,
            'offenseDate': offense

        }, "sign='"+fine['signature']+"'")

    def GetCars(self):

        answer = self.session.post('https://stax.mcdir.ru/engine/api/cars-service.php', data={
            'action': 'get'
        }).json()

        result = dict()

        for car in answer:
            key = car['b_licence_perm'] + car['b_licence_number']
            result[key] = car

        return result
