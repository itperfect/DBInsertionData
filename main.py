import string
import random

import mysql.connector
from email_validator import validate_email

from datetime import datetime

SETTINGS = {
    'DB_HOST': '127.0.0.1',
    'DB_USER': 'root',
    'DB_PASWD': '',
    'DB_NAME': 'test1',
    'DB_TBL': 'users',

    'DATA_FILE': '1644055729399687.100000'
}

t0 = datetime.timestamp(datetime.now())
clean_data = []
with open(SETTINGS['DATA_FILE'], 'r') as f_data:
    valid_file = True
    for str_data in f_data:
        str_data = str_data.replace('\r\n', '').replace('\n', '').replace('\r', '').strip()
        try:
            valid = validate_email(str_data, check_deliverability=False)
        except:
            # print("ERROR! This is not email: {}".format(str_data))
            valid_file = False
            clean_data = []
            break
        else:
            clean_data.append(str(valid.email).lower())
            # print("This is email: {}".format(valid.email))

    if valid_file:
        clean_data = list(set(clean_data))
        print("File validation: OK {} records".format(len(clean_data)))
    else:
        print("File validation: ERROR")

    del valid_file, f_data, str_data, valid
print(datetime.timestamp(datetime.now()) - t0)


def is_email_exist(cursorr: mysql.connector.connect().cursor = None, emaill: str = None):
    result = False
    query = ("SELECT COUNT(*) FROM users WHERE email=%(val)s")
    cursorr.execute(query, {'val': emaill})

    if cursorr.fetchone()[0] == 1:
        result = True

    return result


if len(clean_data) > 1:
    print("STARTING IMPORT")
    t0 = datetime.timestamp(datetime.now())
    cnt = 0
    skipped = stored = 0
    records = len(clean_data)
    with mysql.connector.connect(user=SETTINGS['DB_USER'], password=SETTINGS['DB_PASWD'],
                                 database=SETTINGS['DB_NAME'], host=SETTINGS['DB_HOST']) as conn:
        with conn.cursor() as cursor:
            for email in clean_data:
                u_name = ''.join(random.choices(string.ascii_lowercase, k=7))

                if is_email_exist(cursor, email):
                    print("Skipping: {}: ".format(email))
                    skipped += 1
                else:
                    query = ("INSERT INTO users (`name`, `email`) VALUES (%s, %s)")
                    query_data = (u_name, email)
                    cursor.execute(query, query_data)
                    print("Storing email: {}".format(email))
                    stored += 1

                cnt += 1
                print("{} records left to proceed".format(records-cnt))

            print("START STORING RESULTS - ", end='')
            conn.commit()
            print("SUCCESS")

            # for res in cursor:
            #     print(res)

            print("Skipped emails: {}".format(skipped))
            print("Stored emails: {}".format(stored))
            print("{} seconds".format(datetime.timestamp(datetime.now()) - t0))

if __name__ == '__main__':
    pass

