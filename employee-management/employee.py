from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

employee = Flask(__name__)


employee.config['MYSQL_HOST'] = 'localhost'
employee.config['MYSQL_USER'] = 'root'  
employee.config['MYSQL_PASSWORD'] = ''  
employee.config['MYSQL_DB'] = 'employee_db'

mysql = MySQL(employee)

@employee.route('/employees', methods=['GET'])
def get_employees():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM employees")
    employees = cur.fetchall()
    cur.close()
    
    emp_list = []
    for emp in employees:
        emp_list.append({
            "id": emp[0],
            "full_name": emp[1],
            "date_of_birth": emp[2],
            "address": emp[3],
            "contact_no": emp[4],
            "emergency_contact_no": emp[5]
        })
    
    return jsonify(emp_list)

@employee.route('/employees/<int:id>', methods=['GET'])
def get_employee(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM employees WHERE id = %s", (id,))
    emp = cur.fetchone()
    cur.close()

    if emp:
        return jsonify({
            "id": emp[0],
            "full_name": emp[1],
            "date_of_birth": emp[2],
            "address": emp[3],
            "contact_no": emp[4],
            "emergency_contact_no": emp[5]
        })
    return jsonify({"message": "Employee not found"}), 404

@employee.route('/employees', methods=['POST'])
def add_employee():
    data = request.json
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO employees (full_name, date_of_birth, address, contact_no, emergency_contact_no) 
        VALUES (%s, %s, %s, %s, %s)
    """, (data['full_name'], data['date_of_birth'], data['address'], data['contact_no'], data['emergency_contact_no']))
    
    mysql.connection.commit()
    cur.close()
    return jsonify({"message": "Employee added successfully!"}), 201

@employee.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    data = request.json
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE employees SET full_name=%s, date_of_birth=%s, address=%s, contact_no=%s, emergency_contact_no=%s 
        WHERE id=%s
    """, (data['full_name'], data['date_of_birth'], data['address'], data['contact_no'], data['emergency_contact_no'], id))
    
    mysql.connection.commit()
    cur.close()
    return jsonify({"message": "Employee updated successfully!"})

@employee.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM employees WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({"message": "Employee deleted successfully!"})

if __name__ == '__main__':
    employee.run(debug=True)
