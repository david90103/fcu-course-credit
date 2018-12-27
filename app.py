from flask import Flask, render_template, request, redirect
from util import worm
import json
import database

app = Flask(__name__)


@app.route('/nidLogin', methods=['POST'])
def nidLogin():
    result = worm(request.form.get('nid_acc', None), request.form.get('nid_pwd', None))
    return render_template('nidresult.html', data=database.nidGetCridits(result))


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


@app.route('/ajax/getCredits')
def ajaxGetCredits():
    target = request.args.get('name')
    data = database.getUnitCredits(target)
    temp = request.args.getlist('classes[]')
    
    f = open('h.txt','w')
    for i in temp:
        #print(temp)
        f.write(i)
    f.close()
    if len(data) > 0:
        res = {'content': data}
    else:
        res = {'content': None}
    return json.dumps(res)


@app.route('/ajax/searchTeacher')
def ajaxSearchTeacher():
    target = request.args.get('name')
    data = database.searchTeacher(target)
    if len(data) > 0:
        res = {'content': data}
    else:
        res = {'content': None}
    return json.dumps(res)


@app.route('/teacher')
def teacherPage():
    return render_template('teacher.html')


@app.route('/')
def index():
    d = database.getDeptList()
    return render_template('index.html', data=d)


if __name__ == "__main__":
    app.run()
