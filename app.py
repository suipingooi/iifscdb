from flask import Flask, render_template, request, redirect, url_for, flash
import datetime
from datetime import date, timedelta
import os
from dotenv import load_dotenv
import pymongo
from bson.objectid import ObjectId
import cloudinary
import cloudinary.uploader
import cloudinary.api

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif', '.jpeg']
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

cloudinary.config(
    cloud_name=os.environ.get('CLOUD_NAME'),
    api_key=os.environ.get('API_KEY'),
    api_secret=os.environ.get('API_SECRET')
)

MONGO_URI = os.environ.get('MONGO_URI')
DB_NAME = 'iifscDB'

client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]

CLOUDINARY_URL = os.environ.get('CLOUDINARY_URL')


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
            'imgurl': 1
        })
        return render_template('rinks.template.html',
                               rinks=rinks)
    else:
        rinks = db.rinks.find()
        return render_template('rinks.template.html',
                               rinks=rinks)


# database list of coaches
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
            'coach_phone': 1,
            'imgurl': 1
        })

        return render_template('list_coaches.template.html',
                               coaches=coaches)

    else:
        coaches = db.coaches.find()
        return render_template('list_coaches.template.html',
                               coaches=coaches)


# adding a new coach with validation of forms
@app.route('/coaches/new_coach')
def add_newcoach():
    coaches = db.coaches.find()
    return render_template('form_newcoach.template.html',
                           coaches=coaches,
                           old_values={},
                           errors={})


def validate_form_coach(form):
    coach_fname = form.get('coach_fname')
    coach_lname = form.get('coach_lname')
    coach_email = form.get('coach_email')
    coach_phone = form.get('coach_phone')
    profile = request.files['profile']

    errors = {}

    if len(coach_fname) == 0 or coach_fname.isspace():
        errors['blank_fname'] = "Name field cannot be blank"

    if len(coach_lname) == 0 or coach_lname.isspace():
        errors['blank_lname'] = "Name field cannot be blank"

    if len(coach_email) == 0 or coach_email.isspace():
        errors['blank_email'] = "Email field cannot be blank"

    if len(coach_phone) == 0 or coach_phone.isspace():
        errors['blank_phone'] = "Phone field cannot be blank"

    if profile.filename != "":
        prof = profile.filename
        ft = ["jpg", "png", "gif", "jpeg"]
        x = []
        for i in ft:
            if prof.find(i) > 0:
                x.append(i)
        if x == []:
            errors["x_filetype"] = "Filetype .jpg .jpeg .png .gif only"

        profile.seek(0, os.SEEK_END)
        file_size = profile.tell()
        if file_size > 5 * 1024 * 1024:
            errors["file_xl"] = "File is too large"
        profile.seek(0, 0)

    return errors


@app.route('/coaches/new_coach', methods=["POST"])
def process_newcoach():
    errors = validate_form_coach(request.form)

    if len(errors) == 0:
        cfname = request.form.get('coach_fname').lower()
        clname = request.form.get('coach_lname')
        nroc_level = request.form.get('nroc_level')
        coach_email = request.form.get('coach_email')
        coach_phone = "+65 " + request.form.get('coach_phone')

        philosophy = request.form.get('philosophy')
        if len(philosophy) == 0 or philosophy.isspace():
            philosophy = "no philosophy"

        profile = request.files['profile']
        if profile.filename == "":
            avatar = os.environ['AVATAR']

            db.coaches.insert_one({
                "coach_fname": cfname.title(),
                "coach_lname": clname.title(),
                "nroc_level": nroc_level,
                "coach_email": coach_email,
                "coach_phone": coach_phone,
                "philosophy": philosophy.title(),
                "imgurl": avatar

            })
            flash("File for Coach CREATED")
            return redirect(url_for('coaches_list'))
        else:
            pf = cloudinary.uploader.upload(profile.stream,
                                            public_id=cfname,
                                            folder='iifscdb/coaches/',
                                            resource_type='image')
            db.coaches.insert_one({
                "coach_fname": cfname.title(),
                "coach_lname": clname.title(),
                "nroc_level": nroc_level,
                "coach_email": coach_email,
                "coach_phone": coach_phone,
                "philosophy": philosophy.title(),
                "imgurl": pf['url']

            })
            flash("File for Coach CREATED")
            return redirect(url_for('coaches_list'))
    else:
        all_nroc = db.coaches.find()
        return render_template('form_newcoach.template.html',
                               all_nroc=all_nroc,
                               errors=errors,
                               old_values=request.form)


