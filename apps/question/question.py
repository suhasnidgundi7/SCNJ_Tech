from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import Response
from db import insertData, getDatafromDatabase, atomic_connection
import os
import sys



questionroute = APIRouter()

@questionroute.post('/viewquestionset/')
async def viewQuestionset(request:Request):
    try:
        request_data = await request.json()
        
        query = ''
        for a, b in request_data.items():
            query = query + f"{a} = '{b}' and "
            
        sqlquery = f'select * from questionsetheader where  '
        sqlquery = sqlquery + query

        if sqlquery.endswith('where '):
            sqlquery = sqlquery.replace('where ', '')
        else:
            sqlquery = sqlquery[:len(sqlquery)-5]
        
        questions = getDatafromDatabase(sqlquery)

        for question in questions:
            footerQuery = f'''select qf.*, (select descn from questionmaster where recno = qf.questionrecno) as questiondescn from questionsetfooter qf where questionsetrecno = {question['recno']}'''
            footer = getDatafromDatabase(footerQuery)

            question['questionslist']= footer
            
        return {'Success': True, 'Message':questions}     

    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'Success': False, 'Message': str(err)}


@questionroute.post("/questionset/")
async def addQuestionset(request:Request):
    try:
        request_data = await request.json()

        descn = request_data['descn']
        type = request_data['type']

        sqlquery = f'''insert into questionsetheader(descn, type) values('{descn}', '{type}')'''
        add=insertData(sqlquery)
        
        if add==True:
            sqlquery1 = f''' SELECT recno FROM questionsetheader ORDER BY recno DESC LIMIT 1 '''
            getSet = getDatafromDatabase(sqlquery1)
            return{'Success': True, 'Message':getSet}

        return {'Success': True, 'Message':'Succesfully Added'}

    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'Success': False, 'Message': str(err)}


# @questionroute.patch("/questionset/")
# async def updateQuestionset(request:Request):
#     try:
#         request_data = await request.json()

#         recno = request_data['recno']
#         sqlquery = f'''select * from questionsetheader where recno='{recno}' '''
#         check=getDatafromDatabase(sqlquery)

#         if len(check)>0:        
#             descn = request_data['descn']
#             type = request_data['type']
#             sqlquery = f'''update questionsetheader set descn='{descn}', type='{type}' where recno={recno} '''
#             add=insertData(sqlquery)

#             footers = request_data['footer']
#             for footer in footers:
#                 questionsetrecno = footer['questionsetrecno']
#                 subquestion = footer['subquestion']
#                 sqlquery = f'''update questionsetfooter set questionsetrecno='{questionsetrecno}', subquestion='{subquestion}' where recno={recno} '''
#                 add=insertData(sqlquery)
#             return {'Success': True, 'Message':'Succesfully Update'}

#     except Exception as err:
#         exc_type, exc_obj, exc_tb = sys.exc_info()
#         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#         print(exc_type, fname, exc_tb.tb_lineno)
#         return {'Success': False, 'Message': str(err)}

@questionroute.delete("/questionset/")
async def delectQuestionset(request:Request):
    try:
        request_data = await request.json()

        recno = request_data['recno']
        
        sqlquery = f'''update questionsetheader set active = 0 where recno={recno}'''
        delete=insertData(sqlquery)
        return {'Success': True, 'Message':'Succesfully Delete'}

    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'Success': False, 'Message': str(err)}



#CURD opration for questionmaster 

@questionroute.get("/question/")
async def viewQuestion(request:Request):
    try:
        
        sqlquery = f'''select * from questionmaster where active = 1 '''
        view=getDatafromDatabase(sqlquery)
        return {'Success': True, 'Message':view}

    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'Success': False, 'Message': str(err)}

@questionroute.post("/question/")
async def addQuestion(request:Request):

    try:
        request_data = await request.json()

        questiontype = request_data['questiontype']
        descn = request_data.get('descn',"")
        choice = request_data.get('choice',"")

        sqlquery = f'''insert into questionmaster(descn, questiontype, choice) values ('{descn}', '{questiontype}', '{choice}') '''
        addQuestion=insertData(sqlquery)
        return {'Success': True, 'Message':'Succesfully Added'}
        
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'Success': False, 'Message': str(err)}
  

@questionroute.patch("/question/")
async def updateQuestion(request:Request):
    try:
        request_data = await request.json()

        recno = request_data['recno']
        questiontype = request_data['questiontype']
        descn = request_data['descn']
        choice = request_data.get('choice')
        sqlquery = f'''update questionmaster set descn='{descn}', questiontype='{questiontype}', choice='{choice}' where recno='{recno}' '''
        updateQuestion=insertData(sqlquery)
        return {'Success': True, 'Message':'Succesfully Update'}
        
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'Success': False, 'Message': str(err)}

@questionroute.post("/deletequestion/")
async def deleteQuestion(request:Request):
    try:
        request_data = await request.json()
        recno = request_data['recno']
        
        sqlquery = f''' update questionmaster set active = 0 where recno={recno} '''
        deleteQuestion=insertData(sqlquery)
        return {'Success': True, 'Message':'Succesfully Delete'}

    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'Success': False, 'Message': str(err)}




@questionroute.post("/filterquestionsetfooter/")
async def filter(request:Request):
    try:
        request_data = await request.json()
        questionset = request_data['questionset']
        
        sqlquery = f''' select qh.*, q.* from questionsetfooter qh inner join questionmaster q on q.recno = qh.questionrecno where questionsetrecno ='{questionset}' '''
        
        Question=getDatafromDatabase(sqlquery)
        return {'Success': True, 'Message':Question}

    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'Success': False, 'Message': str(err)}



@questionroute.post("/addquestionsetfooter/")
async def questionsetArr(request:Request):
    try:
        request_data = await request.json()

        for questions in request_data:

            questionsetrecno = questions['questionsetrecno']
            subquestion = questions.get('subquestion', 0)
            questionrecno = questions['recno']

            sqlquery = f''' insert ignore into questionsetfooter (questionsetrecno, subquestion, questionrecno) values ('{questionsetrecno}','{subquestion}', '{questionrecno}') '''
            addQuestion=insertData(sqlquery)
        return {'Success': True, 'Message':"Question Set Added Successfully"}

    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'Success': False, 'Message': str(err)}


 