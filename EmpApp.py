# from flask import Flask, render_template, request
# from pymysql import connections
# import os
# import boto3
# from config import *
# import mysql.connector

# app = Flask(__name__)

# bucket = custombucket
# region = customregion

# # db_conn = connections.Connection(
# #     host=customhost,
# #     port=3306,
# #     user=customuser,
# #     password=custompass,
# #     db=customdb
# # )

# connection = mysql.connector.connect(
#     host=customhost,
#     port=3306,
#     user=customuser,
#     password=custompass,
#     db=customdb
# )

# output = {}
# table = 'employee'


# def getEmp():

#     try:
#         # Define a SQL SELECT Query
#         select_sql = "SELECT * FROM employee"
#         # Get Cursor Object from Connection
#         cursor = connection.cursor()
#         # Execute the SELECT query using execute() method
#         cursor.execute(select_sql)
#         # Extract all rows from a result
#         records = cursor.fetchall()
#         try:
#             # create an array to display employee records at html
#             # employees = []
#             print(records)
#             print("Total number of rows in table: ", cursor.rowcount)
#             for row in records:
#                 print("row = ", row)
#                 emp_id = row[0]
#                 print("emp_id = ", row[0], )
#                 first_name = row[1]
#                 print("first_name = ", row[1])
#                 last_name = row[2]
#                 print("last_name  = ", row[2])
#                 pri_skill = row[3]
#                 print("pri_skill  = ", row[3])
#                 location = row[4]
#                 print("location = ", row[4], "\n")

#                 # employees.append(
#                 #     {"emp_id": row[0], "first_name": row[1], "last_name": row[2], "pri_skill": row[3], "location": row[4]})

#         except Exception as e:
#             return str(e)
#     except connections.Error as e:
#         print("Error reading data from MySQL table", e)
#     finally:
#         if connection.is_connected():
#             connection.close()
#             cursor.close()
#             print("MySQL connection is closed")
#     return render_template('index.html')


# # route to home
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     # return getEmp()
#     return render_template("index.html")


# @app.route("/about", methods=['POST'])
# def about():
#     return render_template('www.intellipaat.com')


# @app.route("/addemp")
# def addemp():
#     return render_template('AddEmp.html')


# @app.route("/test")
# def test():
#     print('I got clicked!')
#     # return getEmp()
#     # getEmp()
#     return 'Click.'


# @app.route("/addemp", methods=['POST'])
# def AddEmp():
#     emp_id = request.form['emp_id']
#     first_name = request.form['first_name']
#     last_name = request.form['last_name']
#     pri_skill = request.form['pri_skill']
#     location = request.form['location']
#     emp_image_file = request.files['emp_image_file']

#     insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
#     cursor = connection.cursor()

#     if emp_image_file.filename == "":
#         return "Please select a file"

#     try:

#         cursor.execute(insert_sql, (emp_id, first_name,
#                        last_name, pri_skill, location))
#         connection.commit()
#         emp_name = "" + first_name + " " + last_name
#         # Uplaod image file in S3 #
#         emp_image_file_name_in_s3 = "emp-id-" + str(emp_id) + "_image_file"
#         s3 = boto3.resource('s3')

#         try:
#             print("Data inserted in MySQL RDS... uploading image to S3...")
#             s3.Bucket(custombucket).put_object(
#                 Key=emp_image_file_name_in_s3, Body=emp_image_file)
#             bucket_location = boto3.client(
#                 's3').get_bucket_location(Bucket=custombucket)
#             s3_location = (bucket_location['LocationConstraint'])

#             if s3_location is None:
#                 s3_location = ''
#             else:
#                 s3_location = '-' + s3_location

#             object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
#                 s3_location,
#                 custombucket,
#                 emp_image_file_name_in_s3)

#         except Exception as e:
#             return str(e)

#     finally:
#         cursor.close()

#     print("all modification done...")
#     return render_template('AddEmpOutput.html', name=emp_name)


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=80, debug=True)

from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
from config import *

app = Flask(__name__)

bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb
)
output = {}
table = 'employee'


def getEmp():

    try:
        # Define a SQL SELECT Query
        select_sql = "SELECT * FROM employee"
        # Get Cursor Object from Connection
        cursor = db_conn.cursor()
        # Execute the SELECT query using execute() method
        cursor.execute(select_sql)
        # Extract all rows from a result
        records = cursor.fetchall()
        try:
            print(records)
            print("Total number of rows in table: ", cursor.rowcount)
            for row in records:
                print("row = ", row)
                emp_id = row[0]
                print("emp_id = ", row[0], )
                first_name = row[1]
                print("first_name = ", row[1])
                last_name = row[2]
                print("last_name  = ", row[2])
                pri_skill = row[3]
                print("pri_skill  = ", row[3])
                location = row[4]
                print("location = ", row[4], "\n")
        except Exception as e:
            return str(e)
    except connections.Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if connections.is_connected():
            connections.close()
            cursor.close()
            print("MySQL connection is closed")
    return render_template('index.html', emp_id=emp_id, first_name=first_name)


# route to home
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@app.route("/about", methods=['POST'])
def about():
    return render_template('www.intellipaat.com')


@app.route("/addemp")
def addemp():
    return render_template('AddEmp.html')


@app.route("/test")
def test():
    print('I got clicked!')
    # return getEmp()
    return 'Click.'


@app.route("/addempSubmit", methods=['POST'])
def AddEmp():
    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    pri_skill = request.form['pri_skill']
    location = request.form['location']
    emp_image_file = request.files['emp_image_file']

    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    if emp_image_file.filename == "":
        return "Please select a file"

    try:

        cursor.execute(insert_sql, (emp_id, first_name,
                       last_name, pri_skill, location))
        db_conn.commit()
        emp_name = "" + first_name + " " + last_name
        # Uplaod image file in S3 #
        emp_image_file_name_in_s3 = "emp-id-" + str(emp_id) + "_image_file"
        s3 = boto3.resource('s3')

        try:
            print("Data inserted in MySQL RDS... uploading image to S3...")
            s3.Bucket(custombucket).put_object(
                Key=emp_image_file_name_in_s3, Body=emp_image_file)
            bucket_location = boto3.client(
                's3').get_bucket_location(Bucket=custombucket)
            s3_location = (bucket_location['LocationConstraint'])

            if s3_location is None:
                s3_location = ''
            else:
                s3_location = '-' + s3_location

            object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                s3_location,
                custombucket,
                emp_image_file_name_in_s3)

        except Exception as e:
            return str(e)

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('AddEmpOutput.html', name=emp_name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
