import os           
import email
from flask import Flask, url_for, render_template, request,redirect,flash,session,send_file
from flask_session import Session
import flask_excel as excel
import io
from io import BytesIO
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

# Supabase Configuration
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

if not url or not key:
    print("❌ ERROR: SUPABASE_URL or SUPABASE_KEY is missing!")
    print("Please set these in your Render Dashboard > Environment Variables.")
    # Initialize with dummy values to prevent total crash during import, 
    # but actual routes will fail if used.
    supabase: Client = None
else:
    supabase: Client = create_client(url, key)

app = Flask(__name__)
excel.init_excel(app)
app.secret_key = os.environ.get('SECRET_KEY', 'snmapp123')
# 16MB File Upload Limit
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        try:
            # Supabase Auth Sign Up
            res = supabase.auth.sign_up({
                "email": email, 
                "password": password,
                "options": {
                    "data": {"username": username}
                }
            })
            if res.user:
                # Also create a profile in our public.profiles table
                supabase.table('profiles').insert({"id": res.user.id, "username": username}).execute()
                # Store email in session to use in OTP verification
                session['reg_email'] = email
                session['reg_username'] = username
                flash('Registration details submitted! Please check your email for a 6-digit confirmation code.', 'success')
                return redirect(url_for('otp'))
        except Exception as e:
            print(f"Registration error: {e}")
            flash('Registration failed. Email might already be in use.', 'error')
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/otp', methods=['GET', 'POST'])
def otp():
    if request.method == 'POST':
        otp_code = request.form.get('otppin')
        email = session.get('reg_email')
        
        if not email:
            flash('Session expired. Please register again.', 'error')
            return redirect(url_for('register'))
            
        try:
            # Supabase OTP Verification
            res = supabase.auth.verify_otp({
                "email": email,
                "token": otp_code,
                "type": "signup"
            })
            
            if res.user:
                session.pop('reg_email', None)
                session.pop('reg_username', None)
                flash('Email verified! You can now login.', 'success')
                return redirect(url_for('login'))
        except Exception as e:
            print(f"OTP Verification error: {e}")
            flash('Invalid OTP code. Please try again.', 'error')
            return redirect(url_for('otp'))
            
    return render_template('otp.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_email = request.form.get('email').strip()
        login_password = request.form.get('password').strip()
        try:
            # Supabase Auth Sign In
            res = supabase.auth.sign_in_with_password({
                "email": login_email, 
                "password": login_password
            })
            if res.user:
                session['user'] = res.user.email
                session['user_id'] = res.user.id
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
        except Exception as e:
            print(f"Login error: {e}")
            flash('Invalid email or password. Please try again.', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

# If you want to use OTP verify, Supabase supports it, and we've implemented it above.

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
            title = request.form.get('title').strip()
            notes = request.form.get('content').strip()
            user_id = session.get('user_id')
            try:
                # Supabase Insert Note
                supabase.table('notesdata').insert({
                    "notestitle": title, 
                    "notescontent": notes, 
                    "userid": user_id
                }).execute()
                flash('notes added successfully', 'success')
            except Exception as e:
                print(f"Add notes error: {e}")
                flash('could not add notes', 'error')
                return redirect(url_for('addnotes'))
        return render_template('addnotes.html')
    else:
        flash('Please login first.', 'info')
        return redirect(url_for('login'))

@app.route('/viewallnotes')
def viewallnotes():
    if session.get('user'):
        user_id = session.get('user_id')
        try:
            # Supabase Select All Notes for User
            response = supabase.table('notesdata').select('*').eq('userid', user_id).order('created_at', desc=True).execute()
            # notesdata format from response.data is list of dicts
            # Need to convert to list of tuples to match old template expectations (nid, title, content, uid, time)
            notesdata = []
            for row in response.data:
                notesdata.append((row['notesid'], row['notestitle'], row['notescontent'], row['userid'], row['created_at']))
        except Exception as e:
            print(f"Fetch all notes error: {e}")
            flash('Could not fetch notes data', 'error')
            return redirect(url_for('dashboard'))
        else:
            return render_template('viewallnotes.html', notesdata=notesdata)
    else:
        flash('Please login first.', 'info')
        return redirect(url_for('login'))

@app.route('/viewnotes/<nid>')
def viewnotes(nid):
    if session.get('user'):
        user_id = session.get('user_id')
        try:
            # Supabase Select Single Note
            response = supabase.table('notesdata').select('*').eq('notesid', nid).eq('userid', user_id).execute()
            if response.data:
                row = response.data[0]
                notesdata = (row['notesid'], row['notestitle'], row['notescontent'], row['userid'], row['created_at'])
            else:
                flash('Note not found', 'error')
                return redirect(url_for('dashboard'))
        except Exception as e:
            print(f"View note error: {e}")
            flash('Could not fetch note data', 'error')
            return redirect(url_for('dashboard'))
        else:
            return render_template('viewnotes.html', notesdata=notesdata)
    else:
        flash('login to view notes', 'info')
        return redirect(url_for('login'))

@app.route('/deletenotes/<nid>')
def deletenotes(nid):
    if session.get('user'):
        user_id = session.get('user_id')
        try:
            # Supabase Delete Note
            supabase.table('notesdata').delete().eq('notesid', nid).eq('userid', user_id).execute()
        except Exception as e:
            print(f"Delete note error: {e}")
            flash('Could not delete note', 'error')
            return redirect(url_for('dashboard'))
        else:
            flash('note deleted successfully', 'success')
            return redirect(url_for('viewallnotes'))
    else:
        flash('login to delete notes', 'info')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    supabase.auth.sign_out()
    session.pop('user', None)
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/updatenotes/<nid>', methods=['GET', 'POST'])
def updatenotes(nid):
    if session.get('user'):
        user_id = session.get('user_id')
        try:
            # Fetch existing note
            response = supabase.table('notesdata').select('*').eq('notesid', nid).eq('userid', user_id).execute()
            if response.data:
                row = response.data[0]
                notesdata = (row['notesid'], row['notestitle'], row['notescontent'], row['userid'], row['created_at'])
            else:
                flash('Note not found', 'error')
                return redirect(url_for('dashboard'))
        except Exception as e:
            print(f"Fetch note for update error: {e}")
            flash('Could not fetch note data', 'error')
            return redirect(url_for('dashboard'))
        else:
            if request.method == 'POST':
                updated_title = request.form.get('title')
                updated_content = request.form.get('content')
                try:
                    # Supabase Update Note
                    supabase.table('notesdata').update({
                        "notestitle": updated_title, 
                        "notescontent": updated_content
                    }).eq('notesid', nid).eq('userid', user_id).execute()
                except Exception as e:
                    print(f"Update note error: {e}")
                    flash('could not update note', 'error')
                    return redirect(url_for('updatenotes', nid=nid))
                else:
                    flash('notes updated successfully', 'success')
                    return redirect(url_for('updatenotes', nid=nid))
            return render_template('updatenotes.html', notesdata=notesdata)
    else:
        flash('login to update notes', 'info')
        return redirect(url_for('login'))

@app.route('/getexceldata')
def excel_data():
    if session.get('user'):
        user_id = session.get('user_id')
        try:
            # Supabase Select All Notes
            response = supabase.table('notesdata').select('*').eq('userid', user_id).execute()
            # Convert dicts to list of tuples for Excel
            notesdata = []
            for row in response.data:
                notesdata.append((row['notesid'], row['notestitle'], row['notescontent'], row['userid'], row['created_at']))
        except Exception as e:
            print(f"Excel data fetch error: {e}")
            flash('Could not fetch notes data', 'error')
            return redirect(url_for('dashboard'))
        else:
            array_data = [list(map(str, i)) for i in notesdata]
            columns = ['notesid', 'Title', 'Content', 'User_ID', 'Time']
            array_data.insert(0, columns)
            return excel.make_response_from_array(array_data, "xlsx", file_name="notesdata.xlsx")
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
                file_content = file.read()
                user_id = session.get('user_id')
                # 16MB limit already enforced by Flask app.config
                storage_path = f"{user_id}/{filename}"
                try:
                    # Supabase Upload to 'files' bucket
                    # Note: You MUST create a public bucket named 'files' in Supabase Storage first
                    supabase.storage.from_('files').upload(
                        path=storage_path, 
                        file=file_content,
                        file_options={"content-type": file.content_type}
                    )
                    
                    # Store link in filesdata table
                    supabase.table('filesdata').insert({
                        "filename": filename, 
                        "storage_path": storage_path, 
                        "userid": user_id
                    }).execute()
                    
                    flash('File uploaded successfully', 'success')
                    return redirect(url_for('allfiles'))
                except Exception as e:
                    print(f"File upload error: {e}")
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
        user_id = session.get('user_id')
        try:
            # Supabase Select All Files
            response = supabase.table('filesdata').select('fileid, filename, created_at').eq('userid', user_id).execute()
            filesdata = [(row['fileid'], row['filename'], row['created_at']) for row in response.data]
            return render_template('allfiles.html', filesdata=filesdata)
        except Exception as e:
            print(f"Fetch all files error: {e}")
            flash('Could not fetch files', 'error')
            return redirect(url_for('dashboard'))
    else:
        flash('Please login first.', 'info')
        return redirect(url_for('login'))

@app.route('/downloadfile/<fid>')
def downloadfile(fid):
    if session.get('user'):
        user_id = session.get('user_id')
        try:
            # Get storage path from DB
            response = supabase.table('filesdata').select('filename, storage_path').eq('fileid', fid).eq('userid', user_id).execute()
            if response.data:
                file_record = response.data[0]
                # Download from Supabase Storage
                storage_data = supabase.storage.from_('files').download(file_record['storage_path'])
                return send_file(io.BytesIO(storage_data), download_name=file_record['filename'], as_attachment=True)
            else:
                flash('File not found', 'warning')
                return redirect(url_for('allfiles'))
        except Exception as e:
            print(f"Download file error: {e}")
            flash('Could not download file', 'error')
            return redirect(url_for('dashboard'))
    else:
        flash('Please login first.', 'info')
        return redirect(url_for('login'))

@app.route('/viewfile/<fid>')
def viewfile(fid):
    if session.get('user'):
        user_id = session.get('user_id')
        try:
            # Get storage path from DB
            response = supabase.table('filesdata').select('filename, storage_path').eq('fileid', fid).eq('userid', user_id).execute()
            if response.data:
                file_record = response.data[0]
                # Download (to view) from Supabase Storage
                storage_data = supabase.storage.from_('files').download(file_record['storage_path'])
                return send_file(io.BytesIO(storage_data), download_name=file_record['filename'], as_attachment=False)
            else:
                flash('File not found', 'warning')
                return redirect(url_for('allfiles'))
        except Exception as e:
            print(f"View file error: {e}")
            flash('Could not view file', 'error')
            return redirect(url_for('dashboard'))
    else:
        flash('Please login first.', 'info')
        return redirect(url_for('login'))

@app.route('/deletefile/<fid>')
def deletefile(fid):
    if session.get('user'):
        user_id = session.get('user_id')
        try:
            # Get storage path first
            response = supabase.table('filesdata').select('storage_path').eq('fileid', fid).eq('userid', user_id).execute()
            if response.data:
                storage_path = response.data[0]['storage_path']
                # Delete from Storage
                supabase.storage.from_('files').remove([storage_path])
                # Delete from DB
                supabase.table('filesdata').delete().eq('fileid', fid).eq('userid', user_id).execute()
                flash('File deleted successfully', 'success')
                return redirect(url_for('allfiles'))
            else:
                flash('File not found', 'warning')
                return redirect(url_for('allfiles'))
        except Exception as e:
            print(f"Delete file error: {e}")
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
        
        user_id = session.get('user_id')
        try:
            # Search Notes (using ilike for case-insensitive search if supported, otherwise like)
            notes_res = supabase.table('notesdata').select('*').eq('userid', user_id).or_(f"notestitle.ilike.%{query}%,notescontent.ilike.%{query}%").execute()
            notes_results = [(row['notesid'], row['notestitle'], row['notescontent'], row['userid'], row['created_at']) for row in notes_res.data]
            
            # Search Files
            files_res = supabase.table('filesdata').select('fileid, filename, created_at').eq('userid', user_id).ilike('filename', f'%{query}%').execute()
            files_results = [(row['fileid'], row['filename'], row['created_at']) for row in files_res.data]
            
            return render_template('search_results.html', query=query, notes=notes_results, files=files_results)
        except Exception as e:
            print(f"Search error: {e}")
            flash('Search failed', 'error')
            return redirect(url_for('dashboard'))
    else:
        flash('Please login first.', 'info')
        return redirect(url_for('login'))

@app.route('/delete_account', methods=['POST'])
def delete_account():
    if session.get('user'):
        user_id = session.get('user_id')
        try:
            # 1. Delete all user files from Storage
            # (In a real app, you'd list all files first or use a recursive delete)
            # For simplicity, we assume RLS handles visibility but cleanup is good.
            files_res = supabase.table('filesdata').select('storage_path').eq('userid', user_id).execute()
            paths = [row['storage_path'] for row in files_res.data]
            if paths:
                supabase.storage.from_('files').remove(paths)
            
            # 2. Supabase Auth Admin can delete user, but simple client can't easily.
            # Usually, you'd call an edge function. For now, we delete DB data.
            # If CASCADE is set in SQL, deleting Auth user handles DB.
            # Since we can't delete Auth user from client easily without admin key,
            # we just delete our table data and log out.
            supabase.table('notesdata').delete().eq('userid', user_id).execute()
            supabase.table('filesdata').delete().eq('userid', user_id).execute()
            supabase.table('profiles').delete().eq('id', user_id).execute()
            
            # NOTE: To fully delete Auth user, you'd use supabase.auth.admin.delete_user(user_id)
            # which requires the SERVICE_ROLE_KEY.
            
            session.clear()
            flash('Your account data has been permanently deleted. (Auth account requires admin cleanup)', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            print(f"Delete account error: {e}")
            flash('An error occurred while deleting your account.', 'error')
            return redirect(url_for('dashboard'))
    else:
        flash('Please login first.', 'info')
        return redirect(url_for('login'))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
