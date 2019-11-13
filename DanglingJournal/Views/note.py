#  Project dangling-journal is developed by "Fahad Ahammed" on 11/12/19, 9:29 PM.
#
#  Last modified at 11/12/19, 9:29 PM.
#
#  Github: fahadahammed
#  Email: obak.krondon@gmail.com
#
#  Copyright (c) 2019. All rights reserved.

from flask import request, render_template, url_for
from flask import redirect, abort, jsonify

from DanglingJournal import app
from DanglingJournal.Model.note import Note


@app.route("/api/note/list", methods=["GET"])
def api_note_list():
    if request.method == "GET":
        to_return = Note().list_of_notes()
        if to_return:
            return jsonify(to_return)
        else:
            return abort(400)


@app.route("/api/note/all", methods=["GET"])
def api_note_all():
    if request.method == "GET":
        to_return = Note().get_all_notes()
        if to_return:
            return jsonify(to_return[0:10])
        else:
            return abort(400)


@app.route("/api/note/<int:note_id>", methods=["GET"])
def api_note_single(note_id):
    if request.method == "GET":
        to_return = Note().get_single_note(note_id=note_id)
        if to_return:
            return jsonify(to_return)
        else:
            return abort(400)


@app.route("/api/note/<int:note_id>", methods=["PUT"])
def api_note_single_edit(note_id):
    if request.method == "PUT":
        to_return = Note().update_note(note_id=note_id, data_json=request.json)
        if to_return:
            return jsonify(to_return)
        else:
            return abort(400)


@app.route("/api/note/<int:note_id>", methods=["DELETE"])
def api_note_single_delete(note_id):
    if request.method == "DELETE":
        to_return = Note().delete_single_note(note_id=note_id)
        if to_return:
            return jsonify(to_return)
        else:
            return abort(400)


@app.route("/api/note", methods=["POST"])
def api_store_note():
    if request.method == "POST":
        to_return = Note().store_note(data_json=request.json)
        if to_return:
            return jsonify(to_return)
        else:
            return abort(400)