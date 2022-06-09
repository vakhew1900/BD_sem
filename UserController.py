
from http.client import NOT_FOUND
from platform import release

from matplotlib.pyplot import connect
import pymysql
from connectionDB import create_connect
from User import User




def add(newUser):
    
    if not isinstance(newUser, User):
        return 

    try:
        con = create_connect()
        try:

            with con.cursor() as cur:
                login = newUser.login
                password = newUser.password
                nickname = newUser.nickname

                print(login + password + nickname)
                addUserCommand = 'INSERT INTO USERS(login, password, nickname) VALUE(%s, %s, %s);'
                cur.execute(addUserCommand, (login, password, nickname))
                print('fff')
                con.commit()

                newId = cur.lastrowid
                newUser.id = newId
                return newId

                

        finally:
            con.close()
    
    except:
        print('error')

def delete(user_id):

    try:
        con = create_connect()
        try:

            with con.cursor() as cur:
              
                deleteUserCommand = 'DELETE FROM USERS WHERE USER_ID = %s'
                cur.execute(deleteUserCommand, user_id)
                con.commit()
        finally:
            con.close()
    
    except:
        print('error')

    

def update(user):
    try:
        con = create_connect()
        try:

            with con.cursor() as cur:
                user_id = user.id
                login = user.login
                password = user.password
                nickname = user.nickname
            
                userExistCommand = 'SELECT * FROM USERS WHERE USER_ID = %s;'
                cur.execute(userExistCommand, user_id)

                row=cur.fetchone()

                if row == None:
                    return
                
                print('row = {}'.format(row))
                loginExistCommand = 'SELECT * FROM USERS WHERE LOGIN = %s'

                cur.execute(loginExistCommand, login)

                row = cur.fetchone()
                
                print('row = {}'.format(row))
                
                if row != None and row['user_id'] != user_id:
                    return

                updateUserCommand = 'UPDATE USERS SET LOGIN = %s, PASSWORD = %s, NICKNAME = %s WHERE user_id = %s'
                print(updateUserCommand)
                cur.execute(updateUserCommand,(login, password, nickname, user_id))
                con.commit()
                print('yes')
                return user  


        finally:
            con.close()
    
    except:
        print('error')



def getAll():

    try:
        con = create_connect()
        try:

            with con.cursor() as cur:
              
                getAllUserCommand = 'SELECT * FROM USERS'
                cur.execute(getAllUserCommand)
                
                rows = cur.fetchall()
                
                if (rows == None):
                        return

                print(rows)
                
                userList = []

                for row in rows:
                    user_id = row['user_id']
                    login = row['login']
                    password = row['password']
                    nickname = row['nickname']

                    user = User(user_id, login, password, nickname)
                    userList.append(user)

                return userList


        finally:
            con.close()
    
    except:
        print('error')
    

def getById(user_id):
    

    try:
        con = create_connect()
        try:

            with con.cursor() as cur:
              
                getUserByIdCommand = 'SELECT * FROM USERS WHERE USER_ID = %s;'
                cur.execute(getUserByIdCommand, user_id)
                
                row = cur.fetchone()
                
                if (row == None):
                        return

                print(row)

                
                login = row['login']
                password = row['password']
                nickname = row['nickname']

                user = User(user_id, login, password, nickname)

                return user


        finally:
            con.close()
    
    except:
        print('error')


if __name__ == '__main__':

    user = getById(2189)

    user.nickname = 'newNickname'

    update(user)

   