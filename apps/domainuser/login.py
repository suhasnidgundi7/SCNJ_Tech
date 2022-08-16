from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import Response
from db import insertData, getDatafromDatabase
import os
import sys


loginroute = APIRouter()


@loginroute.post("/login/")
async def login(request:Request):
    
    try:
        request_data = await request.json()
        loginid = request_data['loginid']
        pwd = request_data['pwd']

        sqlquery = f"select recno as userrecno,domainrecno,loginid,usertype from domainuser where loginid = '{loginid}' and pwd = '{pwd}'"
        login = getDatafromDatabase(sqlquery)
    
        if len(login)>0:
            return {'Success': True, 'Message': login}
        
        else :
            raise Exception("Login and Password Do not Match")

    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'Success': False, 'Message': str(err)}


@loginroute.post("/changepassword/")
async def changePassword(request:Request):
            try:
                request_data = await request.json()

                loginid = request_data['loginid']
                newpwd = request_data['pwd']
                oldpwd = request_data['oldpwd']
                
                # Check the Old password first
                # If entry by loginId and Oldpassword exists
                # Then Chage password
                # Otherwise Do not change password

                ### Check if the Old password and Login ID matches
                verifyOldPasswordquery = f'''select recno from domainuser where loginid = '{loginid}' and pwd = '{oldpwd}' '''
                userObj = getDatafromDatabase(verifyOldPasswordquery)
                
                # If login and password is correct then chagne password
                if len(userObj)>0:
                    # Change the Password for the user
                    sql = f" update domainuser set pwd ={newpwd} where loginid= '{loginid}' "
                    new=insertData(sql)

                    if new != True:
                        raise Exception(new)
                else:
                    raise Exception("Login and Password Do not Match")

                return {'Success':True, 'Message' : 'Password Changed' }
                
            except Exception as err:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                return{'Success': False,'Message': str(err)}


@loginroute.post("/forgetpassword/")
async def forgetPassword(request:Request):
            try:
                request_data = await request.json()
                loginid = request_data['loginid']
                newpwd = request_data['pwd']

                verifylogin = f'''select * from domainuser where loginid = '{loginid}' '''
                userObj = getDatafromDatabase(verifylogin)

                if len(userObj) > 0:
                    sql = f" update domainuser set pwd ='{newpwd}' where loginid = '{loginid}' "
                    forgetpwd=insertData(sql)
                    return{'Success':True, 'Message' : 'Password Changed'}
                    
                else:
                    raise Exception("Login Do not Match")

            
            except Exception as err:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                return{'Success': False,'Message': str(err)}
