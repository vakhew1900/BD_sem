from mysqlx import RowResult
from connectionDB import create_connect
from Game import Game


def getEstimation(product_id): 

    try:
        con = create_connect()
        try:

            with con.cursor() as cur:
                
                getAvgEstimation = 'select\
                                    avg(r.estimation) as estimation\
                                    from reviews r\
                                    natural join products p\
                                    where product_id = %s;'
                
                cur.execute(getAvgEstimation, product_id)

                row = cur.fetchone()
                print(row)

                estimation = None
                if (row['estimation'] != None):
                     estimation = float(row['estimation'])

                     
                return estimation

        finally:
            con.close()
    
    except:
        print('error 1')


def getLibrary(user_id):

    try:
        con = create_connect()
        try:

            with con.cursor() as cur:
                
                getLibraryCommand = 'select \
                                    p.product_id,\
                                    p.`name`,\
                                    p.price,\
                                    p.`description`,\
                                    p.release_date,\
                                    p.developer_id,\
                                    p.publisher_id,\
                                    p.tag_name \
                                    from orders o \
                                    inner join game_keys gk\
                                    on gk.order_id = o.order_id \
                                    inner join fullinfoaboutgame p\
                                    on p.product_id = gk.product_id\
                                    inner join users u\
                                    on o.user_id = u.user_id\
                                    inner join games g\
                                    on g.game_id = p.product_id\
                                    where gk.game_key_id not in (select game_key_id from refunds)\
                                    and u.user_id = %s;'
                
                cur.execute(getLibraryCommand, user_id)

                rows = cur.fetchall()
                print(rows)

                games = []
                tags = []
                for row in rows:
                    product_id = row['product_id']
                    name = row['name']
                    price = row['price']
                    description = row['description']
                    developer_id = row['developer_id']
                    publisher_id = row['publisher_id']
                    release_date = row['release_date']
                    tag = row['tag_name']
                    game = Game(id=product_id, name=name, release_date= release_date, price=price, description= description, developer_id=developer_id, publisher_id=publisher_id)
                    
                    games.append(game)
                    tags.append(tag)

                return games, tags 

        finally:
            con.close()
    
    except:
        print('error 1')


if __name__ == '__main__':

    # x = getEstimation()
    # print(x)
    getLibrary(1)
