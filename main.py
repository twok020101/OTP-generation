from mimetypes import init
from random import randint
import requests
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv('.env')

print(os.environ.get("passoword"))

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.environ.get("password"),
    database="users"
)
mycursor = mydb.cursor()
token = os.environ.get("token")
endpoint = os.environ.get("endpoint")

class OneTimePasswordGenerator:
    def generator(self):
        return randint(1000,10000)

class DatabaseManagement:
    def __init__(self,name,number) -> None:
        self.name=name
        self.number=number
    
    def insert(self):
        otp=OneTimePasswordGenerator.generator(self)
        sql="insert into customers (name,phone_number,otp,verify_status) values (%s,%s,%s,%s)"
        val=(self.name,self.number,otp,0)
        mycursor.execute(sql,val)
        mydb.commit()
        return otp

    def modifyStatus(self):
        sql="update customers set verify_status=1 where phone_number=%s"
        val=(self.number,)
        mycursor.execute(sql,val)
        mydb.commit()

    def checkNumber(self):
        sql="select * from customers where phone_number=%s"
        val=(self.number)
        mycursor.execute(sql,(val,))
        res=mycursor.fetchall()
        if len(res)>0:
            return True
        return False

    def checkValidation(self):
        sql="select verify_status,otp from customers where phone_number=%s"
        val=(self.number)
        mycursor.execute(sql,(val,))
        res=mycursor.fetchall()
        for status,otp in res:
            if status==0:
                return False,otp
            else:
                return True,otp


class ApiManagement:
    def __init__(self,number) -> None:
        self.url = "https://"+endpoint+"/api/v1/"
        self.number=number
    
    def addPhoneNumber(self):
        self.url+="addContact/"+str("91"+str(self.number))
        headers = {
                "Content-Type": "text/json",
                "Authorization": token
            }
        response = requests.post(self.url, headers=headers)
        print(response.text)

    def sendOTP(self,otp):
        url="https://"+endpoint+"/api/v1/sendTemplateMessage?whatsappNumber="+str("91"+str(self.number))
        headers = {
                "Content-Type": "text/json",
                "Authorization": token
            }
        payload = {
                "parameters": [
                    {
                        "name": "one_time_password",
                        "value": str(otp)
                    }
                ],
                "broadcast_name": "my",
                "template_name": "one_time_password_template"
            }
        response = requests.post(url, json=payload, headers=headers)
        print(response.text)
    
class Customer:
    def __init__(self) -> None:
        self.name=input("Enter your name: ")
        self.number=int(input("Enter your number: "))
        self.databaseobj=DatabaseManagement(self.name,self.number)
        self.apiobj=ApiManagement(self.number)

    def addIntoDb(self):
        if self.databaseobj.checkNumber():
            status,otp = self.databaseobj.checkValidation()
            if status==True:
                print("Number is already verified!")
            else:
                print("Number is added but not verified")
                self.apiobj.sendOTP(otp)
                self.verifyOtp(otp)

        else:
            otp=self.databaseobj.insert()
            self.apiobj.sendOTP(otp)
            self.verifyOtp(otp)

    def verifyOtp(self,otp):
        enotp=int(input())
        if enotp==otp:
            self.databaseobj.modifyStatus()
            print("Verified")

if __name__=="__main__":
    x=Customer()
    x.addIntoDb()