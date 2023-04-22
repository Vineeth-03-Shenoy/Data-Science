from flask import Flask, flash, redirect, render_template, request, url_for
import pandas as pd
import cleanData

app = Flask(__name__)
app.secret_key = 'my_secret_key'

df = pd.DataFrame()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    global df
    df = pd.read_csv(file)
    # perform analysis using pandas code here
    # save the data to a file or database
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
    data = cleanData.getCleaned(df)
    data = data.to_html(index=False)
    return render_template('clean.html', data=data)

@app.route('/analyze')
def analyze():
    # retrieve the data from the file or database
    # and perform some analysis using pandas or another library
    # and return the results as a message or HTML table
    return 'Data analyzed successfully!'

@app.route('/visualize')
def visualize():
    # retrieve the data from the file or database
    # and generate a visualization using a library like Matplotlib or Bokeh
    # and return the visualization as an image or HTML page
    return 'Data visualized successfully!'

if __name__ == '__main__':
    app.run(debug=True)