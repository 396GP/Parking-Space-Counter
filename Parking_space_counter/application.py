from flask import Flask, render_template
import csv

app = Flask(__name__)

@app.route('/')
def index():
    data = get_csv_data()
    if data:
        count, space, total = data
        return render_template('hello.html', space=space, total=total, count=count)
    else:
        return "No data found"

def read_csv(filename):
    data = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    return data

def get_csv_data():
    data = read_csv('write.csv')
    if data:
        count = data[0][0]
        space = data[0][1]
        total = data[0][2]
        return count, space, total
    else:
        return None

if __name__ == "__main__":
    app.run(debug=True, port=5001, host='0.0.0.0')

