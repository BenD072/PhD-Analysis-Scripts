from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime
import psycopg2
import os


# In interactive python terminal, need to activate the database
# from app import db
# db.create_all
# To delete the database entries - use db.session.query(GuestListDatabase).delete()
# Then db.session.commit()

app = Flask(__name__)  # Sets up the Flask application - __name__ references the current file
DATABASE_URL = os.environ.get('DATABASE_URL')  # If doesn't work then use direct database link from heroku account
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL  # This tells the app where the database is located. 3 slashes is a relative path (relative to current directory) and 4 is an absolute path
db = SQLAlchemy(app)  # Initialise the database

# Create model for the database
'''
class GuestListDatabase(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Sets up an column to hold the ID for each entry in the dataframe. Primairy key means that each ID will be unique
    name = db.Column(db.String(200), nullable=False)  # A text column to hold the guest's name
    date_created = db.Column(db.DateTime, default=datetime.utcnow)  # A column to hold the date the task was created
    RSVP = db.Column(db.String(200), nullable=False)  # A text column to hold whether the guest is attending or not attending


    def __repr__(self):
        return '<Guest %r>' % self.id  # Returns the name and the ID each time we create a new element in the database
'''


class CommentDatabase(db.Model):

    __tablename__ = 'comment_database'

    id = Column(Integer, primary_key=True)  # id of the status comment
    name = Column(String(200), nullable=False)  # Name of the person creating the status
    date_created = Column(DateTime, default=datetime.utcnow)
    comment = Column(String(2000), nullable=False)  # The actual comment of the status

    def __repr__(self):
        return '<Post %r>' % self.id  # Returns the name and the ID each time we create a new element in the database


class Replies(db.Model):

    __tablename__ = 'replies'

    id = Column(Integer, primary_key=True)  # id of the reply
    name = Column(String(200), nullable=False)
    reply = Column(String(200), nullable=False)  # The reply
    status_id = Column(Integer, ForeignKey('comment_database.id'))

    status = relationship("CommentDatabase", back_populates="replies")

    def __repr__(self):
        return "<Replies(name='%s', reply='%s')" % (self.name, self.reply)


CommentDatabase.replies = relationship("Replies", order_by=Replies.id, back_populates="status")

@app.route('/replies/<int:id>', methods=['POST', 'GET'])
def post_reply(id):
    comment = CommentDatabase.query.get_or_404(id)

    new_name = request.form['reply-name-entry'].strip()
    if new_name == '':
        new_name = 'Anonymous'

    new_reply = request.form['reply-comment-entry']
    comment.replies.append(Replies(name=new_name, reply=new_reply))

    try:
        db.session.add(comment)
        db.session.commit()
        all_posts = CommentDatabase.query.order_by(CommentDatabase.date_created.desc()).all()
        return render_template('comments.html', posts=all_posts)
    except:
        return 'There was an error adding your reply'


@app.route('/comments', methods=['POST', 'GET'])
def post_comment():
    if request.method == 'POST':
        name = request.form['name-entry']
        comment_text = request.form['comment-entry']

        new_post = CommentDatabase(name=name, comment=comment_text)

        try:
            db.session.add(new_post)
            db.session.commit()
            all_posts = CommentDatabase.query.order_by(CommentDatabase.date_created.desc()).all()
            return render_template('comments.html', posts=all_posts)
        except:
            return 'There was an error submitting your post'
    else:  # If not new post being made
        all_posts = CommentDatabase.query.order_by(CommentDatabase.date_created.desc()).all()
        return render_template('comments.html', posts=all_posts)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/comments-admin')
def load_admin_page():
    all_posts = CommentDatabase.query.order_by(CommentDatabase.date_created.desc()).all()
    return render_template('comments-admin.html', posts=all_posts)


@app.route('/delete/comment/<int:id>')
def delete_comment(id):
    comment_to_delete = CommentDatabase.query.get_or_404(id)  # queries the database by id. If doesn't find the id, returns a 404 error. This gets the task to be deleted

    try:
        db.session.delete(comment_to_delete)  # Deletes the item from the database based on the id passed in
        db.session.commit()
        return redirect('/comments-admin')  # Redirects back to the homepage
    except:
        return "There was a problem deleting that comment."


@app.route('/delete/reply/<int:id>')
def delete_reply(id):
    reply_to_delete = Replies.query.get_or_404(id)  # queries the database by id. If doesn't find the id, returns a 404 error. This gets the task to be deleted

    try:
        db.session.delete(reply_to_delete)  # Deletes the item from the database based on the id passed in
        db.session.commit()
        return redirect('/comments-admin')  # Redirects back to the homepage
    except:
        return "There was a problem deleting that comment."

'''
# Create an index route - landing page
@app.route('/guestlist', methods=['POST', 'GET'])  # '/' is the landing page url. POST/GET allows the route to send/recieve data from the database
def show_guestlist():  # Create a function of what to do when someone lands in the '/' url
    if request.method == 'POST':  # If a request to add information to the database is received
        guest_name = request.form['content']  # task_content will be set to the input from the html form object with the 'content' id
        if request.form['Attending_Button'] == 'Attending':
            new_guest_name = GuestListDatabase(name=guest_name, RSVP='Attending')
        elif request.form['Attending_Button'] == 'Not Attending':
            new_guest_name = GuestListDatabase(name=guest_name, RSVP='Not Attending')

        try:
            db.session.add(new_guest_name)  # Will add the new_guest_name object to the database
            db.session.commit()  # Comits to database
            guests = GuestListDatabase.query.order_by(GuestListDatabase.date_created.desc()).all()
            return render_template('Attending_Guest_List.html', tasks=guests)
        except:
            return 'There was an error adding your name'  # If adding name to database doesn't work, print error
    else:  # If no request is being made to add to the database
        guests = GuestListDatabase.query.order_by(GuestListDatabase.date_created.desc()).all()  # Queires database for items and then orders items by the date they were created. The .all() returns all items in the database, could also use .first() etc. to grab first
        return render_template('Attending_Guest_List.html', tasks=guests)  # Will render the index.html file. Flask automatically looks for html files in the templates folder. The tasks parameter is used in the html jinja sntax to render the table
'''

@app.route('/menu')
def menu_page():
    return render_template('menu.html')

@app.route('/directions')
def direction_page():
    return render_template('directions.html')


if __name__ == "__main__":
    app.run(debug=True)  # Run the app


# Template inherentance - create a master html file that contains skeleton of what each page will look like
# Then inherent that skeleton in other html files/pages

'''
<div class="content">

    <br>
    <h1 style="text-align:center">Add Your Name(s) to RSVP!</h1>

    <div>
    <form style="text-align:center" action="/guestlist" method="POST">  <!-- Creates a form for data input -->
        <input class="name-input-field" type="text" name="content" id="content">  <!-- Creates a text input field with the id as 'content'. Use this id in the app route to find/add information from this input field into the database -->
        <input class="button" type="submit" name="Attending_Button" value="Attending">  <!-- A submit button with the value label add task -->
        <input class="button" type="submit" name="Attending_Button" value="Not Attending">
    </form>
    </div>

</div>

<div style="text-align: center">
    <a style="width:500px" href="/guestlist" class="button"><strong>See the Guest List!</strong></a>
</div>
'''
