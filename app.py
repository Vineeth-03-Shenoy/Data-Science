from flask import Flask, flash, redirect, render_template, request, url_for
import pandas as pd
import numpy as np
import cleanData

app = Flask(__name__)
app.secret_key = 'my_secret_key'

df = pd.DataFrame()
miss_data = pd.Series()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    global df
    df = pd.read_csv(file)
    flash('Data uploaded successfully!')
    return redirect(url_for('index'))

@app.route('/view')
def view():
    global df
    data = df.to_html(index=False)
    return render_template('view.html', data=data)

@app.route('/describe')
def describeDF():
    global df
    return render_template('describe.html', data=df.describe(include="all").to_html(index=True))

@app.route('/clean')
def clean():
    global df
    df = cleanData.getCleaned(df)
    df = df.to_html(index=False)
    return render_template('clean.html', data=df)

@app.route('/advance_Clean')
def advanceClean():
    global df, miss_data
    df = cleanData.getCleaned(df, Target=True)
    miss_data = df.isnull().sum()[df.isnull().sum() > 0]
    miss_data=miss_data.to_frame()
    miss_data.columns=['No of Missing Values']
    return render_template('advanceClean.html', data=df.head(5).to_html(), missData=miss_data.to_html())

@app.route('/advance_Clean/replace_missing', methods=['POST'])
def replace_missing():
    columns = request.form.getlist('column')
    method = request.form.get('method')
    value = request.form.get('value')


    global df, miss_data
    miss_data = df.isnull().sum()[df.isnull().sum() > 0]
    miss_data=miss_data.to_frame()

    if not columns or not method or not value:
        return 'Error: Please select at least one column, a method, and a value'
    
    for col in columns:
        if method == 'mean':
            replacement = df[col].astype('float').mean(axis=0)
        elif method == 'freq':
            replacement = df[col].value_counts().idxmax()
        df[col].replace(np.NaN, replacement, inplace=True)    
        done=True
   
    columnsD = df.columns.tolist()
    return render_template('removeMissing.html',columns=columnsD, missData=miss_data.to_html())

@app.route('/visualize')
def visualize():
    # retrieve the data from the file or database
    # and generate a visualization using a library like Matplotlib or Bokeh
    # and return the visualization as an image or HTML page
    return 'Data visualized successfully!'

if __name__ == '__main__':
    app.run(debug=True)