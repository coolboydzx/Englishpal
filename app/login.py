import pickle

from flask import Blueprint, render_template, request, session, redirect, url_for, flash

from app.encryption import encryption
from app.service import verify_user, get_expiry_date, check_username_availability, add_user

login_blue = Blueprint('login',__name__)


#login,logout,signup
@login_blue.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if not session.get('logged_in'):
            return render_template('login.html')
        else:
            return render_template('logined.html')
    elif request.method == 'POST':
        # check database and verify user
        username = request.form['username']
        password = request.form['password']
        password = encryption(password)         # 加密
        verified = verify_user(username, password)
        if verified:
            session['logged_in'] = True
            session[username] = username
            session['username'] = username
            user_expiry_date = get_expiry_date(username)
            session['expiry_date'] = user_expiry_date
            session['articleID'] = None
            return redirect(url_for('user.userpage', username=username))
        else:
            return '无法通过验证。'  #密码输入错误，一样是设置成alert框弹出


@login_blue.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session['passToEasy'] = False              # 新建的session['passToEasy']先定义为false，每次进入都更新
        available = check_username_availability(username)
        if not available:
            flash('用户名 %s 已经被注册。' % (username))
            return render_template('signup.html')
        elif len(password.strip()) < 4:
            session['passToEasy'] = True
            return render_template('signup.html')  # 需要跳回到signup.html 最好是显示几秒然后结束,可以写一个js代码，到时候加个if判断，是否使用，用session来传
        else:
            password = encryption(password)         # 加密
            add_user(username, password)
            dic = {"tom": 1}
            path = 'static/frequency/frequency_' + username + '.pickle'
            fp = open(path, "wb")
            pickle.dump(dic, fp)
            fp.close()
            verified = verify_user(username, password)
            if verified:
                session['logged_in'] = True
                session[username] = username
                session['username'] = username
                session['expiry_date'] = get_expiry_date(username)
                session['articleID'] = None
                return render_template('signed.html', username=username)
            else:
                return '用户名密码验证失败。'



@login_blue.route("/logout", methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return redirect(url_for('mainpage'))