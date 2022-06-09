from platform import release
from connectionDB import create_connect
from Game import Game

def add(newGame):

    try:
        con = create_connect()
        try:

            with con.cursor() as cur:
              
                name = newGame.name
                price = newGame.price
                release_date = newGame.release_date
                description = newGame.description
                developer_id = newGame.developer_id
                publisher_id = newGame.publisher_id

                insertProductCommand = 'INSERT INTO PRODUCTS(name, price, description, release_date) VALUE(%s, %s, %s, %s)'
                cur.execute(insertProductCommand, (name, price, description, release_date))
                con.commit()

                game_id = cur.lastrowid
                print(game_id)

                insertGameCommand = 'INSERT INTO GAMES(game_id, developer_id, publisher_id) VALUE(%s, %s, %s)'
                cur.execute(insertGameCommand, (game_id, developer_id, publisher_id))
                con.commit()

        finally:
            con.close()
    
    except:
        print('error')

def delete(game_id):
    try:
        con = create_connect()
        try:

            with con.cursor() as cur:
              
                getGameByIdCommand = 'SELECT * FROM fullInfoAboutGame WHERE product_id = %s;'
                cur.execute( getGameByIdCommand, game_id)
                
                row = cur.fetchone()
                
                if (row == None):
                        return

                
                deleteProductCommand = 'DELETE FROM PRODUCTS WHERE product_id = %s'
                cur.execute(deleteProductCommand, game_id)
                con.commit()


        finally:
            con.close()
    
    except:
        print('error')
    

def update(game):
    
    try:
        con = create_connect()
        try:

            with con.cursor() as cur:
                
                product_id = game.id
                name = game.name
                price = game.price
                description = game.description
                developer_id = game.developer_id
                publisher_id = game.publisher_id
                release_date = game.release_date

                getGameByIdCommand = 'SELECT * FROM fullInfoAboutGame WHERE product_id = %s;'
                cur.execute( getGameByIdCommand, product_id)
                
                row = cur.fetchone()
                
                if (row == None):
                        return

                
                updateProductCommand = 'UPDATE products SET release_date = %s, price = %s, description = %s, name = %s WHERE product_id = %s'
                cur.execute(updateProductCommand,(release_date, price, description, name, product_id))
                con.commit()

                updateGameCommand = 'UPDATE games SET developer_id = %s, publisher_id = %s where game_id = %s'
                cur.execute(updateGameCommand,(developer_id, publisher_id, product_id))
                con.commit()

                row =cur.fetchone()
                print(row)

                return game
        finally:
            con.close()
    
    except:
        print('error')

def getAll(): 

    try:
        con = create_connect()
        try:

            with con.cursor() as cur:
              
                getGameByIdCommand = 'SELECT * FROM fullInfoAboutGame;'
                cur.execute( getGameByIdCommand)
                
                rows = cur.fetchall()
                
                if (rows == None):
                        return

                gameList = []    
                for row in rows:
                    product_id = row['product_id']
                    name = row['name']
                    price = row['price']
                    description = row['description']
                    developer_id = row['developer_id']
                    publisher_id = row['publisher_id']
                    release_date = row['release_date']
                    
                    game = Game(id=product_id, name=name, release_date= release_date, price=price, description= description, developer_id=developer_id, publisher_id=publisher_id)
                    gameList.append(game)

                return gameList


        finally:
            con.close()
    
    except:
        print('error')

def getById(game_id):
    
    try:
        con = create_connect()
        try:

            with con.cursor() as cur:
              
                getGameByIdCommand = 'SELECT * FROM fullInfoAboutGame WHERE product_id = %s;'
                cur.execute( getGameByIdCommand, game_id)
                
                row = cur.fetchone()
                
                if (row == None):
                        return

                print(row)

                product_id = row['product_id']
                name = row['name']
                price = row['price']
                description = row['description']
                developer_id = row['developer_id']
                publisher_id = row['publisher_id']
                release_date = row['release_date']
                
                game = Game(id=product_id, name=name, release_date= release_date, price=price, description= description, developer_id=developer_id, publisher_id=publisher_id)

                return game 


        finally:
            con.close()
    
    except:
        print('error')


def getByName(name):
    try:
        con = create_connect()
        try:

            with con.cursor() as cur:
              
                getGameByIdCommand = 'SELECT * FROM fullInfoAboutGame WHERE name = %s;'
                cur.execute( getGameByIdCommand, name)
                
                row = cur.fetchone()
                
                if (row == None):
                        return

                print(row)

                product_id = row['product_id']
                name = row['name']
                price = row['price']
                description = row['description']
                developer_id = row['developer_id']
                publisher_id = row['publisher_id']
                release_date = row['release_date']
                
                game = Game(id=product_id, name=name, release_date= release_date, price=price, description= description, developer_id=developer_id, publisher_id=publisher_id)

                return game 


        finally:
            con.close()
    
    except:
        print('error')


if __name__ == '__main__':

    # game = getByName('Skyrim')
    # print(game.name)
    # print(game.release_date)
    game = Game(id = 172)

    add(game)

    # update(game)
    
    # delete(171)