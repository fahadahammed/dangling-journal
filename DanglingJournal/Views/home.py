#  Project dangling-journal is developed by "Fahad Ahammed" on 11/12/19, 5:36 PM.
# 
#  Last modified at 11/12/19, 5:34 PM.
# 
#  Github: fahadahammed
#  Email: obak.krondon@gmail.com
# 
#  Copyright (c) 2019. All rights reserved.

# -----------------------------
#
# Project: DanglingJournal
# Version: 2019-11-12_17-34-11
#
# Date: Tue Nov 12 17:34:27 +06 2019
# Created By: Fahad Ahammed
#
# -----------------------------
from flask import request, render_template, url_for
from flask import redirect, session, jsonify

from DanglingJournal import app



@app.route("/", methods=["GET"])
def home():
    if request.method == "GET":
        to_return = {
                "msg": "Welcome to DanglingJournal !!!"
        }
        return jsonify(to_return)
