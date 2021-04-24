import os
import pickle5 as pickle
import sqlite3
import pandas as pd
from lightgbm import LGBMClassifier
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
    model = pickle.load(open(os.path.join(app.root_path,'credit.pkl'), 'rb'))
    con = sqlite3.connect('project/site.db')
    query = f"SELECT * FROM credit2 WHERE SK_ID_CURR = '{customer_id}'"
    df = pd.read_sql_query(query, con)
    df.drop(['TARGET', 'SK_ID_CURR', 'index'], axis=1, inplace=True)
    con.close()
    object_cols = [col for col in df.columns if df[col].dtype == 'object']
    for col in object_cols:
        df[col]=df[col].astype(float)

    prediction = model.predict_proba(df.values)
    risk,norisk =round(prediction[0][0]*100,2),round(prediction[0][1]*100,2)
    labels = ['Risk', 'No Risk']
    values = [risk, norisk]
    colors = ["#009688", "#F7464A"]

    customer_id= customer_id
    age= round(df["NEW_APP_AGE"][0])
    child= round(df["CNT_CHILDREN"][0])
    if round(df["CODE_GENDER"][0])==1:
        gender = "Male"
    else:
        gender = "Female"
    if round(df["FLAG_OWN_REALTY"][0])==1:
        estate = "Yes"
    else:
        estate = "No"
    if round(df["FLAG_OWN_CAR"][0])==1:
        car = "Yes"
    else:
        car = "No"
        
    return render_template('credit_result.html',set=zip(values, labels, colors),
    age=age,gender=gender,child=child, estate=estate,car=car,customer_id=customer_id)


