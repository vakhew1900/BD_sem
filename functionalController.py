from connectionDB import create_connect



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
                if (row != None):
                     estimation = float(row['estimation'])

                     
                return estimation

        finally:
            con.close()
    
    except:
        print('error')


if __name__ == '__main__':

    x = getEstimation()
    print(x)