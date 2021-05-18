from flask import Flask, flash, request, redirect, url_for, make_response
import pandas as pd
from stationary_module import StationaryTestModule
from idtxlmodules import MultiVariateTime
from pandas.api.types import is_numeric_dtype
import numpy as np
import json
from idtxl.data import Data
from flask import send_file

app = Flask('your_flask_env')

dataframe = None
toggledDifference = 0

@app.route('/get_image')
def get_image():
    if request.args.get('type') == '1':
       filename = 'test.png'
    else:
       filename = 'test.png'
    print(filename)
    print("###############################################################")
    response = send_file(filename, mimetype='image/png')
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")

    return response

@app.route('/togglete', methods=['POST'])
def runTE():
    global dataframe
    response = {}
    if request.method == 'POST':
        if isinstance(dataframe, pd.DataFrame):

            inputTE = json.loads(request.form['inputTE'])
            inputTE = {k: v for k, v in inputTE.items() if len(v) > 0}
            
            for key, value in inputTE.items():
                try:
                    inputTE[key] = int(value)
                except:
                    pass

            numpy_format = dataframe.to_numpy()
            arr_format = numpy_format.reshape((3, len(numpy_format), 1))
            # settings = {'cmi_estimator': 'JidtGaussianCMI',
            #             'max_lag_sources': 5,
            #             'min_lag_sources': 1}

            mod = MultiVariateTime(Data(arr_format), inputTE)
            a, b = mod.run()
            b.savefig("test.png")
            #return send_file("test.png", mimetype='image/PNG')
            response['results'] = 'pass'
            response['details'] = 'Successfully discretize'

        else:
            response['results'] = 'fail'
            response['details'] = 'No dataframe uploaded'
    return generateResponse(response)


@app.route('/togglediscretize', methods=['POST'])
def runDiscretize():
    global dataframe
    response = {}
    if request.method == 'POST':
        if isinstance(dataframe, pd.DataFrame):
            try:
                for col in dataframe.columns:
                    dataframe[col] = dataframe[col].astype(np.int64)
                response['results'] = 'pass'
                response['details'] = 'Successfully discretize'
            except Exception as e:
                response['results'] = 'fail'
                response['details'] = str(e)
        else:
            response['results'] = 'fail'
            response['details'] = 'No dataframe uploaded'
    return generateResponse(response)


@app.route('/runstationarity', methods=['POST'])
def runstationarity():
    global dataframe
    response = {}

    if request.method == 'POST':
        if isinstance(dataframe, pd.DataFrame):
            try:
                module = StationaryTestModule()
                response['results'], response['details'] = module.getResult(dataframe, request.form['adfSig'], request.form['johSig'])
            except Exception as e:
                response['results'] = 'fail'
                response['details'] = str(e)
        else:
            response['results'] = 'fail'
            response['details'] = 'No dataframe uploaded'

    return generateResponse(response)


@app.route('/toggledifference', methods=['POST'])
def toggledifference():
    global dataframe
    global toggledDifference
    response = {}


    if request.method == 'POST':

        if (toggledDifference > 0):
            response['results'] = 'fail'
            response['details'] = "First order difference toggled before"
            return generateResponse(response)

        if isinstance(dataframe, pd.DataFrame):
            try:
                dataframe = dataframe.diff()
                dataframe = dataframe.iloc[1:]

                response['results'] = 'pass'
                response['details'] = 'pass'
                toggledDifference += 1
            except Exception as e:
                response['results'] = 'fail'
                response['details'] = str(e)
        else:
            response['results'] = 'fail'
            response['details'] = 'No dataframe uploaded'


    return generateResponse(response)



@app.route('/uploadCSV', methods=['POST'])
def uploadCSV():
    global dataframe
    global toggledDifference
    response = {}

    if request.method == 'POST':
        if 'CSVFileUpload' in request.files:
            try:
                file = request.files['CSVFileUpload']
                dataframe = pd.read_csv(file)

                response['results'] = 'pass'
                response['details'] = 'pass'
                #no first order difference toggled
                toggledDifference = 0

                #check to make sure that df is int64 or float64
                for col in dataframe.columns:
                    if (not is_numeric_dtype(dataframe[col])):
                        response['results'] = 'fail'
                        response['details'] = "Please check all columns are numeric for " + file.filename
                        df = None

            except Exception as e:
                response['details'] = 'fail'
                response['details'] = str(e)

    return generateResponse(response)

def generateResponse(res):
    response = make_response(res)
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0')
