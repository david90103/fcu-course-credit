from selenium import webdriver


def worm(acc, pas):
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    browser = webdriver.Chrome("./chromedriver.exe", chrome_options=option)

    browser.get('http://learningportfolio.fcu.edu.tw/tw/index.aspx')

    account = browser.find_element_by_id("ctl00_ucLogin_txtID")
    account.send_keys(acc)
    password = browser.find_element_by_id("ctl00_ucLogin_txtPW")
    password.send_keys(pas)
    
    btn = browser.find_element_by_id("ctl00_ucLogin_btnLogin").click()
    try:
        btn = browser.find_element_by_id("li_LearnAssist").click()
    except:
        return {}
    btn = browser.find_element_by_xpath("//*[@id=\"ctl00_Div_LearnAssist\"]/ul/li[11]/a").click()

    answer = {"通識基礎": [],
              "院系必修": [],
              "本系專業選修": [],
              "非本系專業選修": [],
              "通識選修": []
              }
    try:
        GenMustList = browser.find_element_by_id(
            "ctl00_MainContent_GenMustListView_tableHeader").find_elements_by_tag_name('tr')

        for i in range(len(GenMustList)):
            if (i == 0 or i == 1):
                continue
            GenMustListtmep = GenMustList[i].find_elements_by_tag_name('td')
            if (GenMustListtmep[4].text == "通過" or GenMustListtmep[4].text == "抵免" or int(GenMustListtmep[4].text) >= 60):
                answer["通識基礎"].append(GenMustListtmep[1].text)
    except :
        print('無通識基礎修課紀錄!')
        
    try:
        CollegeMustListView = browser.find_element_by_id(
            "ctl00_MainContent_CollegeMustListView_tableHeader").find_elements_by_tag_name('tr')

        for i in range(len(CollegeMustListView)):
            if (i == 0 or i == 1):
                continue
            CollegeMustListViewtmep = CollegeMustListView[i].find_elements_by_tag_name('td')
            if (CollegeMustListViewtmep[4].text == "通過" or CollegeMustListViewtmep[4].text == "抵免" or int(CollegeMustListViewtmep[4].text) >= 60):
                answer["院系必修"].append(CollegeMustListViewtmep[1].text)
    except :
        print('無院系必修修課紀錄!')
        
    try:
        CollegeProListView = browser.find_element_by_id(
            "ctl00_MainContent_CollegeProListView_tableHeader").find_elements_by_tag_name('tr')

        for i in range(len(CollegeProListView)):
            if (i == 0 or i == 1):
                continue
            CollegeProListViewtmep = CollegeProListView[i].find_elements_by_tag_name('td')
            if (CollegeProListViewtmep[4].text == "通過" or CollegeProListViewtmep[4].text == "抵免" or int(CollegeProListViewtmep[4].text) >= 60):
                answer["本系專業選修"].append(CollegeProListViewtmep[1].text)
    except :
        print('無本系專業選修修課紀錄!')

    try:
        NoCollegeProListView = browser.find_element_by_id(
            "ctl00_MainContent_NoCollegeProListView_tableHeader").find_elements_by_tag_name('tr')

        for i in range(len(NoCollegeProListView)):
            if (i == 0 or i == 1):
                continue
            NoCollegeProListViewtmep = NoCollegeProListView[i].find_elements_by_tag_name('td')
            if (NoCollegeProListViewtmep[4].text == "通過" or NoCollegeProListViewtmep[4].text == "抵免" or int(NoCollegeProListViewtmep[4].text) >= 60):
                answer["非本系專業選修"].append(NoCollegeProListViewtmep[1].text)
    except :
        print('無本系專業選修修課紀錄!')

    try:
        GenSelectListView = browser.find_element_by_id(
            "ctl00_MainContent_GenSelectListView_tableHeader").find_elements_by_tag_name('tr')

        for i in range(len(GenSelectListView)):
            if (i == 0 or i == 1):
                continue
            GenSelectListViewtmep = GenSelectListView[i].find_elements_by_tag_name('td')
            if (GenSelectListViewtmep[4].text == "通過" or GenSelectListViewtmep[4].text == "抵免" or int(GenSelectListViewtmep[4].text) >= 60):
                answer["通識選修"].append(GenSelectListViewtmep[1].text)
    except :
        print('無通識選修修課紀錄!')
    return answer
