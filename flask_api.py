from flask import Flask,request
import onlyotp
from inspect import getmembers, isfunction
import json


app=Flask(__name__)

@app.route('/requestotp',methods=['POST'])
def requestotp():
    args=request.args
    number=args.get('number','')
    otp=args.get('otp','')
    response=onlyotp.main(number,otp)
    return json.dumps(response),200

if __name__=="__main__":
    app.run(threaded=True)
    print(getmembers(onlyotp,isfunction))
    


