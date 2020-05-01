from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# creating of the flask app
app = Flask(__name__)

# Telling the flask where the db will be stored !
# '///' - relative path , '////' - absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.sqlite3'
# creating the database
db = SQLAlchemy(app)


# Models : structure the data in the db //Backend stuff : just defined the structure of the db
class Blogpost(db.Model):
    # creating the fields of the relation
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_postede = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # this is going to print out,whenever we create a new Blogpost ,the model when created !!
    def __repr__(self):
        return 'Blog post : ' + str(self.id)


# confg through cmd line , the database
# 1-> from the .py file import the db
# 2-> them , db.create_all() : which will help create the db with the fields mentioned in the class
# 3-> from flask_started(.py) import the class that implements the db.model
# 4-> classname.query.all() : used to display the rows affected in the relation
# 5-> db.session.add(classname(fields = 'parameters',...)) : used to add data to the relation
# 6-> while adding the data, u need not specify data for primary key and dateTime !!
# 7-> classname.query.all()[specigy the index of list].give_the_field_name
# 8-> Blogpost.query.filter_by(author="dushi").all() : diplays the blogpost with the author as dushi
# 9-> Blogpost.query.get(): calls the blogpost by their id's or primary key
# 10-> db.session.delete(Blogpost.query.get(4)) : getting object of the blogpost to delete it
# 11-> Blogpost.query.get(3).author = 'anything' : updates the author of the post


# all_posts = [
#     {
#         'title': 'Post 1 ',
#         'content': 'Content 1',
#         'name': 'Dushi'
#
#     },
#     {
#         'title': 'Post 2 ',
#         'content': 'Content 2'
#     },
#     {
#         'title': 'Post 3 ',
#         'content': 'Content 3'
#     }
# ]


# defining the url where the website will be loaded
@app.route('/<string:name>/rollno/<int:num>')
# defining the function to be displayed
def hello(name, num):
    return "Hello world , this is " + name + " programming having roll no. " + str(num)


@app.route('/sum/<int:num1>/<int:num2>')
def sum(num1, num2):
    return str(num1 + num2)


# here , we have processed an html file
@app.route('/')
def index():
    return render_template('index.html')


# passing data from here to the html page(see the posts.html)
# for the purpose of takin i/p from the website and storing the value iin the db ,import request form flask
@app.route('/posts', methods=['GET'])
def posts():
    # if request.method == 'POST':
    #     # we are creating the object named post_title etc. so as to take input form the form
    #     post_title = request.form['title']
    #     post_content = request.form['content']
    #     post_author = request.form['author']
    #     # new_post object created to take input to the blogpost class
    #     new_post = Blogpost(title=post_title, content=post_content, author=post_author)
    #     # adding the content to the db in the current session
    #     db.session.add(new_post)
    #     # above we are just adding the data temporarily , we need to commit to make it permanent in the db
    #     db.session.commit()
    #     return redirect('/posts')
    # if we are not posting , then we are actually getting the data form the db
    if request.method == 'GET':
        # overriding all_posts by the content in the db , by using the blogpost.query.all()
        # we are ordering all the posts bby their date posted
        all_posts = Blogpost.query.order_by(Blogpost.date_postede).all()
        # below we are sending them to our frontend webisite
        return render_template('posts.html', posts=all_posts)


@app.route("/posts/delete/<int:id>")
def delete(id):
    post = Blogpost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')


@app.route("/posts/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    post = Blogpost.query.get_or_404(id)
    # when we are editing from the page
    if request.method == 'POST':
        post.title = request.form["title"]
        post.content = request.form["content"]
        post.author = request.form["author"]
        db.session.commit()
        return redirect("/posts")
    # when the url is called , the desired webpage shld be diplayed
    else:
        return render_template("edit.html", post=post)


@app.route("/posts/new", methods=['POST', 'GET'])
def newPost():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = Blogpost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = Blogpost.query.order_by(Blogpost.date_postede).all()
        return render_template('add_post.html')


if __name__ == "__main__":
    app.run(debug=True)
