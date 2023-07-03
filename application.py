from noaa import *
from gtrends import *
from flask import Flask, render_template, request, url_for
import time

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keyword_in = request.form['keyword']
        generate_chart(keyword_in)
        return render_template('chart.html')
    return render_template('index.html')

@app.route('/chart', methods=['GET', 'POST'])
def chart():
    if request.method == 'POST':
        keyword_in = request.form['keyword']
        chart_names = generate_chart(keyword_in)
        return render_template('chart.html', chart_names=chart_names)
    chart_names = []
    return render_template('chart.html', chart_names=chart_names)

@app.route('/noaa')
def noaa():
    chart_names = generate_noaa()
    #return render_template('noaa.html')
    return render_template('chart.html', chart_names=chart_names)

@app.route('/dashboard')
def dashboard():
    chart_names = generate_chart('ac repair')
    chart_names.extend(generate_chart('oil change'))
    time.sleep(1)
    return render_template('chart.html', chart_names=chart_names)

if __name__ == '__main__':
    app.run(debug=True)