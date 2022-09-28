# author: Ryan Wong Yi Syen RIT3G1

from flask import Flask, render_template, request, url_for, redirect, flash
#from admin.EmpAppUpdated import adminBlueprint
from pymysql import connections
import os
import boto3
from config import *
import mysql.connector

app = Fapp = Flask(__name__)
#app.register_blueprint(adminBlueprint, url_prefix="/admin")
app.secret_key = "abc"

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

# trying to get s3 image url
s3 = boto3.client('s3')

employees = []


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/login", methods=['POST'])
def login():
    error = None
    if request.method == "POST":
        empid = request.form['id']
        password = request.form['password']
        print("id=" + empid + ', pw=' + password)
        if empid != 9999 and password != 'Bait3273':
            flash('Login unsuccessful! Please try again.💪')
            error = "invalid password!"
        else:
            flash('Login successful! 🌟')
            return redirect(url_for('index1'))
    return render_template('index.html', error=error)


def getEmp():

    try:
        employees = []
        # Define a SQL SELECT Query
        select_sql = "SELECT * FROM employee"
        # Get Cursor Object from Connection
        cursor = db_conn.cursor()
        # Execute the SELECT query using execute() method
        cursor.execute(select_sql)
        print("executed")
        # Extract all rows from a result

        for row in cursor.fetchall():
            employees.append({"emp_id": row[0], "first_name": row[1],
                             "last_name": row[2], "pri_skill": row[3], "location": row[4], "img": row[5]})

    # except mysql.connector.Error as e:
    except:
        print("Error reading data from MySQL table")
    return render_template('home.html', employees=employees)


def getEmp1():

    try:
        employees = []
        # Define a SQL SELECT Query
        select_sql = "SELECT * FROM employee"
        # Get Cursor Object from Connection
        cursor = db_conn.cursor()
        # Execute the SELECT query using execute() method
        cursor.execute(select_sql)
        # Extract all rows from a result

        for row in cursor.fetchall():
            employees.append({"emp_id": row[0], "first_name": row[1],
                             "last_name": row[2], "pri_skill": row[3], "location": row[4], "img": row[5]})

    # except mysql.connector.Error as e:
    except:
        print("Error reading data from MySQL table")
    return render_template('updateEmp.html', employees=employees)


def getEmp2():

    try:
        employees = []
        print(employees)
        # Define a SQL SELECT Query
        select_sql = "SELECT * FROM employee"
        # Get Cursor Object from Connection
        cursor = db_conn.cursor()
        # Execute the SELECT query using execute() method
        cursor.execute(select_sql)
        # Extract all rows from a result
        for row in cursor.fetchall():
            employees.append({"emp_id": row[0], "first_name": row[1],
                             "last_name": row[2], "pri_skill": row[3], "location": row[4], "img": row[5]})
        print(employees)
    # except mysql.connector.Error as e:
    except:
        print("Error reading data from MySQL table")
    return render_template('deleteEmp.html', employees=employees)


def deleteEmployee(number):
    try:
        employees = []
        # Define a SQL DELETE Query
        delete_sql = "DELETE FROM employee WHERE emp_id = %s"
        # Get Cursor Object from Connection
        cursor1 = db_conn.cursor()
        # Execute the DELETE query using execute() method
        cursor1.execute(delete_sql, (number,))
        print("deleted")
        # Commit changes in db
        db_conn.commit()

    # except mysql.connector.Error as e:
    except:
        # Roll back in case there is any error
        db_conn.rollback()
        print("Error deleting data from MySQL table")
    return getEmp2()


def downloadfile(id):
    s3.download_file(
        Bucket="custombucket", Key="emp-id-" + id + "_image_file", Filename="/emp-id-" + id + "_image_file"
    )

# route to home


@app.route('/home', methods=['GET', 'POST'])
def index1():
    return getEmp()


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

    if emp_image_file.filename == "":
        return "Please select a file"

    try:

        emp_name = "" + first_name + " " + last_name
        # Uplaod image file in S3 #
        emp_image_file_name_in_s3 = "emp-id-" + str(emp_id) + "_image_file"
        s3 = boto3.resource('s3')
        insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s, %s)"
        cursor = db_conn.cursor()
        cursor.execute(insert_sql, (emp_id, first_name,
                       last_name, pri_skill, location, emp_image_file_name_in_s3))
        db_conn.commit()

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


@app.route("/portfolio")
def portfolio():
    return render_template('portfolio.html')


@app.route("/account")
def account():
    return render_template('account.html')


@app.route("/updateEmp")
def updateEmp():
    return render_template('updateEmp.html')


@app.route("/updateEmpSubmit", methods=['POST'])
def updateSubmitEmp():
    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    pri_skill = request.form['pri_skill']
    location = request.form['location']
    emp_image_file = request.files['emp_image_file']

    update_sql = "UPDATE employee SET first_name = %s, last_name = %s, pri_skill = %s, location = %s WHERE emp_id = %s"
    sql_update = "UPDATE employee SET first_name=%s, last_name=%s, pri_skill=%s, location=%s WHERE emp_id = %s % (first_name, last_name, pri_skill, location, emp_id)"

    cursor = db_conn.cursor()

    if emp_image_file.filename == "":
        return "Please select a file"

    try:

        cursor.execute(update_sql, (first_name, last_name,
                       pri_skill, location, emp_id))
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
    return getEmp()


@app.route("/deleteEmp")
def deleteEmp():
    return getEmp2()
    # return render_template('deleteEmp.html')

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=80, debug=True)


@app.route("/deleteEmp/<number>")
def delEmp(number):
    return deleteEmployee(number)
    # print("empid = " + number)
    # return render_template('deleteEmp.html', employees=employees, url=url)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
