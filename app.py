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
                           coaches=coaches, old_values={}, errors={})


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
    return render_template('alert_del_coach.template.html',
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


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=8080,
            debug=True)
