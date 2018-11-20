from flask import Flask, render_template, request
import json
import database

app = Flask(__name__)


@app.route('/getClassList', methods=['POST'])
def getClassList():
    required = [[], [], [], [], []]
    elective = [[], [], [], [], []]
    for c in database.getClassList(request.form['unit']):
        if c[4] > 4:
            if c[2] == '必修':
                required[0].append(c[0])
            else:
                elective[0].append(c[0])
        else:
            if c[2] == '必修':
                required[c[4]].append(c[0])
            else:
                elective[c[4]].append(c[0])
    return render_template('index.html', data=[required, elective])


@app.route('/ajaxFindClass')
def ajaxFindClass():
    target = request.args.get('text')
    data = database.findGeneral(target)
    if len(data) > 0:
        res = {'content': data}
    else:
        res = {'content': None}
    # print (res)
    return json.dumps(res)


@app.route('/')
def index():
    return render_template('form.html')


if __name__ == "__main__":
    app.run()
