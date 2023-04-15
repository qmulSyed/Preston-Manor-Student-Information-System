from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from datetime import timedelta
from datetime import datetime
from databases import LoginDatabase, TicketDatabase, QuestionDatabase, ECDB
from flask import jsonify
import os

app = Flask(__name__, static_folder='web', static_url_path='')

app.permanent_session_lifetime = timedelta(days=3)

app.secret_key = "sado72e3ymatyds9782g"

app.config["UPLOAD_FOLDER"] = "uploads"

if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])

@app.route('/api/tickets', methods=['GET'])
def api_tickets():
     db = TicketDatabase()
     tickets = db.get_all_tickets()
     return jsonify(tickets)

@app.route('/api/userTickets', methods=['GET'])
def api_user_tickets():
     db = TicketDatabase()
     user = session['username']
     tickets = db.get_user_tickets(user)
     return jsonify(tickets)

@app.route('/')
def index():
    if "username" not in session:
        return app.send_static_file("home/index.html")
    else:
        return redirect("/home")

@app.route('/home')
def home():
    if "username" not in session:
        return redirect(url_for("index"))
    return app.send_static_file("dashboard/index.html")

@app.route('/knowledgeBase')
def knowledgeBase():
    if "username" not in session:
        return redirect(url_for("index"))
    return app.send_static_file("dashboard/knowledgeBase/knowledgeBase.html")

@app.route('/knowledgeBaseAdmin')
def knowledgeBaseAdmin():
    if "username" not in session:
        return redirect(url_for("index"))
    return app.send_static_file("admin/KB/knowledgeBase.html")

@app.route('/knowledgeBaseAdd')
def knowledgeBaseAdd():
    if "username" not in session:
        return redirect(url_for("index"))
    return app.send_static_file("dashboard/knowledgeBase/knowledgeBaseAdd.html")

@app.route('/knowledgeBaseDuplicate')
def knowledgeBaseDuplicate():
    if "username" not in session:
        return redirect(url_for("index"))
    return app.send_static_file("dashboard/knowledgeBase/knowledgeBaseDuplicate.html")

@app.route('/knowledgeBaseEdit')
def knowledgeBaseEdit():
    if "username" not in session:
        return redirect(url_for("index"))
    return app.send_static_file("dashboard/knowledgeBase/knowledgeBaseEdit.html")

@app.route('/Report')
def report():
    if "username" not in session:
        return redirect(url_for("index"))
    return app.send_static_file("dashboard/report.html")

@app.route('/ECs')
def ECs():
    if "username" not in session:
        return redirect(url_for("index"))
    return app.send_static_file("dashboard/ECs/ECs.html")

@app.route('/tickets')
def tickets():
    if "username" not in session:
        return redirect(url_for("index"))
    return app.send_static_file("dashboard/ticket/ticket.html")

@app.route('/login', methods=['POST'])
def login():
    try:
        data = data = request.form
        username = data['username']
        password = data['password']
    except:
        return {"error": "login requires all fields"}, 403
    
    DB = LoginDatabase()
    userType = DB.isInDatabase(username, password).get("userType", "NotFound")
    if userType == "NotFound":
        return redirect(url_for("index"))
    elif userType == "student":
        session['username'] = username
        session.permanent = True
        return redirect(url_for("home"))
    else:
        session['usernameAdmin'] = username
        session.permanent = True
        return redirect("admin/home")

@app.route("/logout", methods=["POST", "GET"])
def logout():
    session.clear()

    return redirect(url_for("index"))

    
@app.route('/issues', methods=['GET', 'POST'])
def issues():
    #if "username" not in session:
        #return redirect(url_for("index"))
    db = TicketDatabase()
    if request.method == 'GET':
        search = request.args.get('search', '')
        if search:
            tickets = db.search_tickets(search)
        else:
            tickets = db.get_all_tickets()

        return jsonify(tickets), 201

    if request.method == 'POST':
        title = request.json.get('title')
        content = request.json.get('content')
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')        
        user = session['username']

        db.add_ticket(title, content, date, user)
        return {'success': True}

@app.route("/replies", methods=["POST", "GET"])
def add_reply():
    #if "username" not in session:
        #return redirect(url_for("index"))
    db = TicketDatabase()
    
    if request.method == "POST":
    
        data = request.get_json()
        issue_id = data.get('issue_id')
        content = data.get('content')
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')    
        username = session['username']
        
        db.add_reply(content, date, username, issue_id)
        return {'success': True}
    else:
        issue_id = request.args.get('issue_id')
        replies = db.get_replies(issue_id)
        reply_data = []
        for reply in replies:
            reply_data.append({
                'id': reply[0],
                'content': reply[1],
                'date': reply[2],
                'username': reply[3],
                'issue_id': reply[4]
            })
            
        return jsonify(reply_data)
    
@app.route("/repliesAdmin", methods=["POST", "GET"])
def add_repliesAdmin():
    #if "username" not in session:
        #return redirect(url_for("index"))
    db = TicketDatabase()
    
    if request.method == "POST":
    
        data = request.get_json()
        issue_id = data.get('issue_id')
        content = data.get('content')
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')    
        username = session['usernameAdmin']
        
        db.add_reply(content, date, username, issue_id)
        return {'success': True}
    else:
        issue_id = request.args.get('issue_id')
        replies = db.get_replies(issue_id)
        reply_data = []
        for reply in replies:
            reply_data.append({
                'id': reply[0],
                'content': reply[1],
                'date': reply[2],
                'username': reply[3],
                'issue_id': reply[4]
            })
            
        return jsonify(reply_data)
    
