from flask import Flask, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SECRET_KEY'] = 'TEST'

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"item: {self.item}"

migrate = Migrate(app, db)

@app.route('/', methods=['GET'])
def index():
    items = Todo.query.all()
    return render_template(
        'index.html',
        items = items
    )
    
    

@app.route('/add', methods=['POST'])
def add():
    item = request.form.get('item')
    print(item)
    if item != '':
        i = Todo(item=item)
        db.session.add(i)
        db.session.commit()
        flash('Item Added', 'success')
        return redirect('/')
    else:
        flash('Please add item', 'error')
        return redirect('/')
@app.route('/delete/<int:id>')
def erase(id):
    item = Todo.query.get(id)
    db.session.delete(item)
    db.session.commit()
    flash(f'Complete {item}')
    return redirect('/')
    


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)