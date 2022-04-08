from flask import Blueprint, render_template, request, flash, jsonify, json
from flask_login import login_user, logout_user, login_required, current_user
from .models import Note
from . import db

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def Home():
    notes = Note.query.filter_by(user_id=current_user.id).all()
    print(notes)
    if request.method == 'POST':
        note = request.form['note']

        if len(note) < 1:
            flash('Please enter a note.', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added.', category='success')

    return render_template("home.html", user=current_user, notes=notes)


@views.route('/delete-note', methods=['POST'])
def DeleteNote():
    note = json.loads(request.data)
    note_id = note['noteId']
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({})