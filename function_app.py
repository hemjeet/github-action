import azure.functions as func
import logging
from joblib import *
import json
import pandas as pd 
app = func.FunctionApp(http_auth_level = func.AuthLevel.ANONYMOUS)


#---------load model--------#
model = load('model.pkl')
logging.info('Model loaded successfully !')

@app.route(route = "http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()
    df = pd.DataFrame.from_dict(req_body, orient= 'index').T
    try:
        pred = model.predict(df)[0]
        logging.info('Model predicted !!')

        dict_ = {"Prediction": ''}
        
        if pred == 0:
            dict_['Prediction'] = 'Useful'
        else:
            dict_['Prediction'] = 'Not useful'

        response = json.dumps(dict_)
        logging.info('Response created !!')
        return func.HttpResponse(response, status_code= 200)
    except:
        return func.HttpResponse('Some error occured !')