from zeep import Client, Transport
from zeep.wsse.signature import Signature
from zeep.wsse import UsernameToken

# Задаем параметры
webServiceUrl = 'https://services.fedresurs.ru/Bankruptcy/MessageServiceDemo/WebService.svc'
login = 'demowebuser'
password = 'Ax!761BN'

# создаем объект Signature и устанавливаем в нем UsernameToken
signature = Signature(key_filename=None, cert_filename=None)
signature.set_signature('UsernameToken', UsernameToken(login, password))

# Устанавливаем заголовок для подключения к сервису
transport = Transport()
transport.wsse = signature
client = Client(webServiceUrl, transport=transport)

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