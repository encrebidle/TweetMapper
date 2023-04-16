import sqlalchemy
from sqlalchemy import create_engine, text
import pymysql
db_string = "mysql+pymysql://0c7aw7mzy7irdly78y2q:pscale_pw_RSpBT8gKEMmqlmMfseexzvesAwyE4JPao2TO2pZGvB7@aws.connect.psdb.cloud/encrebidledb?charset=utf8mb4"
engine = create_engine(db_string,
connect_args={
    "ssl":{
        "ssl_ca": "/etc/ssl/cert.pem"
    }
})

with engine.connect() as conn:
    result = conn.execute(text("select * from encrebidledb.tweetcon"))
    print(result.all())

#from dotenv import load_dotenv
#load_dotenv()
#import os
