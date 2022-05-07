from flask import Flask, jsonify,request
from flask_restful import Resource, Api
import pickle
import pandas as pd
from flask_cors import CORS
from utils import *
import numpy as np
import xgboost as xgb


app = Flask(__name__)
#
CORS(app)
# creating an API object
api = Api(app)

#prediction api call
class prediction(Resource):
    def post(self):
        cust=request.get_json('Data')
        
        x_vars_list = readData(cust)
        
        #load model and save predictions
        model = pickle.load(open('model.pkl', 'rb'))
        test_X = np.array(x_vars_list)
        xgtest = xgb.DMatrix(test_X)
        preds = model.predict(xgtest)

        #initialize output values
        target_cols = ['Saving Account','Guarantees','Current Account','Derivada Account','Payroll Account','Junior Account','Mas particular Account','particular Account','particular Plus Account','Short-term Deposits','Medium-term Deposits','Long-term Deposits','e-account','Funds','Mortgage','Pensions','Loans','Taxes','Credit Card','Securities','Home Account','Payroll','Pensions','Direct Debit']
        target_cols = target_cols[2:]
        target_cols = np.array(target_cols)

        #map predictions to values
        preds = np.argsort(preds, axis=1)
        preds = np.fliplr(preds)[:,:7]
        
        final_preds = [", ".join(list(target_cols[pred])) for pred in preds]
        out_df = jsonify(final_preds)
    
        return out_df



api.add_resource(prediction, '/prediction/')

if __name__ == '__main__':
    app.run("0.0.0.0",debug=True)

