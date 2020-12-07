# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 16:56:02 2020

@author: AGUZ
"""

import pickle as pkl
import pandas as pd
from flask import Flask,request
import flasgger
from flasgger import Swagger
from sklearn.preprocessing import StandardScaler

# reading the model from the file
fp = open("model.pkl","rb")
model = pkl.load(fp)

#creating api , format of flask api
app = Flask(__name__)
Swagger(app)

#Creating a route with home page to check wheather the address and port of local host working correctly or not
@app.route('/')
def welcome():   
    return "WELCOME USER---type /apidocs for the swagger page where you can enter the data"

# Creating a get request for collecting parametrs one by one for checking the "CHURN_FLAG" of a single 

#creating Query set for running the swagger inide the flasgger
@app.route('/predict',methods = ["Get"])
def predict():    
    """PREDICTS THE CHURN_FLAG of a customer
    NO_CHURN_Company 
    prediction for single customer.
    ---
    parameters:
        - name: International_Plan
          in: query
          type: float
          required : false     
        - name: VMail_Plan
          in: query
          type: float
          required : false         
        - name: Day_Mins
          in: query
          type: float
          required : false         
        - name: Eve_Mins
          in: query
          type: float
          required : false          
        - name: Night_Mins
          in: query
          type: float
          required : false
        - name: International_Mins
          in: query
          type: float
          required : false        
        - name: International_calls
          in: query
          type: float
          required : false         
        - name: CustServ_Calls
          in: query
          type: float
          required : false
    responses:
        200:
            description: Output values
    """
    #loading all parameter values that are received using the get request and loaded into separate variables
    
    International_Plan = request.args.get("International_Plan")
    VMail_Plan = request.args.get("VMail_Plan")
    Day_Mins = request.args.get("Day_Mins")
    Eve_Mins = request.args.get("Eve_Mins")
    Night_Mins = request.args.get("Night_Mins")
    International_Mins = request.args.get("International_Mins")
    International_calls = request.args.get("International_calls")
    CustServ_Calls = request.args.get("CustServ_Calls")
    
    #creating a parameter list which contains all the parametrs
    parameters = [International_Plan,VMail_Plan,Day_Mins,Eve_Mins,Night_Mins,International_Mins,International_calls,CustServ_Calls]
    
    
    #running a for loop to check all the parametrs are entered or not
    for x,i in enumerate(parameters):
        if i == None:
            return " you didn't enter the value for some parameters."
        
    #checking with model and returning the output on screen   
    prediction1 = model.predict([parameters])
    return "predicteded value is : " + str(prediction1)

#here we are using post method for collecting the file adress
@app.route('/predict_file',methods = ['POST'])
def predict_file():
    """PREDICT THE CHURN_FLAG OF SOME CUSTOMER DATASET
    NO_CHURN_COMPANY 
    prediction for a listof customers
    ---
    parameters:
        - name: FILE_NAME
          in: formData
          type: file
          required: true
          
    responses:
        200:
            description: Output values
    
    """
    
    data = pd.read_csv(request.files.get('FILE_NAME'))
    data_scaled =StandardScaler().fit_transform(data) 
    prediction2 = model.predict(data_scaled)
    prediction3 = pd.DataFrame(prediction2.astype(int),columns=["CHURN_FLAG"])
    #pd.concat([data,prediction3],axis=1).to_csv("test_data_out",index=False)
    return "predicteded 'CHURN_FLAG' for the input file is : " + str(prediction2.astype(int))

#-> reading the data set,sciling the dataset,predicting the "CHURN_FLAG" ,printing the CHURN_FLAG in flasgger,saving the dataset with CHURN_FLAG as "test_data_out"

if __name__ == "__main__":
    app.run()
