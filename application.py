from noaa import *
from gtrends import *
from flask import Flask, render_template, request, url_for

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
        generate_chart(keyword_in)
        return render_template('chart.html')
    return render_template('chart.html')

@app.route('/noaa')
def noaa():
    generate_noaa()
    return render_template('noaa.html')

if __name__ == '__main__':
    app.run(debug=True)