# deleting coach entry with confirmation alert
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


# updating coach details
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
        cfname = request.form.get('coach_fname')
        clname = request.form.get('coach_lname')
        nroc_level = request.form.get('nroc_level')
        coach_email = request.form.get('coach_email')
        coach_phone = request.form.get('coach_phone')
        philosophy = request.form.get('philosophy')
        if len(philosophy) == 0:
            philosophy = "no philosophy"

        profile = request.files['profile']
        if profile.filename == "":
            avatar = os.environ['AVATAR']

            db.coaches.update_one({
                '_id': ObjectId(coach_id)
            }, {
                '$set': {
                    "coach_fname": cfname.title(),
                    "coach_lname": clname.title(),
                    "nroc_level": nroc_level,
                    "coach_email": coach_email,
                    "coach_phone": coach_phone,
                    "philosophy": philosophy.title(),
                    "imgurl": avatar
                }
            })
            flash("File for Coach UPDATED")
            return redirect(url_for('coaches_list'))

        else:
            cfname = request.form.get('coach_fname').lower()
            pf = cloudinary.uploader.upload(profile.stream,
                                            public_id=cfname,
                                            folder='iifscdb/coaches/',
                                            resource_type='image')
            db.coaches.update_one({
                '_id': ObjectId(coach_id)
            }, {
                '$set': {
                    "coach_fname": request.form.get('coach_fname').title(),
                    "coach_lname": request.form.get('coach_lname').title(),
                    "nroc_level": request.form.get('nroc_level'),
                    "coach_email": request.form.get('coach_email'),
                    "coach_phone": request.form.get('coach_phone'),
                    "philosophy": philosophy.title(),
                    "imgurl": pf['url']
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


# students/skaters database listings
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
            'imgurl': 1
        })
    else:
        students = db.students.find()

    return render_template('list_students.template.html',
                           students=students)


# adding a new skater file - forms, validation and calc functions
@app.route('/students/new_skater')
def add_newskater():
    students = db.students.find()
    return render_template('form_newskater.template.html',
                           students=students,
                           errors={},
                           old_values={})


def validate_form_student(form):
    student_fname = form.get('student_fname')
    student_lname = form.get('student_lname')
    nation = form.get('nation')
    student_email = form.get('student_email')
    student_phone = form.get('student_phone')
    dob_day = form.get('dob_day')
    dob_month = form.get('dob_month')
    dob_year = form.get('dob_year')
    picfile = request.files['picfile']

    errors = {}

    if len(student_fname) == 0 or student_fname.isspace():
        errors['blank_fname'] = "Name field cannot be blank"

    if len(student_lname) == 0 or student_lname.isspace():
        errors['blank_lname'] = "Name field cannot be blank"

    if len(student_email) == 0 or student_email.isspace():
        errors['blank_email'] = "Email field cannot be blank"

    if len(student_phone) == 0 or student_phone.isspace():
        errors['blank_phone'] = "Phone field cannot be blank"

    if len(nation) == 0 or nation.isspace():
        errors['blank_nation'] = "Nationality field cannot be blank"

    if len(dob_day) == 0 or dob_day.isspace():
        errors['x_dobd'] = "Invalid entry"

    if len(dob_month) == 0 or dob_month.isspace():
        errors['x_dobm'] = "Invalid entry"

    if len(dob_year) == 0 or dob_year.isspace():
        errors['x_doby'] = "Invalid entry"

    if picfile.filename != "":
        pic = picfile.filename
        ft = ["jpg", "png", "gif", 'jpeg']
        x = []
        for i in ft:
            if pic.find(i) > 0:
                x.append(i)
        if x == []:
            errors["x_filetype"] = "Filetype .jpg .jpeg .png .gif only"

        picfile.seek(0, os.SEEK_END)
        file_size = picfile.tell()
        if file_size > 5 * 1024 * 1024:
            errors["file_xl"] = "File is too large"
        picfile.seek(0, 0)

    return errors


# conversion functions
def numtoalpha(form):
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


def alphatonum(form):
    m = request.form.get('dob_month')
    if m == "JAN":
        m = 1
    elif m == "FEB":
        m = 2
    elif m == "MAR":
        m = 3
    elif m == "APR":
        m = 4
    elif m == "MAY":
        m = 5
    elif m == "JUN":
        m = 6
    elif m == "JUL":
        m = 7
    elif m == "AUG":
        m = 8
    elif m == "SEP":
        m = 9
    elif m == "OCT":
        m = 10
    elif m == "NOV":
        m = 11
    elif m == "DEC":
        m = 12
    return m


# age calc functions
def cal_age(form):
    dob_day = form.get('dob_day')
    dob_month = form.get('dob_month')
    dob_year = form.get('dob_year')

    dob_str = dob_day + "-" + dob_month + "-" + dob_year
    dob_dt = datetime.datetime.strptime(dob_str, '%d-%m-%Y')

    today = date.today()
    today_str = today.strftime("%Y-%m-%d")
    cur_dt = datetime.datetime.strptime(today_str, '%Y-%m-%d')

    age_td = str(cur_dt - dob_dt)
    age_strip_time = age_td.rstrip('0:')
    age_days_str = str(age_strip_time.rstrip('days, '))
    age_days_int = int(age_days_str)
    age = int(age_days_int // 365.2425)

    return age


def cal_age_alpha(form):
    m_num = alphatonum(request.form)

    dob_day = form.get('dob_day')
    dob_month = str(m_num)
    dob_year = form.get('dob_year')

    dob_str = dob_day + "-" + dob_month + "-" + dob_year
    dob_dt = datetime.datetime.strptime(dob_str, '%d-%m-%Y')

    today = date.today()
    today_str = today.strftime("%Y-%m-%d")
    cur_dt = datetime.datetime.strptime(today_str, '%Y-%m-%d')

    age_td = str(cur_dt - dob_dt)
    age_strip_time = age_td.rstrip('0:')
    age_days_str = str(age_strip_time.rstrip('days, '))
    age_days_int = int(age_days_str)
    age = int(age_days_int // 365.2425)

    return age


@app.route('/students/new_skater', methods=["POST"])
def process_newskater():
    errors = validate_form_student(request.form)

    if len(errors) == 0:
        age = cal_age(request.form)

        dob_m = numtoalpha(request.form)

        picfile = request.files['picfile']
        if picfile.filename == "":
            avatar = os.environ['AVATAR']

            db.students.insert_one({
                "student_fname": request.form.get('student_fname').title(),
                "student_lname": request.form.get('student_lname').upper(),
                "skate_level": request.form.get('skate_level'),
                "nation": request.form.get('nation').upper(),
                "student_email": request.form.get('student_email'),
                "student_phone": "+65 " + request.form.get('student_phone'),
                "age": age,
                "date_of_birth": {
                    "dob_year": request.form.get('dob_year'),
                    "dob_month": dob_m,
                    "dob_day": request.form.get('dob_day')
                },
                "imgurl": avatar
            })
            flash("File for Skater CREATED")
            return redirect(url_for('students_list'))

        else:
            sfname = request.form.get('student_fname').lower()
            pf = cloudinary.uploader.upload(picfile.stream,
                                            public_id=sfname,
                                            folder='iifscdb/skater/',
                                            resource_type='image')

            db.students.insert_one({
                "student_fname": request.form.get('student_fname').title(),
                "student_lname": request.form.get('student_lname').upper(),
                "skate_level": request.form.get('skate_level'),
                "nation": request.form.get('nation').upper(),
                "student_email": request.form.get('student_email'),
                "student_phone": "+65 " + request.form.get('student_phone'),
                "age": age,
                "date_of_birth": {
                    "dob_year": request.form.get('dob_year'),
                    "dob_month": dob_m,
                    "dob_day": request.form.get('dob_day')
                },
                "imgurl": pf['url']
            })
            flash("File for Skater CREATED")
            return redirect(url_for('students_list'))
    else:
        all_sklvl = db.students.find()
        return render_template('form_newskater.template.html',
                               all_sklvl=all_sklvl,
                               errors=errors,
                               old_values=request.form)


# deleting a student entry form with confirmation alert
@app.route('/students/<student_id>/delete')
def del_skater(student_id):
    student_to_delete = db.students.find_one({
        '_id': ObjectId(student_id)
    })
    return render_template('del_alert_skater.template.html',
                           student_to_delete=student_to_delete)


@app.route('/students/<student_id>/delete', methods=["POST"])
def process_delete_skater(student_id):
    db.students.remove({
        '_id': ObjectId(student_id)
    })
    flash("File for Skater DELETED")
    return redirect(url_for('students_list'))


# updating a student/skater detail
@app.route('/students/<student_id>/update')
def update_skater(student_id):
    all_sklvl = db.students.find()
    student_to_edit = db.students.find_one({
        '_id': ObjectId(student_id)
    })
    return render_template('update_skater.template.html',
                           old_values=student_to_edit,
                           all_sklvl=all_sklvl,
                           errors={})


@app.route('/students/<student_id>/update', methods=["POST"])
def process_update_skater(student_id):
    errors = validate_form_student(request.form)

    if len(errors) == 0:

        age = cal_age_alpha(request.form)

        picfile = request.files['picfile']
        if picfile.filename == "":
            avatar = os.environ['AVATAR']

            db.students.update_one({
                '_id': ObjectId(student_id)
            }, {
                '$set': {
                    "student_fname": request.form.get('student_fname').title(),
                    "student_lname": request.form.get('student_lname').upper(),
                    "skate_level": request.form.get('skate_level'),
                    "nation": request.form.get('nation').upper(),
                    "student_email": request.form.get('student_email'),
                    "student_phone": request.form.get('student_phone'),
                    "age": age,
                    "date_of_birth": {
                        "dob_year": request.form.get('dob_year'),
                        "dob_month": request.form.get('dob_month'),
                        "dob_day": request.form.get('dob_day'),
                    },
                    "imgurl": avatar
                }
            })
            flash("File for Skater UPDATED")
            return redirect(url_for('students_list'))
        else:
            sfname = request.form.get('student_fname').lower()
            pf = cloudinary.uploader.upload(picfile.stream,
                                            public_id=sfname,
                                            folder='iifscdb/skater/',
                                            resource_type='image')
            db.students.update_one({
                '_id': ObjectId(student_id)
            }, {
                '$set': {
                    "student_fname": request.form.get('student_fname').title(),
                    "student_lname": request.form.get('student_lname').upper(),
                    "skate_level": request.form.get('skate_level'),
                    "nation": request.form.get('nation').upper(),
                    "student_email": request.form.get('student_email'),
                    "student_phone": request.form.get('student_phone'),
                    "age": age,
                    "date_of_birth": {
                        "dob_year": request.form.get('dob_year'),
                        "dob_month": request.form.get('dob_month'),
                        "dob_day": request.form.get('dob_day'),
                    },
                    "imgurl": pf['url']
                }
            })
            flash("File for Skater UPDATED")
            return redirect(url_for('students_list'))
    else:
        all_sklvl = db.students.find()
        student_to_edit = db.students.find_one({
            '_id': ObjectId(student_id)
        })
        old_values = {**student_to_edit, **request.form}
        return render_template('update_skater.template.html',
                               old_values=old_values,
                               all_sklvl=all_sklvl,
                               errors=errors)


# detailed individual student profile
@app.route('/students/<student_id>/skater_profile')
def skater_profile(student_id):
    skater = db.students.find_one({
        '_id': ObjectId(student_id)
    })

    return render_template('profile_skater.template.html',
                           skater=skater)


# forms & routes for competition data - student nested /embed object
@app.route('/students/<student_id>/skater_profile/new_competition')
def add_comp(student_id):
    skater = db.students.find_one({
        '_id': ObjectId(student_id)
    })
    old_values = {**{}, **skater}
    return render_template('form_newcomp.template.html',
                           old_values=old_values,
                           errors={})


def validate_form_comp(form):
    comp_year = form.get('comp_year')
    comp_title = form.get('comp_title')
    base = form.get('comp_base')
    tes = form.get('comp_tes')
    pcs = form.get('comp_pcs')

    errors = {}

    if len(comp_year) == 0:
        errors['blank_cyear'] = "Year field cannot be blank"

    if len(comp_title) == 0:
        errors['blank_ctitle'] = "Title field cannot be blank"

    if len(base) == 0:
        errors['blank_cbase'] = "Invalid value"

    if len(tes) == 0:
        errors['blank_ctes'] = "Invalid value"

    if len(pcs) == 0:
        errors['blank_cpcs'] = "Invalid value"

    return errors


def cal_tss(form):
    tes = float(form.get("comp_tes"))
    pcs = float(form.get("comp_pcs"))
    tss = round((tes + pcs), 2)
    return tss


@app.route('/students/<student_id>/skater_profile/new_competition',
           methods=["POST"])
def process_add_comp(student_id):
    errors = validate_form_comp(request.form)

    if len(errors) == 0:

        tss = cal_tss(request.form)

        db.students.update_one({
            '_id': ObjectId(student_id)
        }, {
            "$push": {
                "competition_data": {
                    "comp_id": ObjectId(),
                    "comp_year": request.form.get("comp_year"),
                    "comp_title": request.form.get("comp_title").title(),
                    "category": request.form.get("comp_category"),
                    "sequence": {
                        "seq1": request.form.get("comp_seq1"),
                        "seq2": request.form.get("comp_seq2"),
                        "seq3": request.form.get("comp_seq3"),
                        "seq4": request.form.get("comp_seq4"),
                        "seq5": request.form.get("comp_seq5"),
                        "seq6": request.form.get("comp_seq6"),
                        "seq7": request.form.get("comp_seq7"),
                        "seq8": request.form.get("comp_seq8"),
                        "seq9": request.form.get("comp_seq9"),
                        "seq10": request.form.get("comp_seq10"),
                        "seq11": request.form.get("comp_seq11"),
                        "seq12": request.form.get("comp_seq12"),
                    },
                    "base_value": float(request.form.get("comp_base")),
                    "TES": float(request.form.get("comp_tes")),
                    "PCS": float(request.form.get("comp_pcs")),
                    "TSS": tss
                }
            }
        })
        flash("File for Skater UPDATED")
        return redirect(url_for('skater_profile',
                                student_id=student_id))
    else:
        all_skater = db.students.find()
        skater = db.students.find_one({
            '_id': ObjectId(student_id)
        })
        old_values = {**request.form, **skater}
        return render_template('form_newcomp.template.html',
                               all_skater=all_skater,
                               errors=errors,
                               old_values=old_values)


# updating competition data for skaters
@app.route('/students/<student_id>/<comp_id>/update')
def update_competition(student_id, comp_id):
    skate_comp = db.students.find_one({
        'competition_data.comp_id': ObjectId(comp_id)
    }, {
        'student_lname': 1,
        'student_fname': 1,
        'competition_data.$': 1,
    })
    old_values = {**skate_comp}
    return render_template('update_comp.template.html',
                           old_values=old_values,
                           errors={})


@app.route('/students/<student_id>/<comp_id>/update',
           methods=["POST"])
def process_update_competition(student_id, comp_id):
    errors = validate_form_comp(request.form)

    if len(errors) == 0:

        tss = cal_tss(request.form)

        db.students.update_one({
            '_id': ObjectId(student_id),
            'competition_data.comp_id': ObjectId(comp_id)
        }, {
            "$set": {
                "competition_data.$.comp_year": request.form.get("comp_year"),
                "competition_data.$.comp_title":
                request.form.get("comp_title").title(),
                "competition_data.$.category":
                request.form.get("comp_category"),
                "competition_data.$.sequence": {
                    "seq1": request.form.get("comp_seq1"),
                    "seq2": request.form.get("comp_seq2"),
                    "seq3": request.form.get("comp_seq3"),
                    "seq4": request.form.get("comp_seq4"),
                    "seq5": request.form.get("comp_seq5"),
                    "seq6": request.form.get("comp_seq6"),
                    "seq7": request.form.get("comp_seq7"),
                    "seq8": request.form.get("comp_seq8"),
                    "seq9": request.form.get("comp_seq9"),
                    "seq10": request.form.get("comp_seq10"),
                    "seq11": request.form.get("comp_seq11"),
                    "seq12": request.form.get("comp_seq12"),
                },
                "competition_data.$.base_value":
                float(request.form.get("comp_base")),
                "competition_data.$.TES": float(request.form.get("comp_tes")),
                "competition_data.$.PCS": float(request.form.get("comp_pcs")),
                "competition_data.$.TSS": tss
            }
        })
        flash("File for Skater UPDATED")
        return redirect(url_for('skater_profile',
                                student_id=student_id))
    else:
        skate_comp = db.students.find_one({
            'competition_data.comp_id': ObjectId(comp_id)
        }, {
            'student_lname': 1,
            'student_fname': 1,
            'competition_data.$': 1,
        })
    old_values = {**skate_comp, **request.form}
    return render_template('update_comp.template.html',
                           old_values=old_values,
                           errors=errors)


# deleting competition data from skater
@app.route('/students/<student_id>/skater_profile/<comp_id>/delete')
def del_competition(student_id, comp_id):
    db.students.update_one({
        "competition_data.comp_id": ObjectId(comp_id)
    }, {
        '$pull': {
            'competition_data': {
                'comp_id': ObjectId(comp_id)
            }
        }
    })
    flash('Competition Data DELETED')
    return redirect(url_for('skater_profile', student_id=student_id))


# request lesson with coach
@app.route('/coaches/<coach_id>/request')
def request_lesson(coach_id):
    coach_rl = db.coaches.find_one({
        '_id': ObjectId(coach_id)
    })

    return render_template('form_reqlesson.template.html',
                           coachrl=coach_rl,
                           errors={},
                           old_values={})


# validation of lesson request form
def validate_form_reqclass(form):
    student_fname = form.get('student_fname').title()
    student_lname = form.get('student_lname').upper()
    rl_day = form.get('rl_day')
    rl_month = form.get('rl_month')
    rl_year = form.get('rl_year')
    rl_timeh = form.get('rl_timeh')
    rl_timem = form.get('rl_timem')

    errors = {}

    if len(student_fname) == 0:
        errors['blank_fname'] = "Name field cannot be blank"

    if len(student_lname) == 0:
        errors['blank_lname'] = "Name field cannot be blank"

    if len(student_fname) > 0 and len(student_lname) > 0:
        criteria = {}
        if (student_fname):
            criteria['student_fname'] = {
                '$eq': student_fname,
            }
        if (student_lname):
            criteria['student_lname'] = {
                '$eq': student_lname,
            }
        sk8er = db.students.find_one(criteria, {
            '_id': 1
        })
        if sk8er is None:
            errors['xdb'] = "Student is not in Database, Please Register first"

    if len(rl_day) == 0:
        errors['dtd'] = "Invalid entry"

    if len(rl_month) == 0:
        errors['dtm'] = "Invalid entry"

    if len(rl_year) == 0:
        errors['dty'] = "Invalid entry"

    if len(rl_timeh) == 0:
        errors['dtth'] = "Time session is required"

    if len(rl_timem) == 0:
        errors['dttm'] = "Time session is required"

    if len(rl_year) > 0 and (len(rl_day) > 0 and len(rl_month) > 0):
        cur_dt = datetime.datetime.today() + timedelta(hours=8)
        # timedelta(hours=8) = UTC + 8 for singapore local datetime
        if (int(rl_day) >= 1
            and int(rl_month) >= 1) and (len(rl_timeh) > 0
                                         and len(rl_timem) > 0):
            input_dtstr = rl_year + "-" + rl_month + "-" + \
                rl_day + "-" + rl_timeh + "-" + rl_timem
            input_dt = datetime.datetime.strptime(
                input_dtstr, '%Y-%m-%d-%H-%M')
            if input_dt.strftime("%m") < cur_dt.strftime("%m"):
                errors['dtxm'] = "48hours notice required"
            if input_dt < cur_dt + timedelta(hours=48):
                errors['dtxd'] = "48hours notice required"
        else:
            input_dstr = rl_year + "-" + rl_month + "-" + rl_day
            input_d = datetime.datetime.strptime(input_dstr, '%Y-%m-%d')
            if input_d.strftime("%m") < cur_dt.strftime("%m"):
                errors['dtxm'] = "48hours notice required"
            if input_d < cur_dt + timedelta(hours=48):
                errors['dtxd'] = "48hours notice required"

    return errors


def get_skater_id(form):
    rl_sfname = request.form.get('student_fname')
    rl_slname = request.form.get('student_lname')

    criteria = {}

    if (rl_sfname):
        criteria['student_fname'] = {
            '$regex': rl_sfname, '$options': 'i'
        }
    if (rl_slname):
        criteria['student_lname'] = {
            '$regex': rl_slname, '$options': 'i'
        }

    sk8er = db.students.find_one(criteria, {
        '_id': 1
    })

    student_id = sk8er.get('_id')
    return student_id


@app.route('/coaches/<coach_id>/request', methods=["POST"])
def post_reqlesson(coach_id):

    errors = validate_form_reqclass(request.form)

    if len(errors) == 0:

        student_id = get_skater_id(request.form)

        rl_day = request.form.get('rl_day')
        rl_month = request.form.get('rl_month')
        rl_year = request.form.get('rl_year')
        rl_timeh = request.form.get('rl_timeh')
        rl_timem = request.form.get('rl_timem')

        req_dt = rl_year + "-" + rl_month + "-" + \
            rl_day + " " + rl_timeh + ":" + rl_timem
        rl_datetime = datetime.datetime.strptime(req_dt, '%Y-%m-%d %H:%M')

        timestamp = datetime.datetime.now() + timedelta(hours=8)

        db.schedule.insert_one({
            "_id": ObjectId(),
            "datetime": rl_datetime,
            "duration": request.form.get('rl_duration'),
            "location": request.form.get('rl_loc'),
            "ice_type": request.form.get('rl_icetype'),
            "coach_id": ObjectId(coach_id),
            "student_id": ObjectId(student_id),
            "timestamp": timestamp
        })
        flash("Lesson Request Accepted for Processing")
        return redirect(url_for('index'))
    else:
        coach_rl = db.coaches.find_one({
            '_id': ObjectId(coach_id)
        })

        old_values = {**request.form}
        return render_template('form_reqlesson.template.html',
                               coachrl=coach_rl,
                               errors=errors,
                               old_values=old_values)


# view lesson requests
@app.route('/schedule/requests')
def lesson():
    reqloc = request.args.get('location')
    reqice = request.args.get('ice_type')
    criteria = {}

    if reqloc:
        criteria['location'] = {
            '$regex': reqloc, '$options': 'i'
        }
    if reqice:
        criteria['ice_type'] = {
            '$regex': reqice, '$options': 'i'
        }
    lesson = db.schedule.find(criteria, {
        '_id': 1,
        'coach_id': 1,
        'ice_type': 1,
        'datetime': 1,
        'duration': 1,
        'location': 1,
        'student_id': 1,
        'timestamp': 1
    })

    return render_template('schedule.template.html',
                           lesson=lesson)


@app.route('/schedule/<lesson_id>/<coach_id>+<student_id>/process')
def process_lesson(lesson_id, coach_id, student_id):
    lesson = db.schedule.find_one({
        '_id': ObjectId(lesson_id)
    })
    coach = db.coaches.find_one({
        '_id': ObjectId(coach_id)
    })
    student = db.students.find_one({
        '_id': ObjectId(student_id)
    })
    return render_template('process_lesson.template.html',
                           lesson=lesson,
                           coach=coach,
                           student=student)


@app.route('/schedule/<lesson_id>/delete')
def del_lesson(lesson_id):
    db.schedule.remove({
        '_id': ObjectId(lesson_id)
    })
    flash("Lesson Request DELETED")
    return redirect(url_for('lesson'))


@app.errorhandler(413)
def request_entity_too_large(error):
    flash("File TOO Large, connection reset, 413")
    return redirect(url_for('index'))


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=8080,
            debug=False)
