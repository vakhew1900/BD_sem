from re import X
from connectionDB import create_connect


def getPublisherById(publisher_id):
    

    try:
        con = create_connect()
        try:

            with con.cursor() as cur:
              
                getPublisherByIdCommand = 'SELECT * FROM publishers WHERE publisher_id = %s;'
                cur.execute(getPublisherByIdCommand, publisher_id)
                
                row = cur.fetchone()
                
                if (row == None):
                        return

                # print(row)

                publisher_name = row['publisher_name']
                return publisher_name


        finally:
            con.close()
    
    except:
        print('error')


def getAllPublishers():
    
    try:
        con = create_connect()
        try:

            with con.cursor() as cur:
              
                getPublisherCommand = 'SELECT * FROM publishers;'
                cur.execute(getPublisherCommand)
                
                rows = cur.fetchall()
                
              
                if (rows == None):
                        return

                # print(rows)

                names = []
                id = []
                for row in rows:
                    publisher_name = row['publisher_name']
                    names.append(publisher_name)
                    id.append(row['publisher_id'])

                return id, names


        finally:
            con.close()
    
    except:
        print('error')


def getDeveloperById(developer_id):
    

    try:
        con = create_connect()
        try:

            with con.cursor() as cur:
              
                getDeveloperByIdCommand = 'SELECT * FROM developers WHERE developer_id = %s;'
                cur.execute(getDeveloperByIdCommand, developer_id)
                
                row = cur.fetchone()
                
                if (row == None):
                        return

                # print(row)

                publisher_name = row['developer_name']
                return publisher_name


        finally:
            con.close()
    
    except:
        print('error')


def getAllDevelopers():
    
    try:
        con = create_connect()
        try:

            with con.cursor() as cur:
              
                getDeveloperCommand = 'SELECT * FROM developers;'
                cur.execute(getDeveloperCommand)
                
                rows = cur.fetchall()
                
              
                if (rows == None):
                        return

                # print(rows)

                names = []
                id = []
                for row in rows:
                    publisher_name = row['developer_name']
                    names.append(publisher_name)
                    id.append(row['developer_id'])

                return id, names


        finally:
            con.close()
    
    except:
        print('error')

# getDeveloperById(1)
# getAllDevelopers()