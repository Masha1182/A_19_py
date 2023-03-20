from api import PetFriends
from settings import  valid_email, valid_password
pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_pet_with_valid_key():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, 'Stiv', 'Cat', '3', 'img/cat.jpg')
    assert status == 200
    assert result['name'] == 'Stiv'
    assert result['id'] != ''

def test_successful_delete_self_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, 'Рекс', 'собака', '5', 'img/dog1.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    assert status == 200
    assert pet_id not in my_pets.values()

def test_update_info_about_pet_valid():
    _,auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], 'Быстрый', 'Орёл', 2)
        assert status == 200
        assert result['name'] == 'Быстрый'
    else:
        raise Exception("Питомцы отсутствуют")

# Мои ТЕСТЫ:

def test_add_new_pet_without_photo_valid():
   #  Проверка возможности создать питомца без фотографии
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, 'Эсмиральда', 'Лиса', 8)
    assert status == 200
    assert result['name'] == 'Эсмиральда'
# Сайт позволяет создать питосцев без фотографии

def test_add_pet_photo_valid():
    #  Проверка возможности добавления (замены) фотографии питомца
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, filter='my_pets')
    pet_id = my_pets['pets'][0]['id']
    # Если список непустой, то добавляем фотографию
    if len(my_pets['pets']) > 0:
        status, result = pf.add_pet_photo(auth_key, pet_id, 'img/123.jpg')
        assert status == 200
    else:
        raise Exception("Питомцы отсутствуют")


def test_set_other_pet_photo_invalid():
    #  Проверка ошибки добавления фотографии к питомцу
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, result = pf.get_list_of_pets(auth_key, filter='')

    if len(result['pets']) > 0:
        status, result = pf.add_pet_photo(auth_key, result['pets'][0]['id'], 'img/123.jpg')
    else:
        status, result = pf.add_new_pet_without_photo(auth_key, 'Dusha', 'squirrel', 8)
        status, result = pf.add_pet_photo(auth_key, result['pets'][0]['id'], 'img/123.jpg')

    assert status == 400 or status == 500



def test_get_api_key_for_invalid_user():
    #Проверка получения апи ключа для невалидного email и пароля
   status, result = pf.get_api_key('maSHa@mail.ru', 'Capcan123')
   assert status == 403
# Фактический результат (status == 403) соответствует ожидаемому, получение ключа не возможно


def test_get_all_pets_with_invalid_key(filter=''):
    #Проверка невозможности запроса всех питомцев с неверным api-ключом
    auth_key = {'key': '000'}
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403
# Фактический результат (status == 403) соответствует ожидаемому, получение списка питомцев с невалидным ключем невозможно


def test_cannot_add_a_pet_with_blanc_name_type_age(name='', animal_type='', age=''):
#Проверка невозможности создать питомца с незаполненными обязательными параметрами(имя, тип, возраст)
   _, auth_key = pf.get_api_key(valid_email, valid_password)
   status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
   assert status == 400
# Обнаружен дефект, так как сайт позволяет добавлять питомцев с неуказанными параметрами
# Фактический результат (status == 200) расходится с ожидаемым (status == 400)!!!


def test_cannot_add_a_pet_with_invalid_age(name='Son', animal_type='dog', age='-40'):
#Проверка невозможности задать отрицательный возраст питомца
  _, auth_key = pf.get_api_key(valid_email, valid_password)
  status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
  assert age != '-40' or status == 400
# Обнаружен дефект, так как сайт принимет отрицательные значения возраста и позволяет добавлять питомцев с такими параметрами.
# Фактический результат (status == 200 и age = '-40') расходится с ожидаемым (status == 400)!!!


def test_cannot_get_all_pets_with_no_filter(filter='ahi'):
#Проверка ошибки поиска животных с невалидным фильтром
  _, auth_key = pf.get_api_key(valid_email, valid_password)
  status, result = pf.get_list_of_pets(auth_key, filter)
  assert status == 400 or status == 500
# status == 500 - сайт не  невалидное значение фильтра не принимается

def test_cannot_delete_pet_no_id():
#Проверка невозможности удалить питомца с несуществующим id (удаление id после удаления)
  _, auth_key = pf.get_api_key(valid_email, valid_password)
  _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
  if len(my_pets['pets']) == 0:
    pf.add_new_pet_without_photo(auth_key, MyStiv, 'cat', '3')
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
  pet_id = my_pets['pets'][0]['id']
  status, _ = pf.delete_pet(auth_key, pet_id)
  status, _ = pf.delete_pet(auth_key, pet_id)
  assert status == 400
# Обнаружен дефект, так как после удаления снова было возможно удаление питомца по id
# Фактический результат (status == 200) расходится с ожидаемым (status == 400)!!!

def test_add_new_pet_with_special_symbols_in_name(name='UR&ro№'):
    #Проверка невозможности добавления питомца со специальными символами в параметре name

   _, auth_key = pf.get_api_key(valid_email, valid_password)
   status, result = pf.add_new_pet_without_photo(auth_key, name, 'cat', '3')
   assert status == 400
    # Обнаружен дефект, так как сайт позволяет добавлять питомцев, у которых в имени есть спец.символы ('UR&ro№').
    # Фактический результат (status == 200) расходится с ожидаемым (status == 400)!!!


