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

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
            df = pd.DataFrame.from_dict(req_body, orient= 'index').T
            pred = model.predict(df)[0]

            return func.HttpResponse(str(pred), status_code = 200)

        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )