import pymysql.cursors
import pymysql
import os
import sys


databaseConnection = {
    "host": 'localhost',
    "user": 'suhasnidgundi',
    "password": 'Suhas@123',
    "db": 'scnj',
    "charset": 'utf8',
    "cursorclass": pymysql.cursors.DictCursor
}


connectionString = databaseConnection

def getDatafromDatabase(query):
    con2 = pymysql.connect(**connectionString)

    try:

        with con2.cursor() as c:
            c.execute(query)
            row = c.fetchall()

            for r in row:
                for ibjs in r:
                    ## Write a function for this ##
                    if type(r[ibjs]) == bytes:
                        print(str(r[ibjs]))
                        if r[ibjs] == b'\x00':
                            r[ibjs] = False
                        elif r[ibjs] == b'\x01':
                            r[ibjs] = True

        return row
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        raise Exception(str(err))
    finally:
        con2.close()


def insertData(query):
    con2 = pymysql.connect(**connectionString)

    try:
        with con2.cursor() as c:
            c.execute(query)
            con2.commit()

        return True
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        raise Exception(str(err))
    finally:
        con2.close()


def atomic_connection():
    con2 = pymysql.connect(**connectionString)
    return con2

# def main():
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'milkData.settings')
#     try:
#         from django.core.management import execute_from_command_line
#     except ImportError as exc:
#         raise ImportError(
#             "Couldn't import Django. Are you sure it's installed and "
#             "available on your PYTHONPATH environment variable? Did you "
#             "forget to activate a virtual environment?"
#         ) from exc
#     execute_from_command_line(sys.argv)


# if __name__ == '_main_':
#     main()

# con = pymysql.connect(host='10.10.0.237',
#         user='yottadevmysqluser',
#         password='SmkYotta!2008@0501',
#         db='testdata')


# con2 = pymysql.connect(host="10.10.0.106", user="userforwin", password="MYpoftit@2392", db='sutrapos')

# con2 = pymysql.connect(host="localhost", user="root", password="sC8hUY@123", db='sutrapos')
