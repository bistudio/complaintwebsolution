from flask import url_for, flash, render_template, redirect, request
from app import app, db, bcrypt
from app.form import RegistrationForm, LoginForm, ComplaintForm, SearchForm\
    , SearchResultForm, PasswordResetRequestForm, ResetPasswordForm
from app.models import User, Complaint
from flask_login import login_user, logout_user, current_user, login_required
from app.table import Results
from datetime import datetime as dt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@app.route('/')
@app.route('/home')
@app.route('/complaint/home', methods=['GET', 'POST'])
def home():
    no_of_complaints = Complaint.query.count()
    no_of_open = Complaint.query.filter_by(complaint_status='Open').count()
    no_of_lowlevel = Complaint.query.filter_by(severity='LW').count()
    no_of_fos = Complaint.query.filter_by(severity='EFOS').count()
    no_of_closed = Complaint.query.filter_by(complaint_status='Closed').count()
    return render_template('home.html', title='Home'
                           , open=no_of_open, total=no_of_complaints
                           , low=no_of_lowlevel, fos=no_of_fos
                           , closed=no_of_closed, breach=0
                           )


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # hash the user password
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        created_user = form.username.data
        element = created_user.split(".")
        display_name = [n.capitalize() for n in element]
        if len(display_name) == 1:
            flash(f'{display_name[0]} - {user.id} account created, please log in', 'success')
        else:
            flash(f'{display_name[0]} {display_name[1]} - {user.id} account created, please log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful, please check email and or password!', 'danger')
        return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)


# @app.route('request_password_reset')
# def request_password_reset():
#     form = PasswordResetRequestForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         # s = Serializer()
#         if user is None:
#             flash(f'This email is incorrect or does not exist, please check or register for an account', 'info')
#             return redirect(url_for('register'))
#         else:
#             pass
#         pass
#     return render_template('password_reset_request.html', title='Password Reset Request', form=form)


@app.route('/reset_password')
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # hash the user password
            user = User(password=hashed_password)
            db.session.commit()
            flash(f'Your password has been updated successfully', 'success')
            return redirect(url_for('login'))
        else:
            flash(f'This email is incorrect or does not exist, please check or register for an account')
            return redirect(url_for('register'))
    return render_template('reset_password.html', title='Reset Password', form=form)


