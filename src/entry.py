from azureml.core import Model
from azureml.contrib.services.aml_request import AMLRequest, rawhttp
from azureml.contrib.services.aml_response import AMLResponse
import joblib
import numpy as np
import json

def init():
    global model
    model_path = Model.get_model_path("moa_prediction_model")
    print("Model Path is  ", model_path)
    model = joblib.load(model_path)

@rawhttp
def run(request):
  if request.method == 'POST':
        try:
            data = np.expand_dims(np.array(request.json['data']), axis=0)
            yres = model.predict(data)
            response = {'data' : yres.tolist() , 'message' : "Successfully  classified"}
            return AMLResponse(json.dumps(response), 200)
        except Exception as e:
            print(e)
            return AMLResponse("Server error", 500)
  else:
      return AMLResponse("Unsopported method", 405)
