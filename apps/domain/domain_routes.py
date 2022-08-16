from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import Response
from db import insertData, getDatafromDatabase, atomic_connection
import os
import sys

domainroute = APIRouter()


@domainroute.post("/newregister/")
async def newRegister(request:Request):
    
    try:
        request_data = await request.json()
        descn = request_data['descn']
        mobile = request_data['mobile']
        email = request_data['email']
        industry = request_data['industry']
        keywords = request_data['keyword']

        sqlquery = f"insert into domain(descn, mobile, email, industry, keyword) values('{descn}', {mobile}, '{email}', '{industry}', '{keywords}')"
        addInfo = insertData(sqlquery)
        
        users = request_data['user']
        for user in users:
            loginid = user['loginid']
            pwd = user['pwd']
            userType = user.get('usertype', 2)
            sqlquery1 = f'''insert into domainuser(loginid, pwd, domainrecno, usertype) values ("{loginid}", "{pwd}",(SELECT recno FROM domain ORDER BY recno DESC LIMIT 1), {userType}) '''
            addInfo = insertData(sqlquery1)

        return {'Success': True, 'Message': 'Succesfully Added'}

    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'Success': False, 'Message': str(err)}


@domainroute.post("/viewprofile/")
async def viewProfile(request:Request):
    
    try:
        request_data = await request.json()
        
        recno = request_data['recno']
        sqlquery = f"select * from domain where recno='{recno}' "
        
        profile = getDatafromDatabase(sqlquery)
        for doc in profile:
            footerQuery = f'''select * from domainuser where domainrecno = {doc['recno']}'''
            user = getDatafromDatabase(footerQuery)

            doc['user']= user

        return {'Success': True, 'Message':profile }

    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'Success': False, 'Message': str(err)}


@domainroute.patch('/updateprofile/')
async def updateProfile(request:Request):
    
    try:
        request_data = await request.json()
        recno = request_data['recno']
        descn = request_data['descn']
        mobile = request_data['mobile']
        email = request_data['email']
        address = request_data['address']
        contactperson = request_data['contactperson']
        designation = request_data['designation']
        registeras = request_data['registeras']
        companytype = request_data['companytype']
        gst = request_data['gst']
        pan = request_data['pan']
        city = request_data['city']
        state = request_data['state']
        industry = request_data['industry']
        keywords = request_data['keyword']

        sqlquery = f'''select recno from domain where recno='{recno}' '''
        checkprofile=getDatafromDatabase(sqlquery)

        if len(checkprofile)>0:

            sqlquery = f"update domain set descn='{descn}', mobile={mobile}, email='{email}', address='{address}', contactperson='{contactperson}', designation='{designation}', registeras={registeras}, companytype={companytype}, gst={gst}, pan={pan}, city='{city}', state='{state}', industry='{industry}', keyword='{keywords}' where recno={recno}"
            update = insertData(sqlquery)

            users = request_data['user']
            for user in users:
                loginid = user['loginid']
                # usertype = user['usertype']
                sqlquery = f'''update domainuser set loginid='{loginid}' where loginid='{loginid}' '''
                update = insertData(sqlquery)

            return {'Success': True, 'Message': 'Succesfully Update'}

    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'Success': False, 'Message': str(err)}

