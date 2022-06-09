from datetime import datetime
from IRepository import IRepository
import datetime

class Product(IRepository):
    
    def __init__(self, id=1, name = 'name', release_date = datetime.date(2015, 5, 5), price = 1299, description = 'Description'):
        super().__init__(id)

        self._name = name
        self._release_date = release_date
        self._price = price
        self._description = description
        
    
    '''геттеры'''

    @property
    def name(self):
        return  self._name 
    
    @property
    def release_date(self):
        return self._release_date
    
    @property
    def price(self):
        return self._price
    
    @property
    def description(self):
        return self._description

    '''сеттеры'''

    @name.setter
    def name(self, name):
        self._name = name

    @release_date.setter
    def release_date(self, release_date):
        self._release_date =release_date

    @price.setter
    def price(self, price):
        self._price = price

    @description.setter
    def description(self, description):
        self._description = description


if __name__ == '__main__':
    product = Product()

    print('{} {} {} {} {}'.format( product.id, product.name, product.release_date, product.price, product.description))

    product.id = 1
    product.name = 'n'
    product.release_date = datetime.date(2000,11,12)
    product.price = 1000
    product.description = 'fdsa;jlgadsdgshnags;'
    print('{} {} {} {} {}'.format( product.id, product.name, product.release_date, product.price, product.description))




