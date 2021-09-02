import re
from flask import Flask , render_template, request
import flask
import pandas
import csv
import os
import re
import pandas as pd
import tabulate
from IPython.display import HTML


app = Flask(__name__,template_folder='templates')
app.config["UPLOAD_PATH"] = "/home/veerendra.b/Desktop/upload/"

@app.route('/')
def intro():
    
    return render_template('intro.html')

@app.route('/index',methods = ['GET','POST'])
def index():
    if request.method == 'POST':
        
        for f in request.files.getlist('file_name'):
            #f=request.files['file_name']
            f.save(os.path.join(app.config['UPLOAD_PATH'],f.filename))
        return render_template('index.html',msg = "File Uploaded successfully")
    return render_template('index.html',msg="Choose files to upload")


@app.route('/report')
def report():
    
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    pd.set_option('display.colheader_justify', 'center')
    pd.set_option('display.precision', 3)


    df1 = pd.read_csv('file1.csv')
    df2 = pd.read_csv('file2.csv')
    
    list_of_column_names = list(df1.columns)
    redshift = len(df1)
    mongodb = len(df2)

    null_count = df1.isna().sum()
    result1 = df1[~df1.apply(tuple,1).isin(df2.apply(tuple,1))]
    file = open(r"templates/table.html","r+")
    file.truncate(0)
    file.close()
    for i in range(len(list_of_column_names)):
        result = result1.to_html(columns=[list_of_column_names[i]])
        text_file = open(r"templates/table.html", "a")
        text_file.write(result)
        text_file.close()
    return render_template('report.html',redshift = redshift , mongodb = mongodb , null_count = null_count)


@app.route('/table')
def table():
    return render_template("table.html")





if __name__ == '__main__':
    app.debug = True
    app.run()
    