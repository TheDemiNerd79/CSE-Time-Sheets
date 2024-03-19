from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
from datetime import date
from math import *

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        st = request.form.get('st').split(':')
        bst = request.form.get('bst').split(':')
        bet = request.form.get('bet').split(':')
        et = request.form.get('et').split(':')
        breakmins = int(bet[1]) - int(bst[1])
        breakhrs = int(bet[0]) - int(bst[0])
        workmins = int(et[1]) - int(st[1])
        workhrs = int(et[0]) - int(st[0])
        totalhrs = workhrs - breakhrs
        totalmins = workmins - breakmins
        if totalmins < 0:
            totalhrs = floor(totalhrs + (totalmins/60))
            totalmins = round(60 - (breakmins))
        if len(str(totalmins)) < 2:
            totalmins = f"0{totalmins}"
        if len(str(breakmins)) < 2:
            breakmins = f"0{breakmins}"
        total = f"{totalhrs}:{totalmins}"
        new_note = Note(data=f"{date.today()}: Start: {request.form.get('st')}, Break: {request.form.get('bst')}, to: "
                             f"{request.form.get('bet')}, End: {request.form.get('et')}, Time worked: {total}, "
                             f"Break Time: {breakhrs}:{breakmins}",
                        user_id=current_user.id, timeworked=((totalhrs / 60) + totalmins))
        db.session.add(new_note)
        db.session.commit()

        flash('Time clocked!', category='success')
    print(date.today())
    total = [0, 0]
    for note in current_user.notes:
        total[0] += note_hours
        total[1] += note_minutes

    return render_template("home.html", user=current_user, day=date.today(), total=f"{total[0]}:{total[1]}")


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})