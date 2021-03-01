from flask import Flask, flash, request, redirect, url_for, make_response
import pandas as pd
from stationary_module import StationaryTestModule
app = Flask('your_flask_env')

dataframe = pd.read_csv("C:\\Users\\kangyu\\Desktop\\FYP\\test - Copy.csv")

@app.route('/', methods=['GET', 'POST'])
def register():
    global dataframe
    if request.method == 'POST':
        if 'CSVFileUpload' in request.files:

            try :
                file = request.files['CSVFileUpload']
                dataframe = pd.read_csv(file)
                response = make_response({"results" : "Pass"})
            except:
                response = make_response({"results" : "Fail"})

        elif 'runTest' in request.form:

            print(request.form["adfSig"])
            print(request.form["johSig"])

            module = StationaryTestModule()
            result, text = module.getResult(dataframe, request.form["adfSig"], request.form["johSig"])
            response = make_response({"results" : str(result) , "details" : str(text)})

        else:
            response = make_response({"results" : "Fail"})

        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")

        return response


    if request.method == 'GET':
        return "GET"
        # You probably don't have args at this route with GET
        # method, but if you do, you can access them like so:
    return "GET"

if __name__ == "__main__":
    app.run()
