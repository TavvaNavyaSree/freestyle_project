from flask import Flask, render_template, redirect, url_for, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from forms import RegisterForm, Login_form, SearchForm
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_login import login_user, UserMixin, current_user, logout_user, login_required

#for admin_login, details are already saved in database
#email:admin1@gmail.com  password:admin1
#email:admin2@gmail.com  password:admin2
#email:admin3@gmail.com  password:admin3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee.db'
app.config['SECRET_KEY'] = 'a67dfdf3f895d870fd4da554'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)







#creating database for User
class User(db.Model, UserMixin):
   id = db.Column(db.Integer(), primary_key=True)
   first_name = db.Column(db.String(length=30), nullable = False, unique = True)
   last_name = db.Column(db.String(length=30), nullable = False)
   email_address = db.Column(db.String(length=50), nullable = False, unique = True)
   Phone_number = db.Column(db.Integer(), nullable =  False, unique = True)
   DOB = db.Column(db.String(length=10), nullable = False)
   Address = db.Column(db.String(length=200), nullable = False)
   password_hash = db.Column(db.String(length=60), nullable = False)
   Confirm_password = db.Column(db.String(length=60), nullable = False)

   @property
   def password(self):
       return self.password

   @password.setter
   def password(self, plain_text_password):
       self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')



   def check_password_correction(self, attempted_password):
       return bcrypt.check_password_hash(self.password_hash, attempted_password)


#creating database for Admin and saved 3 logins, assuming that admins are not to register
class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key = True)
    email = db.Column(db.String(length=50), nullable = False, unique = True)
    password = db.Column(db.String(length = 30), nullable = False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')


@app.route("/register", methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(first_name=form.firstname.data,
                              last_name=form.lastname.data,
                              email_address=form.email_address.data,
                              Phone_number=form.phonenumber.data,
                              DOB=form.DOB.data,
                              Address=form.Address.data,
                              password=form.password.data,
                              Confirm_password=form.confirm_password.data)
        db.session.add(user_to_create)
        db.session.commit()
        flash('You have registered successfully!', category='success')
        return redirect(url_for('home_page'))
    if form.errors != {}:
        for form_err in form.errors.values():
            flash(f'error creating user: {form_err}', category = 'danger')

    return render_template('register.html', form=form)


@app.route('/admin_login', methods = ['GET', 'POST'])
def admin_login():
    form=Login_form()
    if form.validate_on_submit():
        users_list = User.query.all()
        attempted = Admin.query.filter_by(email=form.email_address.data, password=form.password.data).first()
        if attempted:
            flash(f'Success! You are logged in as: {attempted.password}', category='success')
            login_user(attempted)
            return render_template("admin_userdetails.html", users=users_list)
        else:
            flash('Email id and password does not match! Please try again', category='danger')
    return render_template('login_admin.html', form=form)


@app.route('/user_login', methods = ['GET', 'POST'])
def user_login():
    form=Login_form()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(email_address=form.email_address.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            flash(f'Success! You are logged in as: {attempted_user.first_name}', category='success')
            login_user(attempted_user)
            return redirect(url_for('index'))
        else:
            flash('Email id and password does not match! Please try again', category='danger')
    return render_template('login.html', form=form)

@app.route('/user_details')
@login_required
def index():
    if login_user:
        users=list(User.query.all())
        return render_template("userdetails.html", details=users)



@app.context_processor
def base():
    form= SearchForm()
    return dict(form=form)

@app.route('/search', methods=['POST'])
def search():
    form=SearchForm()
    searching = User.query
    if form.validate_on_submit():
        searched= form.searched.data
        searching_for1 = searching.filter(User.first_name.like('%' +searched+ '%')|User.email_address.like('%' +searched+ '%'))
        searching_for1= searching_for1.order_by(User.first_name).all()
        return render_template("search.html", form=form, searched= searched, searching1=searching_for1)



@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out", category='info')
    return redirect(url_for('home_page'))
