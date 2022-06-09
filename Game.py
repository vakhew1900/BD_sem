import Product
import datetime

class Game(Product.Product):
    
    def __init__(self, id=1, name = 'name', release_date = datetime.date(2015, 5, 5), price = 1299, description = 'Description', developer_id = 1, publisher_id = 1):
        super().__init__(id,name, release_date, price, description)

        self._developer_id = developer_id
        self._publisher_id = publisher_id

    
    '''геттеры'''

    @property
    def developer_id(self):
        return self._developer_id

    @property
    def publisher_id(self):
        return self._publisher_id

    
    '''сеттеры'''

    @developer_id.setter
    def developer_id(self, developer_id):
        self._developer_id = developer_id

    @publisher_id.setter
    def publisher_id(self, publisher_id):
        self._publisher_id = publisher_id

    

if (__name__ == '__main__'):

    game = Game()
    
    game.developer_id = 2
    game.publisher_id = 3

    print(game.developer_id)
    print(game.publisher_id)
