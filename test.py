from requests import get, post, delete, put

print(get('http://127.0.0.1:8080/api/users').json())  # получение всех пользователей
print(get('http://127.0.0.1:8080/api/users/3').json())  # получение одного пользователя
print(post('http://127.0.0.1:8080/api/users', json={'surname': 'Maksaeva',
                                                       'name': 'Ekaterina',
                                                       'age': 15,
                                                       'position': 'No',
                                                       'speciality': 'No',
                                                       'address': 'Earth',
                                                       'email': 'eka@gmail.com'}).json())  # добавление нового пользователя
print(post('http://127.0.0.1:8080/api/users', json={}).json())  # пустой запрос на добавление, некорректен
print(delete('http://127.0.0.1:8080/api/users/23').json())  # корректный запрос на удаление
print(put('http://127.0.0.1:8080/api/users/5', json={'surname': 'Ed'}).text)

