import azure.functions as func
import logging
from joblib import *
import pandas as pd 
app = func.FunctionApp(http_auth_level = func.AuthLevel.ANONYMOUS)


#---------load model--------#
model =load('model.pkl')

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()

    logging.info('Loading model')
    df = pd.DataFrame.from_dict(req_body, orient= 'index').T
    pred = model.predict(df)[0]

    response = {"Prediction": str(pred)}
    return func.HttpResponse(response, status_code= 200)