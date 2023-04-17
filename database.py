

#from dotenv import load_dotenv
#load_dotenv()
#import os
import sys
sys.path.insert(1,r'C:\Users\encre\OneDrive\Desktop\2023_Learning_Vault_Atulya\Credentials')
def dbquery(query_string):
    import sys
    sys.path.insert(1,r'C:\Users\encre\OneDrive\Desktop\2023_Learning_Vault_Atulya\Credentials')
    from credentials import credential_mysql
    import sqlalchemy
    from sqlalchemy import create_engine, text
    import pymysql
    import pandas as pd
    
    db_string = credential_mysql()
    engine = create_engine(db_string,
    connect_args={
        "ssl":{
            "ssl_ca": "/etc/ssl/cert.pem"
        }
    })

    with engine.connect() as conn:
        result = conn.execute(text(query_string))
        res= []
        for row in result.all():
            res.append((row))
    
    if "tweetcon" in query_string:
        with engine.connect() as conn:
            result = conn.execute(text(query_string))
            res= []
            for row in result.all():
                res.append((row))
        return res
    
    else:
        df = pd.read_sql("query_string",con=engine)
        
        return df   
    
    
            
        #return res 
        #print(result.all())
        
def df_to_sql(df):
    import sqlalchemy
    import mysql.connector
    from sqlalchemy import create_engine
    import pandas as pd
    import sys
    sys.path.insert(1,r'C:\Users\encre\OneDrive\Desktop\2023_Learning_Vault_Atulya\Credentials')
    from credentials import credential_mysql
    
    
    db_string = credential_mysql()
    engine = create_engine(db_string,
    connect_args={
        "ssl":{
            "ssl_ca": "/etc/ssl/cert.pem"
        }
    })
    #q=""
    #df = pd.read_sql_query(q,con=engine)
    #data = {'product_name': ['Computer','Tablet','Monitor','Printer'],
        #'price': [900,300,450,150]
        #}

    df = pd.DataFrame(df, columns= ['product_name','price'])
    df.to_sql(name='tabletest',con=engine, if_exists = 'append',index=False)
    
    return df


    
    #return    
#print(df_to_sql())    
    