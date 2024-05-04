from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
from app import app, db
from app.forms import LoginForm
from app.models import User, Send, Reply
from flask import request
from urllib.parse import urlparse
from flask import session
from app.forms import RegistrationForm, SendForm, ReplyForm

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('user', username=current_user.username))
    return redirect(url_for('login'))
  
@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
  if username is None:
        # Redirect to a default username or handle appropriately
    return redirect(url_for('login'))
  if current_user.username != username:
    abort(403)  # HTTP status code for "Forbidden"
  user = {'username': 'Miguel'}
  posts = [
    {
      'author': {'username': 'John'},
      'body': 'Beautiful day in Portland!'
      }, {
        'author': {'username': 'Susan'},
        'body': 'The Avengers movie was so cool!'
        }
      ]
  return render_template('flask_index.html', title='Home Page', posts=posts)

@app.route('/login',methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('user'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user is None or not user.check_password(form.password.data):
        flash('Invalid username or password')
        return redirect(url_for('login'))
    login_user(user)
    next_page = request.args.get('next')
    if not next_page or urlparse(next_page).netloc != '':
      next_page = url_for('user', username=current_user.username)
    return redirect(next_page)
  return render_template('flask_login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
  logout_user() 
  return redirect(url_for('login')) 


@app.route('/register', methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('user'))
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User(username=form.username.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    flash('Congratulations, you are now a registered user!')
    return redirect(url_for('login'))
  return render_template('flask_register.html', title='Register', form=form)


@app.route('/user/<username>/send', methods=['GET', 'POST'])
@login_required
def send(username):
    if current_user.username != username:
      abort(403)  # HTTP status code for "Forbidden"
    form = SendForm()
    if form.validate_on_submit():
        send = Send(body=form.send.data, author=current_user, anonymous=form.anonymous.data, labels=form.label.data)
        db.session.add(send)
        db.session.commit()
        flash('Your message has been sent!')
        return redirect(url_for('user', username=current_user.username))
    return render_template('flask_send.html', title='Send Message', form=form)
  
@app.route('/user/<username>/reply', methods=['GET', 'POST'])
@login_required
def reply(username):
    if current_user.username != username:
      abort(403) 
    form = ReplyForm()
    sends = Send.query.order_by(Send.id.desc()).limit(5).all()
    if form.validate_on_submit():
        send = Send.query.get_or_404(form.send_id.data)
        reply = Reply(body=form.reply.data, author=current_user, anonymous=form.anonymous.data, sendId=send.id)
        db.session.add(reply)
        db.session.commit()
        flash('Your reply has been posted!')
        return redirect(url_for('user', username=current_user.username))
    return render_template('flask_reply.html', title='Reply Message', form=form, sends=sends)
'''  
@app.route('/label', methods=['GET', 'POST'])
@login_required
def label():
    form = LabelForm()
    if form.validate_on_submit():
        label = Labels(label=form.label.data)
        db.session.add(label)
        db.session.commit()       
        flash('Your label has been added!')   
        return redirect(url_for('send'))
    return render_template('flask_label.html', title='Add Label', form=form)'''