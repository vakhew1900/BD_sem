
class IRepository:

    def __init__(self, id = 1):
        self._id = id
    

    @property
    def id(self):
        return  self._id
    
    @id.setter
    def id(self, x):

        self._id = x


if __name__ == "__main__":
    rep = IRepository(3)

    print(rep.id)
    print(rep.id)