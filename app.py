from flask import Flask, render_template, request
import json
import database

app = Flask(__name__)


@app.route('/getClassList', methods=['GET'])
def getClassList():
    required = [[], [], [], [], []]
    elective = [[], [], [], [], []]
    for c in database.getClassList(request.args.get('unit')):
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
    return render_template('courseList.html', data=[required, elective], dept=request.args.get('unit'))


@app.route('/ajax/findClass')
def ajaxFindClass():
    target = request.args.get('name')
    data = database.findGeneral(target)
    if len(data) > 0:
        res = {'content': data}
    else:
        res = {'content': None}
    return json.dumps(res)


@app.route('/')
def index():
    d = database.getDeptList()
    return render_template('index.html', data=d)


if __name__ == "__main__":
    app.run()
