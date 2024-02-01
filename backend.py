from flask import Flask, request, render_template, redirect, url_for,session
import sqlite3 as sql
import json as js
app = Flask(__name__)
app.secret_key = "b22VD7bKVsEa"
@app.route("/")
def main_page():
    return render_template('main.html')

@app.route('/login')
def show_seat():
    return render_template('show.html')
@app.route('/admin_aicup')
def show_admin():
    return render_template('admin.html')
@app.route('/sign_action', methods=['POST'])
def sign_action():
    con = sql.connect('user.db')
    cur = con.cursor()
    data = request.get_json()
    name = data['name']
    
    if name:
        cur.execute("SELECT name FROM user WHERE name = ?", (name,))
        check_name = cur.fetchone()
        
        if check_name:
            cur.execute("UPDATE user set check_in=? where name=?", (1, name))
            con.commit()
            con.close()
            session['user_name']=name
            return js.dumps({"success": True})
        else:
            con.close()
            return js.dumps({"success": False, "message": "輸入錯誤"})
    else:
        return js.dumps({"success": False, "message": "無效輸入"})
@app.route('/show_seat', methods=['post'])
def handle_seat():
    con = sql.connect('user.db')
    cur = con.cursor()
    name=session['user_name']
    cur.execute("SELECT seat FROM user WHERE name = ?", (name,))
    seat=cur.fetchone()
    cur.execute("SELECT competition FROM user WHERE name=?",(name,))
    competition=cur.fetchone()[0]
    print(seat[0])
    return js.dumps({'seat':seat[0],'name':name,'competition':competition})
    # ss=js.dumps(smsg)
@app.route('/admin_aicup_handle',methods=['post'])
def admin():
    name_array=[]
    check_array=[]
    competition_array=[]
    con = sql.connect('user.db')
    cur = con.cursor()
    cur.execute("SELECT name FROM user")
    names=cur.fetchall()
    for name in names:
        name_array.append(name[0])
    cur.execute("SELECT check_in FROM user")
    checks=cur.fetchall()
    for check in checks:
        check_array.append(check[0])
    cur.execute("SELECT competition FROM user")
    competitions=cur.fetchall()
    for competition in competitions:
        competition_array.append(competition)
    return js.dumps({'names': name_array, 'checks': check_array,'competition':competition_array})

if __name__ == '__main__':
    app.run(debug=True)
