# import all necessary library
# flask for micro web framework
# mysql connector to connect database
# flask cors for cross-platform

import json
import mysql.connector
from flask import Flask, jsonify, request
from mysql.connector import Error
from flask_cors import CORS

# initialized application

app = Flask(__name__)
CORS(app)

# variable initialize

connection1 = None
connection2 = None
connection3 = None
cursor = None

# configure all database
# national bord of revenue e service database
connection1 = mysql.connector.connect(host='localhost', database='nbr_eservice', user='root', password='')
# ott platform database
connection2 = mysql.connector.connect(host='localhost', database='theater_ott', user='root', password='')
# payment gateway database
connection3 = mysql.connector.connect(host='localhost', database='mysql', user='root', password='')


# common string

message = "this email and mobile number already exits in database"


# prepare route
# national board of revenue e service api
@app.route("/checkDB1")
def checkNBRDatabase():
    global cursor
    try:
        if connection3.is_connected():
            db_info = connection3.get_server_info()
            print("Connected to MySQL Server version ", db_info)
            cursor = connection3.cursor()
            cursor.execute("select database();")
            record = cursor.fetchall()
            return str(record)
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection3.is_connected():
            cursor.close()
            connection3.close()
            print("MySQL connection is closed")


# insert sign up data to make nbr admin profile
@app.route("/sighUpAdmin", methods=["POST"])
def signUpAdmin():
    global cursor
    cursor = connection1.cursor()

    firstName = request.json['first_name']
    middleName = request.json['middle_name']
    lastName = request.json['last_name']
    emailAddress = request.json['email_address']
    mobileNumber = request.json['mobile_number']
    userPassword = request.json['user_password']
    userPosition = request.json['user_position']

    try:
        if connection1.is_connected():
            query = "SELECT email_address, mobile_number FROM nbr_admin WHERE email_address = %s AND mobile_number = %s"
            cursor.execute(query, (emailAddress, mobileNumber,))
            record = cursor.fetchall()
            print("data", cursor.rowcount, record)

            if cursor.rowcount == 0:
                insertQuery = "INSERT INTO nbr_admin(first_name, middle_name, last_name,email_address,mobile_number, " \
                              "user_password, user_position) VALUES(%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(insertQuery, (firstName, middleName, lastName, emailAddress, mobileNumber,
                                             userPassword, userPosition))
                response = cursor.lastrowid
                return jsonify({'message': response})

            else:
                return jsonify({'message': message})

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection1.is_connected():
            cursor.close()
            connection2.close()
            print("MySQL connection is closed")


# ott platform service api
@app.route("/checkDB2", methods=["GET"])
def checkOTTDatabase():
    global cursor
    try:
        if connection1.is_connected():
            db_info = connection1.get_server_info()
            print("Connected to MySQL Server version ", db_info)
            cursor = connection1.cursor()
            cursor.execute("SELECT * FROM nbr_admin")
            record = cursor.fetchall()
            return str(record)
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection1.is_connected():
            cursor.close()
            connection2.close()
            print("MySQL connection is closed")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
