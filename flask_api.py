from flask import Flask,request
import WATI_Module.ApiManagementModule as wa
import json
import EmailAutomation.main as em


app=Flask(__name__)

class DataStore():
    originalOtp = None

data = DataStore()

@app.route('/requestotp',methods=['POST'])
def requestotp():
    args=request.args
    number=args.get('number','')
    otp=args.get('otp','')
    response=wa.sender(number,otp)
    return json.dumps(response),200

@app.route('/sendmail',methods=['POST'])
def sendmail():
    args=request.args
    email=args.get('email','')
    otp_verify=args.get('otp','')
    data.originalOtp=otp_verify
    response=em.main(email,otp_verify)
    return json.dumps(response)

@app.route('/checkotp',methods=['POST'])
def checkotp():
    args=request.args
    otpreceived=args.get('otp','')
    response=wa.receiveOtp(data.originalOtp,otpreceived)
    if response==True:
        return "Veification Successful"
    else:
        return "We dont have you in our database please leave us a message with your contact info."

if __name__=="__main__":
    app.run(threaded=True)
    
    


