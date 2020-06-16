from flask_table import Table, Col, LinkCol, DatetimeCol
from dateparser import date_parser


class Results(Table):
    id = Col('Complaint No', show=True, th_html_attrs=None)
    complaint_group = Col('Complaint Group')
    complaint_status = Col('Complaint Status')
    date_received = Col('Date Received')
    date_modified = Col('Date Modified')
    date_escalated = Col('Date Escalated')
    date_acknowledged = Col('Date Acknowledged')
    reg_due_date = Col('Reg. Due Date')
    severity = Col('Severity')
    agreement_no = Col('Agreement No')
    manufacturer = Col('Manufacturer')
    model = Col('Model')
    vehicle_age = Col('Vehicle Age')
    product = Col('Product')
    user_id = Col('Adviser Id')
    update = LinkCol('Update/Edit', 'update_complaint', url_kwargs=dict(id='id'))



