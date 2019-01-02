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

@app.route('/ajax/findOuter')
def ajaxFindOuter():
    target = request.args.get('name')
    data = database.findOuter(target)
    if len(data) > 0:
        res = {'content': data}
    else:
        res = {'content': None}
    return json.dumps(res)


@app.route('/ajax/getCredits')
def ajaxGetCredits():
    exception = ["服務學習","資訊素養作業一：資料蒐集報告","資訊素養作業二：危機處理分析",
                 "資訊素養作業三：資訊理論簡測","資訊素養作業四：實際參訪報告","資訊素養作業五：自我介紹檔案",
                 "資訊素養作業六：電子書編寫","公民參與","多元文化","社會實踐","創意思考","體育(一)","體育(二)","英文(一)初級",
                 "英文(一)中級","英文(一)中高級","英文(二)初級","英文(二)中級","英文(二)中高級","大學國文(一)","大學國文(二)",
                 "全民國防教育軍事訓練(一)","全民國防教育軍事訓練(二)","英文能力檢定",""]
    target = request.args.get('name')
    data = database.getUnitCredits(target)
    
    temp = request.args.getlist('primary[]')
    temp2 = request.args.getlist('elective[]')
    temp3 = request.args.getlist('Gen[]')
    primaryCredits = 0
    electiveCredits = 0
    GenCredits = 0
    for i in range(len(temp)):
        
        if temp[i].split(" ")[10].split("\n")[0] in exception:
            print(temp[i].split(" ")[10].split("\n")[0]+"通識核心")
            print(database.getClassCredits([temp[i].split(" ")[10].split("\n")[0],target,"通識核心"]))
            GenCredits += database.getClassCredits([temp[i].split(" ")[10].split("\n")[0],target ,"通識核心"])
        else:
            print(temp[i].split(" ")[10].split("\n")[0]+"必修")
            print(database.getClassCredits([temp[i].split(" ")[10].split("\n")[0],target,"必修"]))
            primaryCredits += database.getClassCredits([temp[i].split(" ")[10].split("\n")[0],target,"必修"])
    for j in range(len(temp2)):
        print(temp2[j].split(" ")[10].split("\n")[0]+"選修")
        print(database.getClassCredits([temp2[j].split(" ")[10].split("\n")[0],target,"選修"]))
        electiveCredits += database.getClassCredits([temp2[j].split(" ")[10].split("\n")[0],target,"選修"])
    for k in range(len(temp3)):
        print(temp3[k].split(" ")[10].split("\n")[0]+"通識核心")
        print(database.getClassCredits([temp3[k].split(" ")[10].split("\n")[0],target ,"通識核心"]))
        GenCredits += database.getClassCredits([temp3[k].split(" ")[10].split("\n")[0],target ,"通識核心"])
    print(primaryCredits)
    print(electiveCredits)
    print(GenCredits)
    print(data)
    data += (primaryCredits, electiveCredits, 0, GenCredits, 0)
    print(data)
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

@app.route('/ajax/feedback')
def ajaxfeedback():
    target1 = request.args.get('name')
    target2 = request.args.get('comment')
    database.feedback(target1, target2)
    return ()

@app.route('/feedback')
def feedbackPage():
    return render_template('feedback.html')

if __name__ == "__main__":
    app.run()
