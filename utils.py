import datetime
import pytz
import base64
from datetime import timedelta, datetime


IST = pytz.timezone('Asia/kolkata')


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]

    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def write_API_Called(apiName, data):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    date = now.strftime("%d%m%y")
    f = open(f"./Logs/ApiCalledLogs{date}.log", "a")
    f.writelines(
        [f'\n \n AT {apiName} Api Called {dt_string} \n ', f'Data Object Sent - {data} \n '])


def getlocaltime():
    datetime_ist = datetime.now(IST)
    curr_clock = datetime_ist.strftime("%H:%M:%S")
    return curr_clock

financialyear = 22

def write_logs(input):
    f = open("./custom.log", "a")
    f.writelines(input)
    f.close()

def formatForBlob(data):
    for item in data:
        for key, value in item.items():
            if key == 'logo' or key == 'logohd' or key == 'logohighres' or key == 'itemlogo' or key == 'fssaiimage' or key == 'image':
                if value:
                    convertedimage = base64.b64encode(value)
                    item[key] = convertedimage
    return data

def convert_blob(convert_from, image_to_convert):

    if convert_from == 'blob':

        res = bytes(image_to_convert, 'utf-8')

        return res

    elif convert_from == 'base64':

        res = base64.b64decode(image_to_convert)

        return res

def addDays(fromDateString, days):
    fromDate = datetime.strptime(str(fromDateString), "%Y%m%d")
    toDate = fromDate + timedelta(days=days)
    toDate = toDate.strftime("%Y%m%d")
    return toDate

def checkDataValidation(request_data, values):
    try:
        for value in values:    
            
            
            
            fromValue = value.get('fromValue', None) 
            toValue = value.get('toValue', None)
            if value['isCompulsory'] == True:
                if(request_data.get(value['key'], None) == None):
                    raise Exception(f'''{value['key']} is compulsary''')
            if type(request_data[value['key']]) != value['type']:
                if type(request_data[value['key']]) == 'int':
                    request_data[value['key']] = request_data[value['key']]
                    if type(request_data[value['key']]) != (value['type']):
                        raise Exception(f'''{value['key']} should be a {value['type']}''')
                else:
                    raise Exception(f'''{value['key']} should be a {value['type']}''')
            
            if fromValue and toValue:
                if int(request_data[value['key']]) >= fromValue and int(request_data[value['key']]) <= toValue:
                    pass
                else:
                    raise Exception(f'''Invalid value for {value['key']} ''')
            if fromValue and toValue==None:
                
                if int(request_data[value['key']]) >= fromValue:
                    pass
                else:
                    raise Exception(f'''Invalid value for {value['key']} ''')
            if fromValue==None and toValue:
                
                if int(request_data[value['key']]) <= toValue:
                    pass
                else:
                    raise Exception(f'''Invalid value for {value['key']} ''')
        return request_data
    
    except Exception as err:
        import os,sys
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        
        raise Exception(str(err))