@app.route('/questions', methods=['GET', 'POST'])
def questions():
    #if "usernameAdmin" not in session:
        #return redirect(url_for("index"))
    db = QuestionDatabase()
    if request.method == 'GET':
        search = request.args.get('search', '')
        if search:
            questions = db.search_questions(search)
        else:
            questions = db.get_all_questions()

        return jsonify(questions), 201

    if request.method == 'POST':
        title = request.json.get('title')
        content = request.json.get('content')

        db.add_question(title, content)
        return {'success': True}
    
@app.route('/addQuestion', methods=['POST'])
def addQuestion():
    if "usernameAdmin" not in session:
        return redirect(url_for("index"))
    data = data = request.form
    title = data['question']
    content = data['answer']
    db = QuestionDatabase()
    db.add_question(title, content)
    return redirect("/admin/knowledgebase")

@app.route('/countStudents', methods=['GET'])
def countStudents():
    if "usernameAdmin" not in session:
        return redirect(url_for("index"))
    db = LoginDatabase()
    x = jsonify(db.count()), 201
    # print(x)
    return x

@app.route('/countAdmin', methods=['GET'])
def countAdmin():
    if "usernameAdmin" not in session:
        return redirect(url_for("index"))
    db = LoginDatabase()
    x = jsonify(db.countAdmin()), 201
    print(x)
    return x

@app.route('/deleteQuestion/<id>/', methods=['POST'])
def deleteQuestion(id):
    if "usernameAdmin" not in session:
        return redirect(url_for("index"))
    title  = {id}
    #content  = {answer}
    db = QuestionDatabase()
    db.delete_question(id)
    return {'success': True}

@app.route('/deleteTicket/<title>/', methods=['POST'])
def deleteTicket(title):
    if "usernameAdmin" not in session:
        #[]
        return redirect(url_for("index"))
    title  = {title}
    db = TicketDatabase()
    db.delete_ticket(title)
    return {'success': True}

@app.route("/admin/<page>", methods=["GET"])
def adminPages(page):
    if "usernameAdmin" not in session:
        return redirect(url_for("index"))

    home = "admin/home/home.html"
    announcements = "admin/announcements/announcements.html"
    ECs = "admin/ECs/extenuating.html"
    ECs = "admin/ECs/extenuating.html"
    KB = "admin/KB/knowledgebase.html"
    
    knowledgeBaseAdd= "admin/KB/knowledgeBaseAdd.html"
    knowledgeBaseDuplicate= "admin/KB/knowledgeBaseDuplicate.html"
    knowledgeBaseEdit= "admin/KB/knowledgeBaseedit.html"
    
    reports = "admin/reports/reports.html"
    tickets = "admin/tickets/tickets.html"

    if page == "home":
        return app.send_static_file(home)
    elif page == "announcements":
        return app.send_static_file(announcements)
    elif page == "ECs":
        return app.send_static_file(ECs)
    elif page == "knowledgebase":
        return app.send_static_file(KB)
    elif page == "knowledgeBaseAdd":
        return app.send_static_file(knowledgeBaseAdd)
    elif page == "knowledgeBaseDuplicate":
        return app.send_static_file(knowledgeBaseDuplicate)
    elif page == "knowledgeBaseEdit":
        return app.send_static_file(knowledgeBaseEdit)
    elif page == "reports":
        return app.send_static_file(reports)
    elif page == "tickets":
        return app.send_static_file(tickets)
    else:
        return redirect(url_for("index"))

@app.route("/EC-Claim", methods=["POST"])
def ecClaim():
    if "username" not in session:
        return redirect(url_for("index"))
    data = request.form
    moduleDue = data.get("moduleDue")
    moduleName = data.get("moduleName")
    reasoning = data.get("reasoning")
    user = session['username']
    
    file_contents = []
    file_names = []
    for file_key in ["file1", "file2", "file3"]:
        if file_key in request.files:
            file = request.files[file_key]
            if file.filename != "":
                temp_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
                file.save(temp_path)
                with open(temp_path, "rb") as f:
                    file_contents.append(f.read())
                os.remove(temp_path)
                file_names.append(file.filename)

    db = ECDB()
    db.add_ec(user, moduleName, moduleDue, reasoning, file_contents, file_names)
        
    return redirect("/EC-Submit-Success")

@app.route("/EC-Submit-Success", methods=["GET"])
def ecSuccess():
    return app.send_static_file("dashboard/ECs/ECSuccess.html")

@app.route("/ECget", methods=["GET"])
def ecGet():
    db = ECDB()
    return jsonify(db.get_ecs()), 201

@app.route("/ECmark/<reasoning>", methods=["GET"])
def ecMark(reasoning):
    if "usernameAdmin" not in session:
        return redirect(url_for("index"))
    db = ECDB()
    content  = {reasoning}
    return db.update_ec_status(content,"APPROVED")

@app.route("/ECreject/<reasoning>", methods=["GET"])
def ecReject(reasoning):
    if "usernameAdmin" not in session:
        return redirect(url_for("index"))
    db = ECDB()
    content  = {reasoning}
    return db.update_ec_status(content,"REJECTED")

@app.route("/EC-Count", methods=["GET"])
def countEC():
    ecdb = ECDB()
    user = session['username']
    user_ec_count = ecdb.count_user_ecs(user)
    return {"user": user, "ec_count": user_ec_count}
    
if __name__ == "__main__":
    app.run(debug=True)
