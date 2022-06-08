
class IRepository:

    def __init__(self, id = 1):
        self._id = id
    

    @property
    def id(self):
        return  self._id
    
    @id.setter
    def id(self, x):
        
        if (x < 0):
            return

        self._id = x
