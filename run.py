import csv
import datetime
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
    existed_user = read_csv.read_csv_to_dict('static/person_info.csv')
    users.update(existed_user)
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
@app.route('/getMarkedDates', methods=['GET', 'POST'])
def get_marked_dates():
    username = request.args.get('username')  # Lấy tên người dùng từ tham số trong URL
    print(username)
    marked_dates = []  # Danh sách ngày đã điểm danh

    csv_folder = 'static/Sorted_Attendance/'
    now = datetime.datetime.now()
    year_folder = os.path.join(csv_folder, str(now.year))
    month_folder = os.path.join(year_folder, now.strftime('%B'))

    if os.path.exists(month_folder):
        # Đọc các tệp CSV trong thư mục tháng của năm hiện tại
        for csv_file in os.listdir(month_folder):
            # print(csv_file)
            date_str = csv_file.split('_')[-1].split('.')[0].split('-')[0]  # Trích xuất phần ngày từ tên tệp
            csv_file_path = os.path.join(month_folder, csv_file)
            with open(csv_file_path, 'r') as attendance_in_date:
                csv_reader = csv.DictReader(attendance_in_date)
                i = 0
                for row in csv_reader:
                    if row['NAME'] == username:
                        marked_dates.append(int(date_str))
        # print(marked_dates)        
    return jsonify(success = True, markedDates=marked_dates) 


if __name__ == '__main__':
    app.run(debug=True)
