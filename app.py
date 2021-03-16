from flask import Flask, render_template, request, redirect, url_for, flash
import datetime
from datetime import date
import os
from dotenv import load_dotenv
import pymongo
from bson.objectid import ObjectId

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')


MONGO_URI = os.environ.get('MONGO_URI')
DB_NAME = 'iifscDB'

client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]


def validate_form_coach(form):
    coach_fname = form.get('coach_fname')
    coach_lname = form.get('coach_lname')
    coach_email = form.get('coach_email')
    coach_phone = form.get('coach_phone')

    errors = {}

    if len(coach_fname) == 0:
        errors['blank_fname'] = "Name field cannot be blank"

    if len(coach_lname) == 0:
        errors['blank_lname'] = "Name field cannot be blank"

    if len(coach_email) == 0:
        errors['blank_email'] = "Email field cannot be blank"

    if len(coach_phone) == 0:
        errors['blank_phone'] = "Phone field cannot be blank"

    return errors


@app.route('/')
def index():
    return render_template('index.template.html')


@app.route('/rinks')
def rinks_list():
    locreq = request.args.get('location')

    criteria = {}

    if locreq:
        criteria['location'] = {
            '$regex': locreq, '$options': 'i'
        }

    rinks = db.rinks.find(criteria, {
        'name': 1,
        'location': 1,
        'phone': 1,
        'address.unit': 1,
        'address.building': 1,
        'address.street': 1,
        'website': 1,
    })

    return render_template('rinks.template.html',
                           rinks=rinks)


@app.route('/coaches')
def coaches_list():
    nrocnum = request.args.get('nroc_level')

    criteria = {}

    if nrocnum:
        criteria['nroc_level'] = {
            '$regex': nrocnum, '$options': 'i'
        }

    coaches = db.coaches.find(criteria, {
        'coach_lname': 1,
        'coach_fname': 1,
        'nroc_level': 1,
        'philosophy': 1,
        'coach_email': 1,
        'coach_phone': 1
    })

    return render_template('coaches.template.html',
                           coaches=coaches)


@app.route('/coaches/new_coach')
def add_newcoach():
    coaches = db.coaches.find()
    return render_template('form_newcoach.template.html',
                           coaches=coaches,
                           old_values={},
                           errors={})


@app.route('/coaches/new_coach', methods=["POST"])
def process_newcoach():
    errors = validate_form_coach(request.form)

    if len(errors) == 0:
        philosophy = request.form.get('philosophy')
        if len(philosophy) == 0:
            philosophy = "no philosophy"

        db.coaches.insert_one({
            "coach_fname": request.form.get('coach_fname'),
            "coach_lname": request.form.get('coach_lname'),
            "nroc_level": request.form.get('nroc_level'),
            "coach_email": request.form.get('coach_email'),
            "coach_phone": request.form.get('coach_phone'),
            "philosophy": philosophy
        })
        flash("File for Coach CREATED")
        return redirect(url_for('coaches_list'))
    else:
        all_nroc = db.coaches.find()
        return render_template('form_newcoach.template.html',
                               all_nroc=all_nroc,
                               errors=errors,
                               old_values=request.form)


@app.route('/coaches/<coach_id>/delete')
def del_coach(coach_id):
    coach_to_delete = db.coaches.find_one({
        '_id': ObjectId(coach_id)
    })
    return render_template('del_alert_coach.template.html',
                           coach_to_delete=coach_to_delete)


@app.route('/coaches/<coach_id>/delete', methods=['POST'])
def process_delete_coach(coach_id):
    db.coaches.remove({
        '_id': ObjectId(coach_id)
    })
    flash("File for Coach DELETED")
    return redirect(url_for('coaches_list'))


@app.route('/coaches/<coach_id>/update')
def update_coach(coach_id):
    all_nroc = db.coaches.find()
    coach_to_edit = db.coaches.find_one({
        '_id': ObjectId(coach_id)
    })
    return render_template('update_coach.template.html',
                           old_values=coach_to_edit,
                           all_nroc=all_nroc,
                           errors={})


@app.route('/coaches/<coach_id>/update', methods=['POST'])
def process_update_coach(coach_id):
    errors = validate_form_coach(request.form)

    if len(errors) == 0:
        db.coaches.update_one({
            '_id': ObjectId(coach_id)
        }, {
            '$set': {
                "coach_fname": request.form.get('coach_fname'),
                "coach_lname": request.form.get('coach_lname'),
                "nroc_level": request.form.get('nroc_level'),
                "coach_email": request.form.get('coach_email'),
                "coach_phone": request.form.get('coach_phone'),
                "philosophy": request.form.get('philosophy')
            }
        })
        flash("File for Coach UPDATED")
        return redirect(url_for('coaches_list'))
    else:
        all_nroc = db.coaches.find()
        coach_to_edit = db.coaches.find_one({
            '_id': ObjectId(coach_id)
        })
        old_values = {**coach_to_edit, **request.form}
        return render_template('update_coach.template.html',
                               old_values=old_values,
                               all_nroc=all_nroc,
                               errors=errors)


