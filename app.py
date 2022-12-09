#from multiprocessing.managers import _Namespace
from flask import Flask, redirect, request
from flask import render_template
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# create the app , or initialize it 
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db=SQLAlchemy(app)

# create model 
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(50), nullable=False)
    completed= db.Column(db.Integer, default=0)
    created_at=db.Column(db.DateTime , default=datetime.utcnow)

    def __str__(self):
        return self.id

    


# then create the route index
@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect ('/')
        except BaseException as e:
            return str(e)
    else:
        tasks = Todo.query.order_by(Todo.created_at).all()
        return render_template('index.html', tasks=tasks)
        
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)

if __name__=="__main__":
    app.run(debug=True)

