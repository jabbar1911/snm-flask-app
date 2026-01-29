import email
from flask import Flask, url_for, render_template, request,redirect,flash,session,send_file
from flask_session import Session
import flask_excel as excel
import io
from io import BytesIO
from cmail import send_mail
from otp import genotp
from stoken import endata, dndata
import mysql.connector
from mysql.connector import Error
mydb=mysql.connector.connect(user='root',host='localhost',password='1911',database='snm')
app = Flask(__name__)
excel.init_excel(app)
app.secret_key = 'snmapp123'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        server_otp = genotp()
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute("select count(*) from users where useremail=%s",[email])
            count_email=cursor.fetchone()#(1,) or (0,)
            cursor.close()
        except Exception as e:  
            print(e)
            flash('could not verify email', 'error')
            return redirect(url_for('register'))
        else:
            if count_email[0]==0:
                server_otp=genotp()
                user_data={
                    'username': username,
                    'email': email,
                    'password': password,
                    'server_otp': server_otp
                }

                #return server_otp
                # Here you would typically save the user to a database
                subject = '🔐 Verify Your Access - SNM Workspace'
                body = f'Your secure authentication code is: {server_otp}'
                send_mail(to=email, subject=subject, body=body)
                flash('OTP has been sent to your email address', 'success')
                
                return redirect(url_for('otp', var_data=endata(data=user_data)))
            elif count_email[0]==1:
                flash('Email already registered. Please use a different email.', 'warning')
               

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_email = request.form.get('email').strip()
        login_password = request.form.get('password').strip()
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute("select count(*) from users where useremail=%s",[login_email])
            count_email=cursor.fetchone()#('password123',) or None
        except Exception as e:
            print(e)
            flash('could not connect to db', 'error')
            return redirect(url_for('login'))
        else:
            if count_email[0]==1:
                cursor.execute("select userpassword from users where useremail=%s",[login_email])
                stored_password=cursor.fetchone()[0]#('password123',)
                cursor.close()
                if stored_password==login_password:
                     session['user'] = login_email   # 👈 SET SESSION
                     flash('Login successful!', 'success')
                     return redirect(url_for('dashboard'))
                else:
                    flash('Invalid password. Please try again.', 'error')
                    return redirect(url_for('login'))
            else:
                flash('user not found. Please try again.', 'error')
                return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/otp/<var_data>', methods=['GET', 'POST'])
def otp(var_data):
    if request.method == 'POST':
        user_otp = request.form['otppin']
        try:
            user_data = dndata(var_data)
        except Exception as e:
            print(e)
            flash('Invalid or expired OTP', 'error')
            return redirect(url_for('register'))
        else:
           print(f"User OTP: {user_otp}, Server OTP: {user_data['server_otp']}")
           if user_data['server_otp']==user_otp:
                cursor=mydb.cursor()
                cursor.execute("INSERT INTO users (username, useremail, userpassword) VALUES (%s, %s, %s)", (user_data['username'], user_data['email'], user_data['password']))
                mydb.commit()
                flash('user details stored', 'success')
                return redirect(url_for('login'))
           else:
                flash('Invalid OTP. Please try again.', 'error')
    return render_template('otp.html')

@app.route('/dashboard')
def dashboard():
    if session.get('user'):
        return render_template('dashboard.html')
    else:
        flash('Please login first.', 'info')
        return redirect(url_for('login'))
@app.route('/addnotes', methods=['GET', 'POST'])
def addnotes():
    if session.get('user'):
        if request.method == 'POST':
            title=request.form.get('title').strip()
            notes=request.form.get('content').strip()
            try:
                cursor=mydb.cursor(buffered=True)
                cursor.execute("select userid from users where useremail=%s",[session.get('user')])
                user_id=cursor.fetchone()[0]#(1,)
                if user_id:
                    cursor.execute("insert into notesdata(notestitle,notescontent,userid) values(%s,%s,%s)",(title,notes,user_id))
                    mydb.commit()
                    cursor.close()
                else:
                    print(user_id)
                    flash('user not verified', 'error')
                    return redirect(url_for('addnotes'))
            except Exception as e:
                print(e)
                flash('could not add notes', 'error')
                return redirect(url_for('addnotes'))
            else:
                flash('notes added successfully', 'success')
        return render_template('addnotes.html')
    else:
        flash('Please login first.', 'info')
        return redirect(url_for('login'))

@app.route('/viewallnotes')
def viewallnotes():
    if session.get('user'):
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute("select userid from users where useremail=%s",[session.get('user')])
            user_id=cursor.fetchone()[0]#(1,)
            if user_id:
                cursor.execute("select * from notesdata where userid=%s",[user_id])
                notesdata=cursor.fetchall()#[(1,'title1','content1',1),(2,'title2','content2',1)]
            else:
                flash('user could not verified', 'error')
                return redirect(url_for('dashboard'))  
        except Exception as e:
            print(e)
            flash('Could not fetch notes data', 'error')
            return redirect(url_for('dashboard'))
        else:
            return render_template('viewallnotes.html',notesdata=notesdata)
    else:
        flash('Please login first.', 'info')
        return redirect(url_for('login'))
