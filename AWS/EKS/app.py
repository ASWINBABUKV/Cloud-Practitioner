from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    with open('employees.txt', 'a') as f:
        f.write(f"{request.form['name']}, {request.form['age']}, {request.form['gender']}, {request.form['email']}, {request.form['phone']}, {request.form['occupation']}, {request.form['location']}\n")
    return "Employee Registered Successfully!"

@app.route('/search', methods=['POST'])
def search():
    search_name = request.form['search_name']
    with open('employees.txt', 'r') as f:
        for line in f:
            if search_name in line:
                return line
    return "Employee not found."

@app.route('/delete', methods=['POST'])
def delete():
    delete_name = request.form['delete_name']
    with open('employees.txt', 'r') as f:
        lines = f.readlines()
    with open('employees.txt', 'w') as f:
        for line in lines:
            if delete_name not in line:
                f.write(line)
    return "Employee Deleted Successfully!"



@app.route('/display', methods=['GET'])
def display():
    with open('employees.txt', 'r') as f:
        return "<br>".join(f.readlines())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


