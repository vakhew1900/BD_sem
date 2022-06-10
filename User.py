from matplotlib.pyplot import cla
from IModel import IModel

class User(IModel):
    def __init__(self, id = 1,  login = 'login', password = 'password',  nickname = 'nickname'):
        super().__init__(id)
        self._login = login
        self._password = password
        self._nickname = nickname

    '''геттеры '''

    @property
    def login(self):
        return self._login
    
    @property
    def password(self):
        return self._password
    
    @property
    def nickname(self):
        return self._nickname

    '''сеттеры'''

    @login.setter
    def login(self, login):
        self._login = login
    
    @password.setter
    def password(self, password):
        self._password = password
    
    @nickname.setter
    def nickname(self, nickname):
        self._nickname = nickname



if (__name__ == '__main__'):
    user = User(2, 'x', 'y', 'z')
    print('{} {} {} {}'.format(user.id, user.login, user.password, user.nickname))
    user.login = 'login'
    user.password = 'pass'
    user.nickname = 'nickname'
    print('{} {} {} {}'.format(user.id, user.login, user.password, user.nickname))


