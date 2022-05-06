import mysql.connector
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv('.env')

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.environ.get("password"),
    database="users"
)
mycursor = mydb.cursor()

class DatabaseManagement(object):
    def __init__(self,arn) -> None:
        self.arn=arn

    def arnStatus(self):
        sql="select Name,Email,ARNExpiry from arndata where arn=%s"
        val=(self.arn)
        mycursor.execute(sql,(val,))
        res= mycursor.fetchone()
        if res!=None:
            if DatabaseManagement.checkExpiry(self,res[2]):
                return res[1]
            else:
                return "Your arn is expired"
        return "Not valid arn"

    def checkExpiry(self,date):
        curr=datetime.now()
        expdate=datetime.strptime(date,"%d-%b-%Y")
        if (expdate-curr).total_seconds()<0:
            return False
        else:
            return True

def responder(arn):
    cust=DatabaseManagement(arn)
    return(cust.arnStatus())
