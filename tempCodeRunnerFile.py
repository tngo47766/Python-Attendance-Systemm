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
            student_info = {
                'name' : name,
                'email' : email
            }
            return redirect(url_for('userPage', info = student_info))
        else:
            return "Thong tin dang nhap sai"

    if role == 'user':
        return render_template('login_user.html')
    elif role == 'admin':
        return render_template('login_admin.html')
    else:
        return 'Vai trò không hợp lệ.'