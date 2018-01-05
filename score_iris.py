# This script generates the scoring and schema files
# Creates the schema, and holds the init and run functions needed to 
# operationalize the Iris Classification sample

# Import data collection library. Only supported for docker mode.
# Functionality will be ignored when package isn't found
try:
    from azureml.datacollector import ModelDataCollector
except ImportError:
    print("Data collection is currently only supported in docker mode. May be disabled for local mode.")
    # Mocking out model data collector functionality
    class ModelDataCollector(object):
        def nop(*args, **kw): pass
        def __getattr__(self, _): return self.nop
        def __init__(self, *args, **kw): return None
    pass

import os

# Prepare the web service definition by authoring
# init() and run() functions. Test the functions
# before deploying the web service.
def init():
    global inputs_dc, prediction_dc
    from sklearn.externals import joblib

    # load the model file
    global model
    model = joblib.load('model.pkl')

    inputs_dc = ModelDataCollector("model.pkl", identifier="inputs")
    prediction_dc = ModelDataCollector("model.pkl", identifier="prediction")

def run(input_df):
    import json
    
    # append 40 random features just like the training script does it.
    import numpy as np
    n = 40
    random_state = np.random.RandomState(0)
    n_samples, n_features = input_df.shape
    input_df = np.c_[input_df, random_state.randn(n_samples, n)]
    inputs_dc.collect(input_df)

    pred = model.predict(input_df)
    prediction_dc.collect(pred)
    return json.dumps(str(pred[0]))

def score(sepallength, sepalwidth, petallength, petalwidth):
  from azureml.api.schema.dataTypes import DataTypes
  from azureml.api.schema.sampleDefinition import SampleDefinition
  from azureml.api.realtime.services import generate_schema
  import pandas
  
  df = pandas.DataFrame(data=[[sepallength, sepalwidth, petallength, petalwidth]], columns=['sepal length', 'sepal width','petal length','petal width'])

  # Turn on data collection debug mode to view output in stdout
  os.environ["AML_MODEL_DC_DEBUG"] = 'true'

  # Test the output of the functions
  init()
  input1 = pandas.DataFrame([[sepallength, sepalwidth, petallength, petalwidth]])
  res = run(input1)
  print("Result: " + res)
  return res
  inputs = {"input_df": SampleDefinition(DataTypes.PANDAS, df)}
  
  #Genereate the schema
  generate_schema(run_func=run, inputs=inputs, filepath='./service_schema.json')
  print("Schema generated")

if __name__ == "__main__":
    score()
