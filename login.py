from flask import Flask,render_template,redirect,url_for,session
from flask_sqlalchemy import SQLAlchemy,request
# from sqlalchemy import update
app = Flask(__name__) #creating the Flask class object   
app.secret_key = "Hardik"  
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///ghp.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) 

class ghp(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    un = db.Column(db.String(80), unique=True, nullable=False)
    pd = db.Column(db.String(30),nullable = False)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.un} - {self.pd}"

@app.route('/')  
def home():  
    return render_template('home.html') 

@app.route('/login',methods = ['GET','POST'])
#@app.route('/login')  
def login():
    if request.method=="POST":
        # session['un'] = request.form['un']
        
        un1 = request.form['username']
        pw = request.form['password']
        session['un'] = un1
        print(un1,pw)
        mytodo = ghp.query.filter_by(un=un1,pd = pw).first()
        if mytodo is not None:
            return render_template('done.html',username = un1,password = pw)
        else:
            return render_template('ghp.html')
        #mytodo = ghp.query.get(un = un1).first()
        print(mytodo)
        
        #return render_template('done.html')
    mytodo = ghp.query.all()


    #ghp_ = ghp.query("INSERT INTO ghp (un, pd) VALUES (un, pw)")
    return render_template('login.html',mytodo = mytodo)

@app.route('/sign_up',methods = ['GET','POST'])
def sign_up():
    if request.method=="POST":
        un = request.form['username']
        pw = request.form['password']
        print(un,pw)

        myfunc = ghp(un = un,pd = pw)
        try:               
            db.session.add(myfunc)
            db.session.commit()
            return render_template('ghp1.html')
        except Exception as e:
            return "Sign-Up Failed"
        
    mytodo1 = ghp.query.all()
    return render_template('sign_up.html',mytodo1 = mytodo1)

# @app.route('/show')
# def products():
#     mytodo1 = ghp.query.all()
#     print(mytodo1)
#     return "This is product page"
@app.route('/dashboard')
def dashboard():
    alltodo = ghp.query.all()
    # print(alltodo)
    if 'un' in session:  
        return render_template('dashboard.html',alltodo = alltodo)  
    else:
        return redirect('/login')
@app.route("/Update/<int:sno>",methods = ['GET','POST'])
def Update(sno):
    alltodo = ghp.query.filter_by(sno=sno).first()

    if request.method == "POST":
        alltodo = ghp.query.filter_by(sno=sno).first()
        print(alltodo)
        alltodo.un = request.form['username']
        alltodo.pd = request.form['password']
        db.session.commit()
        return redirect('/dashboard')
    else:
       return render_template('/update.html',alltodo = alltodo)

@app.route("/Delete/<int:sno>")
def Delete(sno):
    alltodo = ghp.query.filter_by(sno=sno).first()
    # print("Hello")
    # print(alltodo)
    db.session.delete(alltodo)
    db.session.commit() 
    return redirect("/dashboard")  

@app.route('/logout')
def logout():
    session.pop('un', None) 
    return redirect('/')

# @app.route('/Random')
# def random():
#     return render_template('Random.html')

if __name__ =='__main__':  
    app.run(debug = True,port = 8000)  