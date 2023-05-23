import requests.auth
from zeep import Client
from requests import Session
from requests.auth import HTTPDigestAuth
from zeep.transports import Transport


# Задаем параметры
webServiceUrl = 'https://services.fedresurs.ru/Bankruptcy/MessageServiceDemo/WebService.svc?wsdl'
username = 'demowebuser'
password = 'Ax!761BN'


# Устанавливаем заголовок для подключения к сервису
session = Session()
session.auth = requests.auth.HTTPDigestAuth(username, password)
client = Client(webServiceUrl, transport=Transport(session=session))

# Функция для проверки и очистки введенного ИНН
def process_inn():
    while True:
        inn = input('Введите ИНН (от 10 до 15 цифр): ')
        inn = ''.join([ch for ch in inn if ch.isdigit()]) # Удаление всех символов из строки, оставление только цифр
        if 10 <= len(inn) <= 15:
            return inn
        print('Введите число, состоящий из 10-15 цифр')

inn = 125986032597 # Тестовый Инн

# Отправляем запрос на сервис и выводим результат
try:
    response = client.service.GetDebtorByIdBankrupt(inn)
    if response.Status == 'success':
        for message in response.Messages:
            print('MessageGUID:', message.MessageGUID)
            print('PublishDate:', message.PublishDate)
            print('MessageInfo:', message.MessageInfo)
            print('-' * 20)
        print('Авторизация прошла успешно')
    else:
        print('Ошибка авторизации: ', response.ErrorMessage)
except Exception as e:
    print(f'Error {e}: {e.args}')
