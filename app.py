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
    return render_template('form_newcoach.template.html')


@app.route('/coaches/new_coach', methods=["POST"])
def process_newcoach():
    coach_fname = request.form.get('coach_fname')
    coach_lname = request.form.get('coach_lname')
    nroc_level = request.form.get('nroc_level')
    coach_email = request.form.get('coach_email')
    coach_phone = request.form.get('coach_phone')
    philosophy = request.form.get('philosophy')

    db.coaches.insert_one({
        "_id": ObjectId(),
        "coach_fname": coach_fname,
        "coach_lname": coach_lname,
        "nroc_level": nroc_level,
        "coach_email": coach_email,
        "coach_phone": coach_phone,
        "philosophy": philosophy
    })
    flash("File for Coach CREATED")
    return redirect(url_for('coaches_list'))


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
    coach_to_edit = db.coaches.find_one({
        '_id': ObjectId(coach_id)
    })
    return render_template('update_coach.template.html',
                           coach_to_edit=coach_to_edit)


@app.route('/coaches/<coach_id>/update', methods=['POST'])
def process_update_coach(coach_id):
    db.coaches.update_one({
        '_id': ObjectId(coach_id)
    }, {
        '$set': request.form
    })
    flash("File for Coach UPDATED")
    return redirect(url_for('coaches_list'))


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=8080,
            debug=True)
