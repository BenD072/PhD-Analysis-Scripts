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


app = Flask(__name__)  # Sets up the Flask application - __name__ references the current file
DATABASE_URL = os.environ.get('DATABASE_URL') 
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL  

# Create model for the database

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

@app.route('/menu')
def menu_page():
    return render_template('menu.html')

@app.route('/directions')
def direction_page():
    return render_template('directions.html')


if __name__ == "__main__":
    app.run(debug=True)  # Run the app


