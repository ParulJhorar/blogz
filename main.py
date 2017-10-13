from flask import Flask, request, redirect, render_template,flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'y337kGcys&zP3B'
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body= db.Column(db.String(5000))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/newpost', methods= ['POST','GET'])

def newpost():
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        
        if blog_title == '' or blog_body=='' :
            flash('Please complete your blog entry','error')
            return redirect('/newpost')     
            
        entry = Blog(blog_title, blog_body)
        
        db.session.add(entry)
        db.session.commit()
        
        

        last_title=request.form.get('title')
        entry = Blog.query.filter_by(title=last_title).first()

      
        
        return redirect('/blog?id='+ str(entry.id)) #render_template('singleblogpost.html', entry =entry)
   
      

    return render_template( 'newpost.html')


@app.route('/blog', methods= ['POST','GET'])

def index():
    all_blogs= Blog.query.all() 
    
    if request.args:
        id=request.args.get('id')
        entry= Blog.query.get(id)
        return render_template('singleblogpost.html', entry = entry)
    else:
        return render_template('blog.html',all_blogs=all_blogs)
   
       
if __name__ == '__main__':
    app.run()