@app.route('/complaint/new', methods=['GET', 'POST'])
@login_required
def new_complaint():
    form = ComplaintForm()
    if form.validate_on_submit():
        complaint = Complaint(agreement_no=form.agreement_no.data,
                              manufacturer=form.manufacturer.data,
                              model=form.model.data,
                              product=form.product.data,
                              vehicle_age=form.vehicle_age.data,
                              centre=form.centre.data,
                              title=form.title.data,
                              first_name=form.first_name.data,
                              middle_name=form.middle_name.data,
                              last_name=form.last_name.data,
                              email=form.email.data,
                              contact_no=form.contact_no.data,
                              id=form.complaint_no.data,
                              complaint_group=form.complaint_group.data,
                              complaint_source=form.complaint_source.data,
                              complaint_narrative=form.complaint_narrative.data,
                              complaint_status=form.complaint_status.data,
                              severity=form.severity.data,
                              date_received=form.date_received.data,
                              reg_due_date=form.reg_due_date.data,
                              date_modified=None,
                              date_escalated=None,
                              date_acknowledged=None,
                              # company_outcome='',
                              # regulatory_outcome='',
                              # regulatory_reportable='',
                              # goodwill_offered='',
                              # goodwill_method='',
                              # goodwill_reason='',
                              # goodwill_amount='',
                              adviser=current_user)
        db.session.add(complaint)
        db.session.commit()
        flash(f'Complaint no {form.complaint_no.data} saved successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('create_complaint.html', title='New Complaint', form=form)


@app.route('/complaint/search', methods=['GET', 'POST'])
@login_required
def search_complaint():
    search = SearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('search_complaint.html', title='Search or Update a Complaint', form=search)


@app.route('/searchresults')
@login_required
def search_results(search):
    results = []
    search_select = search.data['select']
    search_string = search.data['search']
    search_st_dt = search.data['date_received_st']
    search_ed_dt = search.data['date_received_ed']

    if search_st_dt is None and search_ed_dt is None or (search_st_dt == '' and search_ed_dt == ''):
        if search_select == 'agreement_no':
            qry = db.session.query(Complaint).filter_by(agreement_no=search_string).all()
            results = qry
        if search_select == 'id':
            qry = db.session.query(Complaint).filter_by(id=search_string).all()
            results = qry
    else:
        if search_select == 'agreement_no':
            qry = db.session.query(Complaint) \
                .filter(Complaint.date_received.between(search_st_dt, search_ed_dt)) \
                .filter_by(agreement_no=search_string).all()
            results = qry
        if search_select == 'id':
            qry = db.session.query(Complaint) \
                .filter(Complaint.date_received.between(search_st_dt, search_ed_dt)) \
                .filter_by(id=search_string).all()
            results = qry

    if not results:
        flash('No results found!')
        return redirect('home')
    else:
        table = Results(results)
        table.border = True

        return render_template('searchresults.html', table=table)


def save_changes(complaint, form, new=False):
    """
    Save the changes to the database
    """
    # Get data from form and assign it to the correct attributes
    # of the SQLAlchemy table object
    complaint = ComplaintForm()
    complaint.name = form.artist.data
    complaint.complaint_narrative = form.complaint_narrative.data
    complaint.complaint_status = form.complaint_status.data
    complaint.date_modified = dt.utcnow
    complaint.publisher = form.publisher.data
    complaint.media_type = form.media_type.data
    if new:
        # Add the new album to the database
        db.session.add(complaint)
    # commit the data to the database
    db.session.commit()


@app.route('/complaint/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_complaint(id):
    complaint = Complaint.query.filter_by(id=id).first_or_404()
    current_date = dt.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    form = SearchResultForm()

    if form.submit():
        print('submitted')

    if form.validate():
        print('valid')

    print(form.errors)

    if form.validate_on_submit():
        complaint.agreement_no = form.agreement_no.data,
        complaint.manufacturer = form.manufacturer.data,
        complaint.model = form.model.data,
        complaint.product = form.product.data,
        complaint.vehicle_age = form.vehicle_age.data,
        complaint.centre = form.centre.data,
        complaint.title = form.title.data,
        complaint.first_name = form.first_name.data,
        complaint.middle_name = form.middle_name.data,
        complaint.last_name = form.last_name.data,
        complaint.email = form.email.data,
        complaint.contact_no = form.contact_no.data,
        complaint.id = form.complaint_no.data,
        complaint.complaint_group = form.complaint_group.data,
        complaint.complaint_source = form.complaint_source.data,
        complaint.complaint_narrative = form.complaint_narrative.data,
        complaint.complaint_status = form.complaint_status.data,
        complaint.severity = form.severity.data,
        complaint.date_received = form.date_received.data,
        complaint.reg_due_date = form.reg_due_date.data,
        complaint.date_modified = dt.utcnow,
        complaint.date_escalated = dt.utcnow,
        complaint.date_acknowledged = dt.utcnow,
        complaint.company_outcome = form.company_outcome.data,
        complaint.regulatory_outcome = form.regulatory_outcome.data,
        complaint.regulatory_reportable = form.regulatory_reportable.data,
        complaint.goodwill_offered = form.goodwill_offered.data,
        complaint.goodwill_method = form.goodwill_method.data,
        complaint.goodwill_reason = form.goodwill_reason.data,
        complaint.goodwill_narrative = form.goodwill_narrative.data,
        complaint.goodwill_amount = form.goodwill_amount.data,
        complaint.adviser = form.adviser.data
        db.session.commit()
        flash(f'Complaint no {form.complaint_no.data} updated successfully!', 'success')
        return redirect(url_for('complaint', id=complaint.id))
    elif request.method == 'GET':
        form.agreement_no.data = complaint.agreement_no,
        form.manufacturer.data = complaint.manufacturer,
        form.model.data = complaint.model,
        form.product.data = complaint.product,
        form.vehicle_age.data = complaint.vehicle_age,
        form.centre.data = complaint.centre,
        form.title.data = complaint.title,
        form.first_name.data = complaint.first_name,
        form.middle_name.data = complaint.middle_name,
        form.last_name.data = complaint.last_name,
        form.email.data = complaint.email,
        form.contact_no.data = complaint.contact_no,
        form.complaint_no.data = complaint.id,
        form.complaint_group.data = complaint.complaint_group,
        form.complaint_source.data = complaint.complaint_source,
        form.complaint_narrative.data = complaint.complaint_narrative,
        form.complaint_status.data = complaint.complaint_status,
        form.severity.data = complaint.severity,
        form.date_received.data = complaint.date_received,
        form.reg_due_date.data = complaint.reg_due_date,
        form.date_modified.data = complaint.date_modified,
        form.date_escalated.data = complaint.date_escalated,
        form.date_acknowledged.data = complaint.date_acknowledged,
        form.company_outcome.data = complaint.company_outcome,
        form.regulatory_outcome.data = complaint.regulatory_outcome,
        form.regulatory_reportable.data = complaint.regulatory_reportable,
        form.goodwill_offered.data = complaint.goodwill_offered,
        form.goodwill_method.data = complaint.goodwill_method,
        form.goodwill_reason.data = complaint.goodwill_reason,
        form.goodwill_narrative.data = complaint.goodwill_narrative,
        form.goodwill_amount.data = complaint.goodwill_amount,
        form.adviser.data = current_user
    return render_template('complaint.html', form=form, complaint=complaint, current_date=current_date)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
