from flask import Flask, request, render_template, redirect, url_for,session
import sqlite3 as sql
import json as js
app = Flask(__name__)
app.secret_key = "b22VD7bKVsEa"
@app.route("/")
def main_page():
    return render_template('main.html')

@app.route('/<msg>')
def mainf(msg):
    if msg == "輸入錯誤":
        return render_template('main.html', msg=msg)
    else:
        return render_template('main.html')
@app.route('/success/<msg>')
def show_seat(msg):
    return render_template('show.html',msg=msg)

@app.route('/sign_action', methods=['POST', 'GET'])
def sign_action():
    con=sql.connect('user.db')
    cur=con.cursor()
    if request.method == 'POST':
        name = request.form['Name']
    if name:
        cur.execute("SELECT name FROM user WHERE name = ?", (name,))
        check_name=cur.fetchone()
        print(check_name)
        if check_name:
            cur.execute("UPDATE user set check_in=? where name=?",(1,name))
            session['logged_in'] = True
            con.commit()
            return redirect(url_for('show_seat',msg=check_name[0]))
        else:
            return redirect(url_for('mainf',msg="輸入錯誤"))
    else:
        return redirect(url_for('mainf',msg="輸入錯誤"))
    # ss=js.dumps(smsg)
    

if __name__ == '__main__':
    app.run(debug=True)
