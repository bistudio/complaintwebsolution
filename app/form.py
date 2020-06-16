from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, BooleanField, SelectField, SubmitField\
    , TextAreaField, DateTimeField, IntegerField, DateField
from wtforms.validators import EqualTo, DataRequired, Length, Email, ValidationError
import uuid as uid
from datetime import datetime as dt
from datetime import timedelta
from app.models import User


# create user registration form


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=13)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('User already Exists!')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email already Exists!')


# create user login form


class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=13)])
    remember = BooleanField('Remember my details')
    submit = SubmitField('Login')

# create password reset request form


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

# create user reset password form


class ResetPasswordForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Reset Password', validators=[DataRequired(), Length(min=8, max=13)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


# create new app form


def complaint_no():
    return str(uid.uuid4().int)[2:7]


product_choices = [(None, 'Select'), ('PCP', 'PCP'), ('HP', 'HP'), ('Other', 'Other')]
severity_choices = [(None, 'Select'), ('Low', 'Low'), ('Escalated to CR', 'Escalated to CR'), ('Escalated - FOS', 'Escalated - FOS')]
manufacturer_choices = [(None, 'Select'), ('Toyota', 'Toyota'), ('Lexus', 'Lexus'), ('Non-Franchise', 'Non-Franchsie'), ('Other', 'Other')]
model_choices = [(None, 'Select'), ('Aygo', 'Aygo'), ('Aurius', 'Aurius'),
                 ('Avensis', 'Avensis'), ('C-HR', 'C-HR'), ('GT86', 'GT86'), ('Hiace', 'Hiace'),
                 ('Prius', 'Prius'), ('Prius +', 'Prius +'), ('Proace', 'Proace')
    , ('LCR', 'Land Cruiser'), ('Supra', 'Supra'), ('Yaris', 'Yaris'), ('RAV 4', 'RAV 4'), ('Es', 'Es')
    , ('Is', 'Is'), ('Gs', 'Gs'), ('Ls', 'Ls'), ('Rx', 'Rx'), ('Lc', 'Lc'), ('Ct', 'CT200h')
    , ('Non-Fran', 'Non-Franchise')]
vechicle_age_choices = [(None, 'Select'), ('New', 'New'), ('Used', 'Used'), ('Demo', 'Demo'), ('Other', 'Other')]
title_choices = [(None, 'Select'), ('Mr', 'Mr'), ('Mrs', 'Mrs'), ('Ms', 'Ms'),
                 ('Dr', 'Dr'), ('Lord', 'Lord'), ('Sir', 'Sir'), ('Esq', 'Esq'), ('Other', 'Other')]
complaint_grp_choices = [(None, 'Select'), ('Staff', 'Staff'), ('Aff', 'Affordability')
    , ('MM', 'Mis-selling & Mis-description'), ('CFI', 'Charges, Fees & Interests')
    , ('FDFT', 'Financial Difficulty Fair Treatment'), ('SQ', 'Satisfactory Quality')
    , ('SRV', 'Service'), ('Other', 'Other')]
complaint_source_choices = [(None, 'Select'), ('Email', 'Email'), ('Telephone', 'Telephone')
    , ('In-Person', 'In-Person'), ('FOS', 'FOS'), ('CMC', 'CMC'), ('Centre', 'via Centre'), ('Other', 'Other')]
centre_chocies = [(None, 'Select',), ('006808', 'Inchcape Basingstoke [006808]')
    , ('005826', 'Steven Eagell Milton Keynes [005826]'), ('006211', 'Jemca Epsom [006211]')]
company_outcome_choices = [(None, 'Select'), ('Upheld','Upheld'),('Not Upheld','Not Upheld')
    ,('Partially Upheld','Partially Upheld')]
regulatory_outcome_choices = [(None, 'Select'), ('Upheld','Upheld'),('Not Upheld','Not Upheld')
    ,('Partially Upheld','Partially Upheld')]
complaint_status_choices = [('Open','Open'), ('Resolved', 'Resolved'), ('Closed', 'Closed')]
yes_no_choices = [('Yes', 'Yes'), ('No', 'No')]


