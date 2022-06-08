import pymysql
import config


def create_connect():
    
    con = pymysql.connect(
    host ='localhost',
    port = 3306, 
    user ='root',
    password = 'myRoTpass1ord',
    database = 'gameshop',
    cursorclass=pymysql.cursors.DictCursor
    )

    return con

# con = pymysql.connect(
#     host ='localhost',
#     port = 3306, 
#     user ='root',
#     password = 'myRoTpass1ord',
#     database = 'gameshop',
#     cursorclass=pymysql.cursors.DictCursor
#     )

# con = create_connect()
# cur = con.cursor()
# cur.execute('SELECT * FROM PRODUCTS WHERE PRODUCT_ID = 1')
# product = cur.fetchall()

# print(product)


