import pickle
from datetime import datetime
from flask import Blueprint, session, request,render_template,redirect,url_for
from app import pickle_idea, pickle_idea2
from app.WordFreq import WordFreq
from app.service import get_flashed_messages_if_any, appears_in_test, get_today_article, load_freq_history, get_time
from app.wordfreqCMD import youdao_link, sort_in_descending_order

user_blue = Blueprint('user',__name__)

path_prefix = 'D:/pycharm/englishpal/app/'
path_prefix = './'  # comment this line in deployment

#用户界面 userpage



@user_blue.route("/<username>/reset", methods=['GET', 'POST'])
def user_reset(username):
    if request.method == 'GET':
        session['articleID'] = None
        return redirect(url_for('user.userpage',username=username))
    else:
        return 'Under construction'

@user_blue.route("/<username>", methods=['GET', 'POST'])
def userpage(username):

    if not session.get('logged_in'):
        return render_template('returnlogin.html')
        # 经过几秒之后跳转到登录界面

    username = session.get('username')

    user_expiry_date = session.get('expiry_date')
    if datetime.now().strftime('%Y%m%d') > user_expiry_date:
        return render_template('expiry.html',username)  #需要添加一个支付宝二维码在static里面， 叫donate-the-author-hidden.jpg
        # 跳转到expiry页面

    user_freq_record = path_prefix + 'static/frequency/' + 'frequency_%s.pickle' % (username)
    if request.method == 'POST':  # when we submit a form
        content = request.form['content']  # 跳转到userpagepost界面
        f = WordFreq(content)
        lst = f.get_freq()
        #需要传入的数，将其放在一个词典中,这个是可以改进的地方
        #username，count，link
        return render_template('userpagepost.html',username=username,lst=lst)

    elif request.method == 'GET':  # when we load a html page
        flashed_messages=get_flashed_messages_if_any()
        today_article=get_today_article(user_freq_record, session['articleID'])
        d = load_freq_history(user_freq_record)
        d_len = len(d)
        if len(d) > 0:
            lst = pickle_idea2.dict2lst(d)
            lst2 = []
            for t in lst:
                lst2.append((t[0], len(t[1])))
            lst3 = sort_in_descending_order(lst2)
            for x in lst3:
                word = x[0]
                freq = x[1]
                if session.get('thisWord') == x[0] and session.get('time') == 1:
                    # page += '<a name="aaa"></a>'  # 3. anchor
                    session['time'] = 0  # discard anchor
                isInstance = isinstance(d[word], list)
        return render_template('userpageget.html', username=username, flashed_messages=flashed_messages, today_article=today_article, d_len=d_len, lst3=lst3, isInstance=isInstance)


@user_blue.route("/<username>/mark", methods=['GET', 'POST'])
def user_mark_word(username):
    username = session[username]
    user_freq_record = path_prefix + 'static/frequency/' + 'frequency_%s.pickle' % (username)
    if request.method == 'POST':
        d = load_freq_history(user_freq_record)
        lst_history = pickle_idea2.dict2lst(d)
        lst = []
        for word in request.form.getlist('marked'):
            lst.append((word, [get_time()]))
        d = pickle_idea2.merge_frequency(lst, lst_history)
        pickle_idea2.save_frequency_to_pickle(d, user_freq_record)
        return redirect(url_for('user.userpage', username=username))
    else:
        return 'Under construction'

