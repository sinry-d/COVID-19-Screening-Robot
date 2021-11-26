from flask import Flask, render_template
import functions
import main

app = Flask(__name__)

headings = ("Visitor Index", "Face mask", "Wrist Temperature", "Allowed Entry")
data = []

@app.route('/')

def table():
    dataItem = functions.addData()

    data.append(dataItem)

    return render_template("table.html", headings=headings, data=data)