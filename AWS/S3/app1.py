import boto3
from flask import Flask, request, jsonify, render_template, json

app = Flask(__name__)

# Configure Boto3 S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id='<access_key',
    aws_secret_access_key='accesskey_password'
)
bucket_name = '<bucket_name>'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create-user', methods=['POST'])
def create_user():
    data = request.get_json()
    
    # Write data to local file
    with open('user_data.txt', 'a') as file:
        file.write(f"Name: {data['name']}, Gender: {data['gender']}, Age: {data['age']}, Membership: {data['membership']}, Contact: {data['contact']}, Email: {data['email']}\n")
    
    # Upload JSON data to S3
    s3_key = f"user_{data['name']}.json"
    s3.put_object(Bucket=bucket_name, Key=s3_key, Body=json.dumps(data))
    
    return jsonify({"message": "User created successfully!"})



@app.route('/search-user', methods=['GET'])
def search_user():
    name_to_search = request.args.get('name')
    if not name_to_search:
        return jsonify({"error": "Please provide a name to search"}), 400

    result = []
    with open('user_data.txt', 'r') as file:
        for line in file:
            if f"Name: {name_to_search}" in line:
                result.append(line.strip())

    if not result:
        return jsonify({"message": "User not found"}), 404

    return jsonify({"users": result})

@app.route('/delete-user', methods=['DELETE'])
def delete_user():
    name_to_delete = request.args.get('name')
    if not name_to_delete:
        return jsonify({"error": "Please provide a name to delete"}), 400

    with open('user_data.txt', 'r') as file:
        lines = file.readlines()

    with open('user_data.txt', 'w') as file:
        deleted = False
        for line in lines:
            if f"Name: {name_to_delete}" not in line:
                file.write(line)
            else:
                deleted = True

        if not deleted:
            return jsonify({"message": "User not found"}), 404

    return jsonify({"message": "User deleted successfully!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
