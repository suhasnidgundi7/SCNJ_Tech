from datetime import datetime
from typing import Union
from fastapi import APIRouter
from starlette.requests import Request
from db import insertData, getDatafromDatabase, atomic_connection
import random, base64
import os
import sys
from utils import getlocaltime, convert_blob
from fastapi_utils.tasks import repeat_every
import requests, json

docroute = APIRouter()



@docroute.post("/viewdocument/")
async def viewDocument(request:Request):
    try:
        request_data = await request.json()
        
        query = ''
        for a, b in request_data.items():
            if a == 'fromdate':
                query = query + f''' trdate >= {b}'''
            elif a == 'todate': 
                query = query + f''' trdate <= {b}'''
            elif b == None:
                pass
            else:
                query = query + f''' {a} = '{b}' and '''

        sqlquery = f'select doc.*, (select descn from domain where recno = doc.domainrecno) as domaindescn, (select loginid from domainuser where domainrecno = doc.domainrecno)as userdescn from docmaster doc where doc.active = 1 and ' 
        sqlquery = sqlquery + query

        if sqlquery.endswith('where '):
            sqlquery = sqlquery.replace('where ', '')
        else:
            sqlquery = sqlquery[:len(sqlquery)-5]
        documents = getDatafromDatabase(sqlquery)

        for doc in documents:
            footerQuery = f'''select df.*, (select descn from questionmaster where recno = df.questionrecno) as questiondescn from docfooter df where docmasterrecno = {doc['recno']}'''
            footer = getDatafromDatabase(footerQuery)
            for img in footer:
                    for key, value in img.items():
                        if key == 'img':
                            
                            if value:
                                convertedimage = base64.b64encode(value)
                                img['img'] = convertedimage

            connection = f'''select * from docconnect where bdocrecno = {doc['recno']} or sdocrecno = {doc['recno']} '''
            viewconnection = getDatafromDatabase(connection) 


            doc['questionslist']= footer
            doc['connectdocument']=viewconnection
       
        return {'Success': True, 'count':len(viewconnection),  'Message':documents}     

    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'Success': False, 'Message': str(err)}

@docroute.post("/adddocument/")
async def addDocument(request:Request):
    con2 = atomic_connection()
    try:
        request_data = await request.json()

        with con2.cursor() as c:
            domainrecno =request_data['domainrecno']
            domainuserrecno =request_data['domainuserrecno']
            doctype = request_data['doctype']
            trdate = datetime.now().strftime("%Y/%m/%d")
            trtime = getlocaltime()
            status = request_data.get('status',1)
            active = request_data.get('active')
            code = random.randint(0000,9999)
            descn = request_data['descn']

            sqlquery = f'''insert into docmaster(domainrecno, domainuserrecno, doctype, trdate, trtime, status, active, code, descn) values ('{domainrecno}', '{domainuserrecno}', '{doctype}', '{trdate}','{trtime}', '{status}', '{active}', '{code}', '{descn}')'''
            c.execute(sqlquery)

            footers = request_data['footer']
            for footer in footers:
                questionrecno = footer['questionrecno']
                answer = footer.get('answer', '')
                img = footer.get('img', " ")

                img = convert_blob("base64", img)
                
                sqlquery = '''insert into docfooter(questionrecno, answer, img, docmasterrecno) values (%s, %s,%s, (SELECT recno FROM docmaster ORDER BY recno DESC LIMIT 1))'''

                c.execute(sqlquery, [questionrecno, answer, img])

            con2.commit()
            
        return {'Success': True, 'Message':'Succesfully Added'}
        
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'Success': False, 'Message': str(err)}

    finally:
        con2.close()


@docroute.patch("/updatedocument/")
async def updateDocument(request:Request):
    try:
        request_data = await request.json()
        recno =request_data.get('recno',None)
        domainrecno =request_data['domainrecno']
        domainuserrecno =request_data['domainuserrecno']
        doctype = request_data['doctype']
        status = request_data['status']
        active = request_data['active']
        code = request_data['code']

        sqlquery = f'''select recno from docmaster where recno='{recno}' '''
        checkdoc=getDatafromDatabase(sqlquery)

        if len(checkdoc)>0:
            
            sqlquery = f'''update docmaster set domainrecno='{domainrecno}', domainuserrecno='{domainuserrecno}', doctype='{doctype}', status='{status}', active='{active}', code='{code}' where recno='{recno}' '''
            updatedoc=insertData(sqlquery)
        
            footers = request_data['questionslist']
            for footer in footers:
                recno = footer['recno']
                answer = footer['answer']
                img = footer['img']
                sqlquery = f'''update docfooter set answer='{answer}', img='{img}' where recno={recno} '''
                updatefooter=insertData(sqlquery)
                return {'Success': True, 'Message':'Succesfully Update'}
        else:
            return {'Success': False, 'Message':'Document Not Update'}

    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'Success': False, 'Message': str(err)}



@docroute.post("/deletedocument/")
async def deleteDocument(request:Request):
    try:
        request_data = await request.json()
        recno = request_data['recno']
        
        sqlquery = f''' update docmaster set active = 0 where recno={recno} '''
        deleteDoc=insertData(sqlquery)

        return {'Success': True, 'Message':'Succesfully Delete'}

    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'Success': False, 'Message': str(err)}




@docroute.post('/viewconnectdocument/')
async def viewConnectDocument(request:Request):
    try:
        request_data = await request.json()

        query = ''
        for a, b in request_data.items():
            query = query + f"{a} = '{b}' and "

        sqlquery = f'''select * from docconnect where  '''
        sqlquery = sqlquery + query

        if sqlquery.endswith('where '):
            sqlquery = sqlquery.replace('where ', '')
        else:
            sqlquery = sqlquery[:len(sqlquery)-5]

        viewConnectDoc = getDatafromDatabase(sqlquery)
        return {'Success': True, 'count':len(viewConnectDoc) ,'Message':viewConnectDoc}

    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'Success': False, 'Message': str(err)}



# @docroute.post("/trialAPI/")
# def trailAPI(itemId : int, itemName : str, itemArr : list, itemCode : Union[str, None] = "Ganesh"):
#     try:
#         print(itemId, itemName, itemArr, itemCode)
#         return True
#     except Exception as err:
#         return str(err)

@docroute.post('/connectdocument/')
async def connectDocument(request:Request):
    try:

        sql = f'''insert ignore into docconnect(bdocrecno, sdocrecno) with S as(select df.answer as S_ans, d.recno as srecno from docfooter df inner join docmaster d on d.recno = df.docmasterrecno where d.doctype ='S'), B as(select df.answer as B_ans, d.recno as drecno from docfooter df inner join docmaster d on d.recno = df.docmasterrecno where d.doctype ='B') select srecno,drecno from S join B where S_ans like CONCAT('%',B_ans,'%') '''
        connection = insertData(sql)

        return {'Success': True, 'Message':'connected'}

    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'Success': False, 'Message': str(err)}



@docroute.on_event("startup")
@repeat_every(seconds=60)  # 1 hour
def remove_expired_tokens_task() -> None:
    url = "http://127.0.0.1:8000/api/v1/connectdocument/"
    res = requests.post(url)
    reuslt = (json.dumps(res.json()))
    

