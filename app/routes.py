from app import app
from flask import render_template, request, redirect, url_for,session,send_file, send_from_directory
import time
from .utils.DB import DBB
import  os
from app.utils.MyResponse import *

app.config['SECRET_KEY'] = os.urandom(24)


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')
        confirm = DBB.c.private.user_id.find_one({'username':username})

        if confirm == None:
            data = {
                'username':None
            }
            return responseError(data,402,"用户名不存在")
        elif confirm['password'] == password:

            session['username'] = username

            return redirect(url_for('index'))
        else :
            return 'wrong password'
    elif request.method == 'GET':

        return render_template('login.html')


@app.route('/regist', methods=['GET', 'POST'])
def regist():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        nickname = request.form.get('nickname')
        gender = request.form.get('gender')
        email = request.form.get('email')
        career = request.form.get('career')



        iptdict = {
            'username': username,
            'password': password,
            'nickname': nickname,
            'gender': gender,
            'email': email,
            'career': career,
            'usercloud':'None'
        }
        confirm = DBB.c.private.user_id.find_one({'username': username})
        str(password)

        for k in iptdict:
            if iptdict[k] == '':
                return '表单填写不完全'

        if confirm != None:
            return '用户名已存在'

        if password != password2:
            return '两次密码不一致，请重新输入'

        if len(password) >5:
            if len(password)<10:
                pass
            else:
                return '密码长度过长'
        else:
            return '密码长度过短'


        DBB.c.private.user_id.insert_one(iptdict)

    return render_template('newregist.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = session.get('username')
        data = DBB.c.private.user_id.find_one({'username': username})
        onclick = request.form.get('onclick')


        if onclick == 'True':
            if username == None:
                return redirect(url_for('login'))
            elif data['usercloud'] == 'enable':
                return '已开启'
            else:

                upath = "D:/私有云/app/user-cloud/" + str(username)
                os.mkdir(upath)
                update = 'enable'
                menu={ "$set":{'usercloud':update}}
                DBB.c.private.user_id.update_one(data,menu)


    return render_template('boots.html')

@app.route('/mycloud', methods=['GET', 'POST'])
def mycloud():

    #确定文件上传格式判定

    def allow_file(filename):
        allowed_extensions = ['.jpg', '.png', '.doc', '.ppt', '.txt', '.pdf', '.jpeg', '.gif',
                              '.iso', '.docx', '.rar', '.xls', '.html', '.mp4', '.zip']
        ufilename , ext = os.path.splitext(filename)

        return ext.lower() in allowed_extensions

    if request.method == 'POST':
        username = session.get('username')
        file = request.files.get('file')
        if file == None:
            #没有数
            return '未上传文件'
        else:
            if allow_file(file.filename):
                upath = "user-cloud/" + str(username)+'/'+str(file.filename)
                save_path = 'app/'+upath
                file.save(save_path)
                fsize = os.path.getsize(save_path)
                file_info = {
                    'username': username,
                    'filename':file.filename,
                    'filepath':upath,
                    'savetime':time.asctime( time.localtime(time.time()) ),
                    'fsize':fsize
                }
                DBB.c.private.user_file.insert_one(file_info)
                return '已上传'
            else:
                return '格式不正确'
    # elif request.method == 'GET':
    #     username = session.get('username')
    #     user_folder = "app/user-cloud/" + str(username)
    #     dirs = os.listdir(user_folder)
    #
    #     data = {
    #         'file_name':dirs,
    #
    #     }

    return render_template('Pcloud.html')


@app.route('/mycloud/download', methods=['GET', 'POST'])
def download():
        if request.method == 'GET':
            username = session.get('username')
            file_info = DBB.c.private.user_file.find_one({'username':username})

            if username == file_info['username']:
                path = file_info['filepath']
                print(path)
                return responseFile(path, file_info['filename'].encode("utf-8").decode("latin-1"), file_info['fsize'])
        return '下完了'


@app.route('/test',methods = ['GET','POST'])
def test():
    if request.method == 'GET':
        userconfig =  request.args


        if userconfig.get('username') !=None:

            confirm = DBB.c.private.user_id.find_one({'username':userconfig.get('username')})
            print(confirm)
            if confirm != None:
                return json.dumps({
                    'data':False
                                })
            elif confirm == None:
                return json.dumps({
                    'data':True
                })




    return render_template('test.html')
