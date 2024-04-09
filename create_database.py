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
    planet = Planets('Меркурий')
    session.add(planet)
    new = News('Great', 'Very big planet', 'img/op.jog', 1)
    session.add(new)
    session.commit()
    session.close()
    return session
