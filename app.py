from flask import Flask, render_template, request
import pandas as pd
import numpy as np

app = Flask(__name__)
app.secret_key = 'mysecretkey'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        global df
        df = pd.read_csv(file)

        #Replace '?' and '' with NaN 
        df.replace('?', np.NaN, inplace=True)
        df.replace('', np.NaN, inplace=True)

        #Delete Rows that contain duplicates
        df.drop_duplicates(inplace=True)

        #Delete Columns that have single values 
        for key, value in df.items():
            if len(df[key].unique())==1:
                del df[key]

        miss_data = df.isnull().sum()[df.isnull().sum() > 0]
        miss_data=miss_data.to_frame()
        miss_data.columns=['No of Missing Values']
        cols = list(miss_data.index)
        dataType=df.dtypes
        dataType=dataType.to_frame() 
        return render_template('advance_cleaning.html', data=df, dataType=dataType.transpose() , cols=cols, columns=list(df.columns))

@app.route('/advance_cleaning', methods=['GET', 'POST'])
def advance_cleaning():
    global df
    clean_message = None
    if request.method == 'POST':
        if request.form['action'] == 'replace_missing':
            columns = request.form.getlist('replace_column')
            method = request.form['replace_method']
            for col in columns:
                if method == 'mean':
                    avg = df[col].astype('float').mean(axis=0)
                    df[col].replace(np.NaN, avg, inplace=True)
                elif method == 'freq':
                    freq = df[col].value_counts().idxmax()
                    df[col].replace(np.NaN, freq, inplace=True)
                elif method == 'deleteRow':
                    df.dropna(subset=[columns[0]], axis=0, inplace=True)
                    df.reset_index(drop=True, inplace=True)
            clean_message = "Missing values replaced successfully!"

        elif request.form['action'] == 'change_datatype':
            column = request.form.getlist('column')
            datatype = request.form['datatype']
            for col in column:
                df[col] = df[col].astype(datatype)
            clean_message = "Data type changed successfully!"

        elif request.form['action'] == 'normalize_data':
            columns = request.form.getlist('columns')
            df[columns] = (df[columns] - df[columns].min()) / (df[columns].max() - df[columns].min())
            data = df.head()
            desc = df.describe().to_html(classes='table table-striped')
            clean_message = "Data normalized successfully!"

        elif request.form['action'] == 'convert_categorical':
            columns = request.form.getlist('columns')
            df = pd.get_dummies(df, columns=columns, prefix=columns)
            data = df.head()
            desc = df.describe().to_html(classes='table table-striped')
            clean_message = "Categorical data converted to integer successfully!"

    miss_data = df.isnull().sum()[df.isnull().sum() > 0]
    miss_data=miss_data.to_frame()
    miss_data.columns=['No of Missing Values']
    cols = list(miss_data.index)
    dataType=df.dtypes
    dataType=dataType.to_frame() 
    return render_template('advance_cleaning.html', data=df, dataType=dataType.transpose(), cols=cols ,columns=list(df.columns), clean_message=clean_message)

if __name__ == '__main__':
    app.run(debug=True)