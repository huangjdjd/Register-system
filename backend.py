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
    team_array=[]
    rank_array=[]
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
        # print(competition_array)

    cur.execute("SELECT rank FROM user")
    ranks=cur.fetchall()
    for rank in ranks:
        rank_array.append(rank[0])

    cur.execute("SELECT team FROM user")
    teams=cur.fetchall()
    for team in teams:
        team_array.append(team[0])
    return js.dumps({'names': name_array, 'checks': check_array,'competition':competition_array,'team':team_array,'rank':rank_array})
@app.route('/admin_aicup_number',methods=['post'])
def adminCheck():
    name_array=[]
    name=request.get_json()
    namecheck=name['checkstatus']
    nameid=name['checkid']
    con=sql.connect('user.db')
    cur=con.cursor()
    cur.execute("SELECT name FROM user")
    names=cur.fetchall()
    judgei=0
    for name in names:
        if(nameid==judgei and namecheck==1):
            cur.execute("UPDATE user set check_in=? where name=?", (1, name[0]))
            con.commit()
            con.close()
        elif(nameid==judgei and namecheck==0):
            cur.execute("UPDATE user set check_in=? where name=?", (0, name[0]))
            con.commit()
            con.close()
        judgei+=1
    # print(nameid)
    # print(namecheck)
    return js.dumps({'checkstatus':True})
    
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5050)
