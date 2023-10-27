from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import attendanceModule
import read_csv
import add_faces
import os

app = Flask(__name__)

# Dữ liệu người dùng (đơn giản cho mục đích minh họa)
users = {
    'admin': {'name':'Admin', 'password': 'password123', 'role': 'admin'}        
}

existed_user = read_csv.read_csv_to_dict('static/person_info.csv')
users.update(existed_user)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    role = request.args.get('role', 'user')  # Mặc định là user nếu không có tham số role

    if role not in ['user', 'admin']:
        return 'Vai trò không hợp lệ.'

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email in users and users[email]['password'] == password and users[email]['role'] == role:
            # Trả về trang user_page với thông tin sinh viên
            name = users[email]['name']
            if role == 'user': return redirect(url_for('userPage', name = name, email = email))
            else: return redirect(url_for('adminPage', name = name, email = email))
        else:
            if role == 'user': 
                return render_template('login_user.html', login_failure=True)
            else:
                return render_template('login_admin.html', login_failure=True)

    if role == 'user':
        return render_template('login_user.html')
    elif role == 'admin':
        return render_template('login_admin.html')
    else:
        return 'Vai trò không hợp lệ.'

@app.route('/userpage', methods=['GET', 'POST'])
def userPage():
    # Tao dictionary tu 'info'
    person_name = str(request.args.get('name'))
    person_email = str(request.args.get('email'))
    return render_template('user_page.html', name = person_name, email = person_email)

@app.route('/attendance', methods=['POST'])
def attendance():
    # Gọi hàm runModule() từ module điểm danh của bạn
    if attendanceModule.runModule():
        return jsonify(success=True)
    else:
        return jsonify(success=False)
        
    

@app.route('/adminpage', methods=['POST', 'GET'])
def adminPage():
    person_name = str(request.args.get('name'))
    person_email = str(request.args.get('email'))
    if request.method == 'POST':
        name = request.form['nameUser']
        email = request.form['email']
        password = '123456'
        if add_faces.add_face(name, email, password):
            return render_template('admin_page.html', name = person_name, email = person_email)

    else:
        return render_template('admin_page.html', name = person_name, email = person_email)

@app.route('/get_directory_tree')
def get_directory_tree():
    base_path = 'static/Sorted_Attendance'
    tree = {}

    for root, dirs, files in os.walk(base_path):
        current_dir = tree
        path = os.path.relpath(root, base_path)

        if path != '.':
            for dir in path.split(os.sep):
                current_dir = current_dir.setdefault(dir, {})

        current_dir['files'] = files

    return jsonify(tree)


if __name__ == '__main__':
    app.run(debug=True)
