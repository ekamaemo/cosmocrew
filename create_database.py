from db_session import create_db, session
from users import Users
from planets import Planets
from news import News


def create_database(load_fake_data: bool = True):
    create_db()
    if load_fake_data:
        return _load_fake_data(session())
    return session()


def _load_fake_data(session: session):
    planets = [['Меркурий', 'mercury.jfif'], ['Венера', 'венера.jpeg'],
               ['Земля', 'земля.jpeg'], ['Марс', 'марс.jpeg'],
               ['Юпитер', 'юпитер.jpeg'], ['Сатурн', 'сатурн.jpeg'],
               ['Уран', 'уран.jpeg'], ['Нептун', 'нептун.jpeg']]
    for planet in planets:
        planet = Planets(planet[0], planet[1])
        session.add(planet)
    session.commit()
    session.close()
    return session
