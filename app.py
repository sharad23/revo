from flask import Flask, render_template, request, send_from_directory
from flask import jsonify
from lib.execute import daily_reporting, transaction_reporting, rollover_reporting, emi_cal
import json
import csv
import os

PATH = '~/revolving_cr/'
DOMAIN = os.environ.get('BASE_URL', 'http://localhost:5000/')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PATH


@app.route('/', methods=['GET'])
# def dashboard():
#    return render_template('home.html', domain=DOMAIN)


@app.route('/api/daily-reporting', methods=['POST'])
def test():
    if request.method == 'POST':
        input_data = request.get_json()
        print(input_data)
        results = daily_reporting(**input_data)
        return jsonify(results)


@app.route('/api/trans-reporting', methods=['POST'])
def test2():
    if request.method == 'POST':
        input_data = request.get_json()
        results = transaction_reporting(**input_data)
        return jsonify(results)

@app.route('/daily-reporting', methods=['POST', 'GET'])
def hello():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        filename, ext = f.filename.split('.')
        filename = filename + '_'
        print('here')
        print(filename, ext)
        with open(f.filename) as json_data:
            daily = json.load(json_data)
            results = daily_reporting(**daily)
            if results:
                keys = results[0].keys()
                with open(filename+'.csv', 'w') as csv_file:
                    c = csv.writer(csv_file)
                    c.writerow(keys)
                    for result in results:
                        c.writerow(result.values())
        # return 'complete'
        return send_from_directory(directory='.', filename=filename+'.csv', as_attachment=True)
    else:
        return render_template('daily.html', domain=DOMAIN)
    # return 'Hello World'


@app.route('/trans-reporting', methods=['POST', 'GET'])
def hello2():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        filename, ext = f.filename.split('.')
        filename = filename + '_'
        print('here')
        print(filename, ext)
        with open(f.filename) as json_data:
            trans = json.load(json_data)
            results = transaction_reporting(**trans)
            if results:
                keys = results[0].keys()
                with open(filename+'.csv', 'w') as csv_file:
                    c = csv.writer(csv_file)
                    c.writerow(keys)
                    for result in results:
                        c.writerow(result.values())

        return send_from_directory(directory='.', filename=filename + '.csv')
        # return 'complete'

    else:
        return render_template('trans.html', domain=DOMAIN)
    # return 'Hello World'


@app.route('/rollover-reporting', methods=['POST', 'GET'])
def hello3():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        filename, ext = f.filename.split('.')
        filename = filename + '_'
        print('here')
        print(filename, ext)
        with open(f.filename) as json_data:
            roll = json.load(json_data)
            results = rollover_reporting(**roll)
            if results:
                keys = results[0].keys()
                with open(filename+'.csv', 'w') as csv_file:
                    c = csv.writer(csv_file)
                    c.writerow(keys)
                    for result in results:
                        c.writerow(result.values())

        return send_from_directory(directory='.', filename=filename + '.csv')
        # return 'complete'

    else:
        return render_template('rollover.html', domain=DOMAIN)
    # return 'Hello World'


@app.route('/emi', methods=['POST', 'GET'])
def hello4():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        filename, ext = f.filename.split('.')
        filename = filename + '_'
        print('here')
        print(filename, ext)
        with open(f.filename) as json_data:
            emi_cals = json.load(json_data)
            results = emi_cal(**emi_cals)
            if results:
                keys = results[0].keys()
                with open(filename+'.csv', 'w') as csv_file:
                    c = csv.writer(csv_file)
                    c.writerow(keys)
                    for result in results:
                        c.writerow(result.values())

        return send_from_directory(directory='.', filename=filename + '.csv')
        # return 'complete'

    else:
        return render_template('emi.html', domain=DOMAIN)
    # return 'Hello World'


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)