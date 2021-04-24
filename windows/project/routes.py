import os
import sqlite3
import pandas as pd
from flask import render_template, url_for, flash, redirect
from project import app, db
from project.forms import CreditForm


@app.route("/", methods=['GET', 'POST'])
def credit():
    
    form = CreditForm()
    if form.validate_on_submit():
        if form.customer_id.data:
            if form.customer_id.data >300:
                flash("Customer ID range is between 1-300", "warning")
                return redirect(url_for('credit'))
            return redirect(url_for('credit_result', customer_id=form.customer_id.data))
    return render_template('credit.html',form=form)


@app.route("/<customer_id>", methods=['GET', 'POST'])
def credit_result(customer_id):
    con = sqlite3.connect('project\\site.db')
    query = f"SELECT * FROM result WHERE customer_id = '{customer_id}'"
    df = pd.read_sql_query(query, con)
    con.close()
    norisk,risk =round(df.values[0][1]*100,2),round(df.values[0][2]*100,2)
    labels = ['No Risk','Risk']
    values = [risk, norisk]
    colors = ["#F7464A","#009688" ]
        
    return render_template('credit_result.html',set=zip(values, labels, colors))


