# MyProfile app

SEPARATOR = '------------------------------------------'

# user profile
name = ''
age = 0
phone_number = ''
email = ''
index = ''
address = ''
info = ''
# business profile
ogrnip = 0
inn = 0
account = 0
bank_name = ''
bic = ''
correspondent_account = 0


def private_info_user(name_parameter, age_parameter, phone_number_parameter,
                      email_parameter, index_parameter, address_parameter,
                      info_parameter):
    print(SEPARATOR)
    print('Имя:    ', name_parameter)
    if 11 <= age_parameter % 100 <= 19: years_parameter = 'лет'
    elif age_parameter % 10 == 1: years_parameter = 'год'
    elif 2 <= age_parameter % 10 <= 4: years_parameter = 'года'
    else: years_parameter = 'лет'
    print('Возраст:', age_parameter, years_parameter)
    print('Телефон:', phone_number_parameter)
    print('E-mail: ', email_parameter)
    print('Индекс: ', index_parameter)
    print('Адрес:  ', address_parameter)
    if info:
        print('')
        print('Дополнительная информация:')
        print(info_parameter)


def business_info_user(ogrnip_parameter, inn_parameter, account_parameter,
                       bank_name_parameter, bic_parameter,
                       correspondent_account_parameter):
    print(SEPARATOR)
    print('ОГРНИП: ', ogrnip_parameter)
    print('ИНН:    ', inn_parameter)
    print('Рассчетный счет:', account_parameter)
    print('Название банка:', bank_name_parameter)
    print('БИК банка:', bic_parameter)
    print('Кор. счет:', correspondent_account_parameter)


def get_check_parameter(parameter_name: str, length: int) -> int:
  parameter = 0
  while 1:
    parameter = int(input(f'Введите {parameter_name}: '))
    if (parameter > 0) and (len(str(parameter))) == length:
        return parameter
    print(f'{parameter_name} должен содержать {length} цифр')


print('Приложение MyProfile')
print('Сохраняй информацию о себе и выводи ее в разных форматах')

while True:
    # main menu
    print(SEPARATOR)
    print('ГЛАВНОЕ МЕНЮ')
    print('1 - Ввести или обновить информацию')
    print('2 - Вывести информацию')
    print('0 - Завершить работу')

    option = int(input('Введите номер пункта меню: '))
    if option == 0:
        break

    if option == 1:
        # submenu 1: edit info
        while True:
            print(SEPARATOR)
            print('ВВЕСТИ ИЛИ ОБНОВИТЬ ИНФОРМАЦИЮ')
            print('1 - Личная информация')
            print('2 - Информация о предпринимателе')
            print('0 - Назад')

            option2 = int(input('Введите номер пункта меню: '))
            if option2 == 0:
                break
            if option2 == 1:
                # input private info
                name = input('Введите имя: ')
                while 1:
                    # validate user age
                    age = int(input('Введите возраст: '))
                    if age > 0:
                        break
                    print('Возраст должен быть положительным')

                phone_input = input('Введите номер телефона (+7ХХХХХХХХХХ): ')
                phone_number = ''
                for ch in phone_input:
                    if ch == '+' or ('0' <= ch <= '9'):
                        phone_number += ch

                email = input('Введите адрес электронной почты: ')
                index_input = input('Введите почтовый индекс: ')
                index = ''
                for ch in index_input:
                    if '0' <= ch <= '9':
                        index += ch
                address = input('Введите почтовый адрес (без индекса): ')
                info = input('Введите дополнительную информацию:\n')

            elif option2 == 2:
                # input business info
                ogrnip = get_check_parameter('ОГРНИП', 15)
                inn = get_check_parameter('ИНН', 12)
                account = get_check_parameter('Расчетный счет', 20)
                bank_name = input('Введите название банка: ')
                bic_input = input('Введите БИК банка: ')
                bic = ''
                for ch in bic_input:
                    if '0' <= ch <= '9':
                        bic += ch
                correspondent_account = get_check_parameter('Корреспондентский счет', 20)
            else:
                print('Введите корректный пункт меню')
    elif option == 2:
        # submenu 2: print info
        while True:
            print(SEPARATOR)
            print('ВЫВЕСТИ ИНФОРМАЦИЮ')
            print('1 - Личная информация')
            print('2 - Вся информация')
            print('0 - Назад')

            option2 = int(input('Введите номер пункта меню: '))
            if option2 == 0:
                break
            if option2 == 1:
                private_info_user(name, age, phone_number, email, index,
                                  address, info)
            elif option2 == 2:
                private_info_user(name, age, phone_number, email, index,
                                  address, info)
                business_info_user(ogrnip, inn, account, bank_name, bic,
                                   correspondent_account)

            else:
                print('Введите корректный пункт меню')
    else:
        print('Введите корректный пункт меню')
