from os import error
from werkzeug.wrappers import response
from app import app
from flask import render_template, request, flash


from app.modules.base_analyzer import BaseAnalyzer

@app.route("/")
def index():
    kwargs = request.args
    print(kwargs)
    if not kwargs:
        return render_template("index.html")
    ba = BaseAnalyzer(**kwargs)
    report = ba.get_report()
    print(report)
    if report["status"] == "error":
        flash(report["info"], "error")
        return render_template("index.html")
    
    return render_template("index.html", report=report)