@app.route('/viewnotes/<nid>')
def viewnotes(nid):
    if session.get('user'):
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute("select userid from users where useremail=%s",[session.get('user')])
            user_id=cursor.fetchone()
            if user_id:
                cursor.execute("select * from notesdata where userid=%s and notesid=%s",[user_id[0],nid])  
                notesdata=cursor.fetchone()#(1,'title1','content1',1)
            else:
                flash('could not verify user', 'error')
                return redirect(url_for('dashboard'))
        except Exception as e:
            print(e)
            flash('Could not fetch note data', 'error')
            return redirect(url_for('dashboard'))
        else:
            return render_template('viewnotes.html',notesdata=notesdata)
    else:
        flash('login to view notes', 'info')
        return redirect(url_for('login'))
@app.route('/deletenotes/<nid>')
def deletenotes(nid):
    if session.get('user'):
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute("select userid from users where useremail=%s",[session.get('user')])
            user_id=cursor.fetchone()
            if user_id:
                cursor.execute("delete from notesdata where userid=%s and notesid=%s",[user_id[0],nid])  
                mydb.commit()
                cursor.close()
            else:
                flash('could not verify user', 'error')
                return redirect(url_for('dashboard'))
        except Exception as e:
            print(e)
            flash('Could not delete note', 'error')
            return redirect(url_for('dashboard'))
        else:
            flash('note deleted successfully', 'success')
            return  redirect(url_for('viewallnotes'))
    else:
        flash('login to delete notes', 'info')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/updatenotes/<nid>', methods=['GET', 'POST'])
def updatenotes(nid):
    if session.get('user'):
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute("select userid from users where useremail=%s",[session.get('user')])
            user_id=cursor.fetchone()
            if user_id:
                cursor.execute("select * from notesdata where userid=%s and notesid=%s",[user_id[0],nid])  
                notesdata=cursor.fetchone()#(1,'title1','content1',1)
            else:
                flash('could not verify user', 'error')
                return redirect(url_for('dashboard'))
        except Exception as e:
            print(e)
            flash('Could not fetch note data', 'error')
            return redirect(url_for('dashboard'))
        else:
            if request.method=='POST':
                updated_title=request.form.get('title')
                updated_content=request.form.get('content')
                try:
                    cursor.execute("update notesdata set notestitle=%s,notescontent=%s where notesid=%s and userid=%s",(updated_title,updated_content,nid,user_id[0]))
                    mydb.commit()
                    cursor.close()
                except Exception as e:
                    print(e)
                    flash('could not update note', 'error')
                    return redirect(url_for('updatenotes',nid=nid))
                else:
                    flash('notes updated successfully', 'success')
                    return redirect(url_for('updatenotes',nid=nid))
            return render_template('updatenotes.html',notesdata=notesdata)
    else:
        flash('login to update notes', 'info')
        return redirect(url_for('login'))

@app.route('/getexceldata')
def excel_data():
    if session.get('user'):
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute("select userid from users where useremail=%s",[session.get('user')])
            user_id=cursor.fetchone()   
            if user_id:
                cursor.execute("select * from notesdata where userid=%s",[user_id[0]])
                notesdata=cursor.fetchall()
            else:
                flash('user could not verified', 'error')
                return redirect(url_for('dashboard'))
        except Exception as e:
            print(e)
            flash('Could not fetch notes data', 'error')
            return redirect(url_for('dashboard'))
        else:
            array_data = [list(map(str, i)) for i in notesdata]
            columns=['notesid','Title','Content','User_ID','Time']
            array_data.insert(0,columns)
            return excel.make_response_from_array(array_data,"xlsx",file_name="notesdata.xlsx")

    else:
        flash('could not verify user please login', 'info')
        return redirect(url_for('login'))

@app.route('/addfiles', methods=['GET', 'POST'])
def addfiles():
    if session.get('user'):
        if request.method == 'POST':
            file = request.files.get('file')
            if file:
                filename = file.filename
                filecontent = file.read()
                try:
                    cursor = mydb.cursor(buffered=True)
                    cursor.execute("select userid from users where useremail=%s", [session.get('user')])
                    user_id = cursor.fetchone()[0]
                    if user_id:
                        cursor.execute("insert into filesdata(filename, filecontent, userid) values(%s, %s, %s)", (filename, filecontent, user_id))
                        mydb.commit()
                        cursor.close()
                        flash('File uploaded successfully', 'success')
                        return redirect(url_for('allfiles'))
                    else:
                        flash('User not verified', 'error')
                        return redirect(url_for('addfiles'))
                except Exception as e:
                    print(e)
                    flash('Could not upload file', 'error')
                    return redirect(url_for('addfiles'))
            else:
                flash('No file selected', 'warning')
                return redirect(url_for('addfiles'))
        return render_template('uploadfile.html')
    else:
        flash('Please login first.', 'info')
        return redirect(url_for('login'))

