from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
import pickle
import pandas as pd
from os import environ

app = Flask(__name__)
model = pickle.load(open("clf.pkl", "rb"))


app.static_folder = 'static'
@app.route("/")
@cross_origin()
def home():
    return render_template("home.html")




@app.route("/predict", methods = ["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":


        # step
        step = int(request.form["step"])
        # print("step : ",step)

        # type
        type = request.form["type"]
        if type=='Transfer':
            type=1
        elif type=='Cash Out':
            type=0
        # print("type : ",type)

        # amount
        amount = float(request.form["amount"])
        # print("amount : ",amount)

        # oldbalanceOrg
        oldbalanceOrg = float(request.form["oldbalanceOrg"])
        # print("oldbalanceOrg : ",oldbalanceOrg)

        # newbalanceOrig
        newbalanceOrig = float(request.form["newbalanceOrig"])
        # print("newbalanceOrig : ",newbalanceOrig)

        # nameDest
        nameDest = request.form["nameDest"]
        if nameDest=='Merchant':
            nameDest=1
        elif nameDest=='Customer':
            nameDest=0
        else:
            nameDest=0
        # print("nameDest : ",nameDest)

        # oldbalanceDest
        oldbalanceDest = float(request.form["oldbalanceDest"])
        # print("oldbalanceDest : ",oldbalanceDest)

        # newbalanceDest
        newbalanceDest = float(request.form["newbalanceDest"])
        # print("newbalanceDest : ",newbalanceDest)

        # isFlagged
        isFlagged = request.form["isFlagged"]
        if isFlagged=='Yes':
            isFlagged=1
        elif isFlagged=='No':
            isFlagged=0
        else:
            isFlagged=0
        # print("isFlagged : ",isFlagged)
        # step=1
        # type=1
        # amount=181.0
        # oldbalanceOrg=181.0
        # newbalanceOrig=0.0
        # nameDest=0
        # oldbalanceDest=21182.0
        # newbalanceDest=0.0
        # isFlagged=0


        prediction = model.predict([[int(step), int(type), float(amount), float(oldbalanceOrg), float(newbalanceOrig), int(nameDest), float(oldbalanceDest), float(newbalanceDest), int(isFlagged)]])


        output=prediction[0]
        print(step,type,amount,oldbalanceOrg,newbalanceOrig,nameDest,oldbalanceDest,newbalanceDest,isFlagged)
        print(output)
        if output==1:
            return render_template('home.html', prediction_text="The transaction is fraudulent")
        else:
            return render_template('home.html', prediction_text="The transaction is not fraudulent")
        #return render_template('home.html',prediction_text="Your Flight price is Rs. {}".format(output))


    return render_template("home.html")




if __name__ == "__main__":
    app.run(debug = True, host = '0.0.0.0', port=environ.get("PORT", 5000))