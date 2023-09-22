from flask_wtf import FlaskForm
from wtforms import StringField, validators, TelField, DateField, TextAreaField, PasswordField, SubmitField, SearchField
from wtforms.validators import length, equal_to, email, data_required, ValidationError



class RegisterForm(FlaskForm):

    def validate_firstname(self, firstname_to_check):
        from employee import User
        first = User.query.filter_by(first_name=firstname_to_check.data).first()
        if first:
            raise ValidationError('First Name already exists! Please try a different first name')


    def validate_email_address(self, email_address_to_check):
        from employee import User
        address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if address:
            raise ValidationError('Email already exists! Please try a different Email')


    def validate_phonenumber(self, phonenumber_to_check):
        from employee import User
        phonenumber = User.query.filter_by(Phone_number=phonenumber_to_check.data).first()
        if phonenumber:
            raise ValidationError('Phone number already exists! Please try a different phone number')



    firstname = StringField(label='First Name:', validators= [length(min=2, max=30), data_required()])
    lastname = StringField(label='Last Name:', validators= [length(min=2, max=30), data_required()])
    email_address = StringField(label='Email id:', validators=[email(), data_required()])
    phonenumber = TelField(label='Phone Number:', validators= [length(max=10), data_required()])
    DOB = DateField(label='Date Of Birth:', validators= [data_required()])
    Address = TextAreaField(label = 'Address:', validators=[data_required()])
    password = PasswordField(label='Password:', validators= [length(min=6), data_required()])
    confirm_password = PasswordField(label='Confirm Password:', validators=[equal_to('password'), data_required()])
    Submit = SubmitField(label='Create Account')


class Login_form(FlaskForm):
    email_address = StringField(label='Email id:', validators=[data_required()])
    password = PasswordField(label='Password:', validators=[data_required()])
    Submit = SubmitField(label='Sign in')

class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[data_required()])
    submit = SubmitField("Submit")