class ComplaintForm(FlaskForm):
    agreement_no = StringField('Agreement No', validators=[Length(min=10, max=30)])
    product = SelectField('Product', validators=[DataRequired()], choices=product_choices, default=product_choices[0])
    manufacturer = SelectField('Manufacturer', validators=[DataRequired()],
                               choices=manufacturer_choices, default=manufacturer_choices[0])
    model = SelectField('Model', validators=[DataRequired()],
                        choices=model_choices, default=model_choices[0])
    vehicle_age = SelectField('Vehicle Age', validators=[DataRequired()],
                              choices=vechicle_age_choices, default=vechicle_age_choices[0])
    centre = SelectField('Centre', choices=centre_chocies, default=centre_chocies[0])
    company = StringField('Company')
    title = SelectField('Title', choices=title_choices, default=title_choices[0])
    first_name = StringField('First Name')
    middle_name = StringField('Middle Name')
    last_name = StringField('Last Name')
    contact_no = StringField('Contact No')
    email = StringField('Email Address', validators=[Email()])
    adviser = StringField(validators=[DataRequired()], default='damian fadahunsi')
    complaint_no = StringField('Complaint No', validators=[DataRequired()], default=complaint_no)
    complaint_status = StringField('Complaint Status', validators=[DataRequired()], default='Open')
    complaint_group = SelectField('Complaint Group', validators=[DataRequired()],
                                  choices=complaint_grp_choices, default=complaint_grp_choices[0])
    complaint_source = SelectField('Complaint Source', validators=[DataRequired()],
                                   choices=complaint_source_choices, default=complaint_source_choices[0])
    complaint_narrative = TextAreaField('Complaint Narrative', validators=[DataRequired(), Length(min=2, max=500)])
    severity = SelectField('Severity', validators=[DataRequired()], choices=severity_choices, default=severity_choices[0])
    date_received = DateTimeField('Date Received', format='%d/%m/%Y', validators=[DataRequired()], default=dt.utcnow)
    reg_due_date = DateTimeField('Reg. Due Date', format='%d/%m/%Y', validators=[DataRequired()],
                                 default=dt.utcnow() + timedelta(days=56))
    date_modified = DateTimeField('Date Modified', format='%d/%m/%Y', default=dt.utcnow)
    date_acknowledged = DateTimeField('Date Acknowledged', format='%d/%m/%Y', default=dt.utcnow)
    date_escalated = DateTimeField('Date Escalated', format='%d/%m/%Y', default=dt.utcnow)
    # company_outcome = SelectField('Company Outcome', choices=company_outcome_choices, default=company_outcome_choices[0])
    # regulatory_outcome = SelectField('Regulatory Outcome', choices=regulatory_outcome_choices,
    #                               default=regulatory_outcome_choices[0])
    # regulatory_reportable=SelectField('Regulatory Reportable', choices=yes_no_choices, default=yes_no_choices[1])
    # goodwill_offered = SelectField('Goodwill Offered', choices=yes_no_choices, default=yes_no_choices[1])
    # goodwill_reason = StringField('Goodwill Reason')
    # goodwill_method = StringField('Goodwill Reason')
    # goodwill_narrative = TextAreaField('Complaint Narrative', validators=[Length(min=2, max=500)])
    # goodwill_amount = IntegerField('Goodwill Amount')
    submit = SubmitField('Save')

# create a search app form


class SearchForm(FlaskForm):
    id = IntegerField('Complaint No')
    agreement_no = StringField('Agreement No')
    search_method = [('agreement_no', 'Agreement No'), ('id', 'Complaint No')]
    select = SelectField('by:', choices=search_method, default=search_method[1])
    date_received_st = DateField('Received Start :')
    date_received_ed = DateField('Received End :')
    search = StringField('')
    submit = SubmitField('Search')

# create search result form


class SearchResultForm(FlaskForm):
    agreement_no = StringField('Agreement No')
    product = StringField('Product')
    manufacturer = StringField('Manufacturer')
    model = StringField('Model')
    vehicle_age = StringField('Vehicle Age')
    centre = StringField('Centre')
    company = StringField('Company')
    title = StringField('Title')
    first_name = StringField('First Name')
    middle_name = StringField('Middle Name')
    last_name = StringField('Last Name')
    contact_no = StringField('Contact No')
    email = StringField('Email Address ')
    adviser = StringField('Adviser')
    complaint_no = StringField('Complaint No')
    complaint_status = SelectField('Complaint Status', validators=[DataRequired()]
                                   , choices=complaint_status_choices, default=complaint_status_choices[0])
    complaint_group = StringField('Complaint Group')
    complaint_source = StringField('Complaint Source')
    complaint_narrative = TextAreaField('Complaint Narrative')
    severity = SelectField('Severity', validators=[DataRequired()], choices=severity_choices, default=severity_choices[0])
    date_received = DateTimeField('Date Received')
    reg_due_date = DateTimeField('Reg. Due Date')
    date_modified = DateTimeField('Date Modified', validators=[DataRequired()], default=dt.utcnow)
    date_acknowledged = DateTimeField('Date Acknowledged', format='%d/%m/%Y', default=dt.utcnow)
    date_escalated = DateTimeField('Date Escalated', format='%d/%m/%Y', default=dt.utcnow)
    company_outcome = SelectField('Company Outcome', choices=company_outcome_choices, default=company_outcome_choices[0])
    regulatory_outcome = SelectField('Regulatory Outcome', choices=regulatory_outcome_choices,
                                  default=regulatory_outcome_choices[0])
    regulatory_reportable = SelectField('Regulatory Reportable'
                                        , choices=yes_no_choices, default=yes_no_choices[1])
    goodwill_offered = SelectField('Goodwill Offered', choices=yes_no_choices, default=yes_no_choices[1])
    goodwill_reason = StringField('Goodwill Reason')
    goodwill_method = StringField('Goodwill Method')
    goodwill_narrative = TextAreaField('Goodwill Narrative', validators=[DataRequired(), Length(min=2, max=500)])
    goodwill_amount = IntegerField('Goodwill Amount')
    submit = SubmitField('Update')