@app.route('/students')
def students_list():
    skreq = request.args.get('skate_level')

    criteria = {}

    if skreq:
        criteria['skate_level'] = {
            '$regex': skreq, '$options': 'i'
        }

    students = db.students.find(criteria, {
        'student_lname': 1,
        'student_fname': 1,
        'skate_level': 1,
        'age': 1,
    })

    return render_template('students.template.html',
                           students=students)


def validate_form_student(form):
    student_fname = form.get('student_fname')
    student_lname = form.get('student_lname')
    nation = form.get('nation')
    student_email = form.get('student_email')
    student_phone = form.get('student_phone')
    dob_day = form.get('dob_day')
    dob_month = form.get('dob_month')
    dob_year = form.get('dob_year')

    errors = {}

    if len(student_fname) == 0:
        errors['blank_fname'] = "Name field cannot be blank"

    if len(student_lname) == 0:
        errors['blank_lname'] = "Name field cannot be blank"

    if len(student_email) == 0:
        errors['blank_email'] = "Email field cannot be blank"

    if len(student_phone) == 0:
        errors['blank_phone'] = "Phone field cannot be blank"

    if len(nation) == 0:
        errors['blank_nation'] = "Nationality field cannot be blank"

    if len(dob_day) == 0:
        errors['x_dob'] = "Please enter a valid date of birth"

    if len(dob_month) == 0:
        errors['x_dob'] = "Please enter a valid date of birth"

    if len(dob_year) == 0:
        errors['x_dob'] = "Please enter a valid date of birth"

    # if float(dob_day) > 31 or float(dob_day) < 1:
    #     errors['x_dob'] = "Please enter a valid date of birth"

    # if float(dob_month) > 12 or float(dob_month) < 1:
    #     errors['x_dob'] = "Please enter a valid date of birth"

    # if float(dob_year) > 2018 or float(dob_year) <= 1941:
    #     errors['x_dob'] = "Please enter a valid date of birth"

    return errors


def cal_age(form):
    dob_day = form.get('dob_day')
    dob_month = form.get('dob_month')
    dob_year = form.get('dob_year')

    dob_str = dob_day + dob_month + dob_year
    dob_dt = datetime.datetime.strptime(dob_str, '%d%m%Y')

    today = date.today()
    today_str = today.strftime("%Y-%m-%d")
    cur_dt = datetime.datetime.strptime(today_str, '%Y-%m-%d')

    age_td = str(cur_dt - dob_dt)
    age_days_str = age_td.rstrip('days, 00:00:00')
    age_days_int = int(age_days_str)
    age = int(age_days_int // 365.2425)

    return age


def convert_month(form):
    m = request.form.get('dob_month')
    if m == "01" or "1":
        m = "JAN"
    elif m == "02" or "2":
        m = "FEB"
    elif m == "03" or "3":
        m = "MAR"
    elif m == "04" or "4":
        m = "APR"
    elif m == "05" or "5":
        m = "MAY"
    elif m == "06" or "6":
        m = "JUN"
    elif m == "07" or "7":
        m = "JUL"
    elif m == "08" or "8":
        m = "AUG"
    elif m == "09" or "9":
        m = "SEP"
    elif m == "10":
        m = "OCT"
    elif m == "11":
        m = "NOV"
    elif m == "12":
        m = "DEC"
    return m


@app.route('/students/new_skater')
def add_newskater():
    students = db.students.find()
    return render_template('form_newskater.template.html',
                           students=students,
                           errors={},
                           old_values={})


@app.route('/students/new_skater', methods=["POST"])
def process_newskater():
    errors = validate_form_student(request.form)

    if len(errors) == 0:
        age = cal_age(request.form)

        dob_month = convert_month(request.form)

        db.students.insert_one({
            "student_fname": request.form.get('student_fname'),
            "coach_lname": request.form.get('student_lname').upper(),
            "skate_level": request.form.get('skate_level'),
            "nation": request.form.get('nation').upper(),
            "student_email": request.form.get('student_email'),
            "student_phone": request.form.get('student_phone'),
            "age": age,
            "date_of_birth": {
                "dob_year": request.form.get('dob_year'),
                "dob_month": dob_month,
                "dob_day": request.form.get('dob_day')
            }
        })
        flash("File for Skater CREATED")
        return redirect(url_for('students_list'))
    else:
        all_sklvl = db.students.find()
        return render_template('form_newskater.template.html',
                               all_sklvl=all_sklvl,
                               errors=errors,
                               old_values=request.form)


@app.route('/students/<student_id>/delete')
def del_skater(student_id):
    student_to_delete = db.students.find_one({
        '_id': ObjectId(student_id)
    })
    return render_template('del_alert_skater.template.html',
                           student_to_delete=student_to_delete)


@app.route('/students/<student_id>/delete', methods=['POST'])
def process_delete_student(student_id):
    db.students.remove({
        '_id': ObjectId(student_id)
    })
    flash("File for Coach DELETED")
    return redirect(url_for('students_list'))


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=8080,
            debug=True)
