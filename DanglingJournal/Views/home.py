#  Project dangling-journal is developed by "Fahad Ahammed" on 11/12/19, 5:36 PM.
# 
#  Last modified at 11/12/19, 5:34 PM.
# 
#  Github: fahadahammed
#  Email: obak.krondon@gmail.com
# 
#  Copyright (c) 2019. All rights reserved.


from flask import request, render_template, url_for
from flask import redirect, session, jsonify

from DanglingJournal import app


@app.route("/api/", methods=["GET"])
def home():
    if request.method == "GET":
        to_return = {
                "msg": "Welcome to DanglingJournal !!!"
        }
        return jsonify(to_return)
