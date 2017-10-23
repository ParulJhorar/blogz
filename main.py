from flask import Flask, request, redirect, render_template,flash,session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'y337kGcys&zP3B'
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body= db.Column(db.String(5000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner= owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog',backref='owner')   

    def __init__(self,username,password):
        self.username = username
        self.password = password   



@app.before_request
def require_login():
    allowed_routes = ['login','signup','index','blog']
    if request.endpoint not in allowed_routes and 'username' not in session :
        return redirect ('/login') 
    

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form ['password']
        user = User.query.filter_by(username=username).first()
        if username=='' or password == '':
            flash('Please provide username and password!','error') 
            return render_template('login.html')
        
       
       
        if user and user.password == password:
            session['username']=username
            flash("logged in")
            return redirect('/newpost')

        else:
            flash('User does not exist or Password is incorrect','error')
            

       
            

    return render_template('login.html')

@app.route('/signup', methods= ['POST','GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form ['verify']
        password_error=''
        verify_error=''
        existing_user = User.query.filter_by(username=username).first()
        if username=='':
            flash('Please fill in complete information','error')
            return render_template('signup.html')
        
        
        if not existing_user:
             
            
            if len(password)<3 or password == '':
                password_error="Please enter a valid password"
                return render_template('signup.html',username=username,password_error=password_error) 
                
            if verify!=password or verify =='':
                verify_error='passswords do not match'
                return render_template('signup.html',username=username,verify_error=verify_error)

            else:
                new_user= User(username,password)
                db.session.add(new_user)
                db.session.commit()
                session['username']=username
                return redirect('/newpost')
        else:
            flash('User already exist')
            
        
        
        
        
        

             
    return render_template('signup.html') 


@app.route('/newpost', methods= ['POST','GET'])

def newpost():
    owner = User.query.filter_by(username =session['username']).first()
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        
        if blog_title == '' or blog_body=='' :
            flash('Please complete your blog entry','error')
            return redirect('/newpost')     
            
        entry = Blog(blog_title, blog_body,owner)
        
        db.session.add(entry)
        db.session.commit()
        
        

        last_title=request.form.get('title')
        entry = Blog.query.filter_by(title=last_title).first()

      
        
        return redirect('/blog?id='+ str(entry.id)) 
   
      

    return render_template( 'newpost.html')


@app.route('/logout')
def logout():
        del session['username']
        return redirect ('/blog')    



@app.route('/blog', methods= ['POST','GET'])

def blog():
    
    all_blogs= Blog.query.all() 
    all_users= User.query.all() 
    
    
    
    if request.args:
        id=request.args.get('id')
       
        entry= Blog.query.get(id)
        owner1=entry.owner_id
        owner=User.query.filter_by(id=owner1).first()
        
        
       
        return render_template('singleblogpost.html', entry = entry,owner=owner)
    else:
        return render_template('blog.html',all_blogs=all_blogs,all_users=all_users)


@app.route('/', methods = ['POST','GET'])

def index():
    all_users= User.query.all() 
    if request.args:
        id=request.args.get('id')
        owner = User.query.get(id)
        

        entry=Blog.query.filter_by(owner=owner).all()
        return render_template('singleuser.html', entry = entry)
    else:
        return render_template('index.html',all_users=all_users)



   
       
if __name__ == '__main__':
    app.run()

