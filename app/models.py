from datetime import datetime as dt
from datetime import timedelta
from uuid import uuid4
from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):

    def reg_user_id(self):
        return int(str(uuid4().int)[6:12])

    id = db.Column(db.Integer, primary_key=True, default=reg_user_id)
    username = db.Column(db.String(60), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    date_created = db.Column(db.DateTime, default=dt.utcnow)
    date_modified = db.Column(db.DateTime, default=dt.utcnow)
    complaints = db.relationship('Complaint', backref='adviser', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.date_created}')"


class Complaint(db.Model):

    def complaint_id(self):
        return int(str(uuid4().int)[8:14])

    id = db.Column(db.Integer, primary_key=True, default=complaint_id)
    complaint_group = db.Column(db.String(100), nullable=False)
    complaint_source = db.Column(db.String(60), nullable=False)
    complaint_status = db.Column(db.String(30), nullable=False)
    severity = db.Column(db.String(30), nullable=False)
    complaint_narrative = db.Column(db.Text, nullable=False)
    agreement_no = db.Column(db.String(60), nullable=True)
    product = db.Column(db.String(60), nullable=True)
    manufacturer = db.Column(db.String(60), nullable=True)
    model = db.Column(db.String(30), nullable=True)
    vehicle_age = db.Column(db.String(30), nullable=True)
    centre = db.Column(db.String(150), nullable=True)
    company = db.Column(db.String(150), nullable=True)
    title = db.Column(db.String(20), nullable=True)
    first_name = db.Column(db.String(100), nullable=True)
    middle_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    contact_no = db.Column(db.String(60), nullable=True)
    date_received = db.Column(db.DateTime, default=dt.utcnow)
    reg_due_date = db.Column(db.DateTime, default=(dt.utcnow() + timedelta(days=56)))
    date_modified = db.Column(db.DateTime, default=dt.utcnow)
    date_escalated = db.Column(db.DateTime, default=dt.utcnow)
    date_acknowledged = db.Column(db.DateTime, default=dt.utcnow)
    company_outcome = db.Column(db.String(60), nullable=True)
    regulatory_outcome = db.Column(db.String(60), nullable=True)
    regulatory_reportable = db.Column(db.String(10), nullable=True)
    goodwill_offered = db.Column(db.String(10), nullable=True)
    goodwill_method = db.Column(db.String(60), nullable=True)
    goodwill_reason = db.Column(db.String(60), nullable=True)
    goodwill_narrative = db.Column(db.Text, nullable=True)
    goodwill_amount = db.Column(db.Float(precision=5, asdecimal=True, decimal_return_scale=2), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"'{self.id}', '{self.complaint_group}', '{self.complaint_source}'," \
               f" '{self.complaint_status}', '{self.complaint_narrative}' ,'{self.date_received}'," \
               f" '{self.date_modified}', '{self.date_acknowledged}','{self.date_escalated}', " \
               f"'{self.reg_due_date}','{self.manufacturer}', '{self.model}'," \
               f"'{self.vehicle_age}','{self.product}', '{self.agreement_no}'," \
               f"'{self.title}','{self.first_name}', '{self.middle_name}'," \
               f"'{self.last_name}','{self.email}', '{self.contact_no}'," \
               f"'{self.company}','{self.company_outcome}', '{self.regulatory_outcome}'," \
               f"'{self.regulatory_reportable}','{self.goodwill_offered}', '{self.goodwill_reason}'," \
               f"'{self.goodwill_method}','{self.goodwill_narrative}','{self.goodwill_amount}', '{self.user_id}'"