@app.route('/allfiles')
def allfiles():
    if session.get('user'):
        try:
            cursor = mydb.cursor(buffered=True)
            cursor.execute("select userid from users where useremail=%s", [session.get('user')])
            user_id = cursor.fetchone()[0]
            if user_id:
                cursor.execute("select fileid, filename, created_at from filesdata where userid=%s", [user_id])
                filesdata = cursor.fetchall()
                cursor.close()
                return render_template('allfiles.html', filesdata=filesdata)
            else:
                flash('User not verified', 'error')
                return redirect(url_for('dashboard'))
        except Exception as e:
            print(e)
            flash('Could not fetch files', 'error')
            return redirect(url_for('dashboard'))
    else:
        flash('Please login first.', 'info')
        return redirect(url_for('login'))

@app.route('/downloadfile/<fid>')
def downloadfile(fid):
    if session.get('user'):
        try:
            cursor = mydb.cursor(buffered=True)
            cursor.execute("select userid from users where useremail=%s", [session.get('user')])
            user_id = cursor.fetchone()[0]
            if user_id:
                cursor.execute("select filename, filecontent from filesdata where fileid=%s and userid=%s", (fid, user_id))
                file_record = cursor.fetchone()
                cursor.close()
                if file_record:
                    return send_file(io.BytesIO(file_record[1]), download_name=file_record[0], as_attachment=True)
                else:
                    flash('File not found', 'warning')
                    return redirect(url_for('allfiles'))
            else:
                flash('User not verified', 'error')
                return redirect(url_for('dashboard'))
        except Exception as e:
            print(e)
            flash('Could not download file', 'error')
            return redirect(url_for('dashboard'))
    else:
        flash('Please login first.', 'info')
        return redirect(url_for('login'))

@app.route('/viewfile/<fid>')
def viewfile(fid):
    if session.get('user'):
        try:
            cursor = mydb.cursor(buffered=True)
            cursor.execute("select userid from users where useremail=%s", [session.get('user')])
            user_id = cursor.fetchone()[0]
            if user_id:
                cursor.execute("select filename, filecontent from filesdata where fileid=%s and userid=%s", (fid, user_id))
                file_record = cursor.fetchone()
                cursor.close()
                if file_record:
                    return send_file(io.BytesIO(file_record[1]), download_name=file_record[0], as_attachment=False)
                else:
                    flash('File not found', 'warning')
                    return redirect(url_for('allfiles'))
            else:
                flash('User not verified', 'error')
                return redirect(url_for('dashboard'))
        except Exception as e:
            print(e)
            flash('Could not view file', 'error')
            return redirect(url_for('dashboard'))
    else:
        flash('Please login first.', 'info')
        return redirect(url_for('login'))

@app.route('/deletefile/<fid>')
def deletefile(fid):
    if session.get('user'):
        try:
            cursor = mydb.cursor(buffered=True)
            cursor.execute("select userid from users where useremail=%s", [session.get('user')])
            user_id = cursor.fetchone()[0]
            if user_id:
                cursor.execute("delete from filesdata where fileid=%s and userid=%s", (fid, user_id))
                mydb.commit()
                cursor.close()
                flash('File deleted successfully', 'success')
                return redirect(url_for('allfiles'))
            else:
                flash('User not verified', 'error')
                return redirect(url_for('dashboard'))
        except Exception as e:
            print(e)
            flash('Could not delete file', 'error')
            return redirect(url_for('dashboard'))
    else:
        flash('Please login first.', 'info')
        return redirect(url_for('login'))

@app.route('/search')
def search():
    if session.get('user'):
        query = request.args.get('query', '').strip()
        if not query:
            return redirect(url_for('dashboard'))
        
        try:
            cursor = mydb.cursor(buffered=True)
            cursor.execute("select userid from users where useremail=%s", [session.get('user')])
            user_id = cursor.fetchone()[0]
            
            if user_id:
                # Search Notes
                cursor.execute("select * from notesdata where userid=%s and (notestitle LIKE %s or notescontent LIKE %s)", (user_id, f'%{query}%', f'%{query}%'))
                notes_results = cursor.fetchall()
                
                # Search Files
                cursor.execute("select fileid, filename, created_at from filesdata where userid=%s and filename LIKE %s", (user_id, f'%{query}%'))
                files_results = cursor.fetchall()
                
                cursor.close()
                return render_template('search_results.html', query=query, notes=notes_results, files=files_results)
            else:
                flash('User not verified', 'error')
                return redirect(url_for('dashboard'))
        except Exception as e:
            print(e)
            flash('Search failed', 'error')
            return redirect(url_for('dashboard'))
    else:
        flash('Please login first.', 'info')
        return redirect(url_for('login'))

app.run(debug=True,use_reloader=True)
