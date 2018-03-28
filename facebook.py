#this is for facebook api json
import sys
import json
import requests
import codecs

#this is for update token
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#this is for queue to save the processed posts
from Queue import PriorityQueue

q = PriorityQueue(maxsize=50)

SUBSCRIPTION_TOKEN = "tony_server_token"

MAX_MSG_LEN = 300
GRAPH_API = "https://graph.facebook.com/v2.3/me/messages"
GRAPH_API_USER = 'https://graph.facebook.com/v2.3/me/groups'

ACCESS_TOKEN_PAGE = "EAADnDRlMFXQBAFr69RLlAmGZBObbP2QJSA9oVZCtUoEwTlQdE4Ju78xHaE6cDzVIm8MT5mUlxuSk2kQLFZAbZCtIOyQusSbZBEQcZBYURRX5HPhvZCgZATBFukG9mYp6AzPHgVwlqXdZB7l8Jb0UZAEO5ZC3XjK0B9mdWDZCc5UsZCodLQgZDZD"
ID_USER = '779372735413850'
ACCESS_TOKEN_USER = 'EAACEdEose0cBAN8VLnOvPKWZAZASoulmO0no0jPsvxMfPX7RiXA4WVtAi2JNomAAzcurOrFdaAGWA3oXZCH3VdKvH24q1d0nHiT6uUYWYlRVKx5FeiH7mrL8QHoeSJsUaEIn8fj88samljy2XiK6jo5Rfjl1kVaBQREljMAdMNzUiyGm7SWyiZA1HpuOMZB8ZD'

ID_LIST=[]

VIP_KEY_LIST=[]
NOT_KEY_LIST=[]
NOT_KEY_LIST2 = []

cm_mes_save = []
class Facebook_messages():
       #May me cho hoi

    def _split_msg(self, text):
        """
        Facebook doesn't allows messages longer than MAX_MSG_LEN in chat windows.
        This function cuts messages exceeding MAX_MSG_LEN and returns
        a list of appropriately trimmed messages.
        """
        text = [text[i:i+MAX_MSG_LEN]
                  for i in range(0, len(text), MAX_MSG_LEN)]
        return text

    def simple_msg(self, recipient_id, message_text):
        """
        This function is used to send chat messages that don't exceed MAX_MSG_LEN.
        """
        params = {"access_token": ACCESS_TOKEN_PAGE}
        headers = {"Content-Type": "application/json"}
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "text": message_text
            }
            })

        # try:
        #     print("Sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))
        # except:
        #     print("Error printing the message. The server will try returning received message.")



        r = requests.post(GRAPH_API, params=params, headers=headers, data=data)
        if r.status_code != 200:
            print(r.status_code)
            print(r.text)


    def long_msg(self, recipient_id, message_text):
        """
        This function is used to send chat messages which length is not known
        at the time of writing.
        """
        if len(message_text) > MAX_MSG_LEN:
            msg_list = self._split_msg(message_text)
            for i in msg_list:
                self.simple_msg(recipient_id, i)
        else:
            self.simple_msg(recipient_id, message_text)


    def filter(self):
        self.check_token_expire()
        for x in range(0,len(ID_LIST)):
            self.search_content(ID_LIST[x])

    def check_token_expire(self):
        # get_url1 = "https://graph.facebook.com/v2.3/me?access_token=%s"
        get_url1 = "https://graph.facebook.com/v2.3/779372735413850?format=json&access_token=%s" %  (ACCESS_TOKEN_USER)
        ri = requests.get(get_url1)
        recei_obj = json.loads(ri.text)
        if ("Session has expired" in str(recei_obj)):
            # print "old token"
            # print ACCESS_TOKEN_USER
            self.update_token()


    def update_token(self):
        global ACCESS_TOKEN_USER
        driver = webdriver.Firefox()
        driver.get("https://developers.facebook.com/tools/explorer/145634995501895/?method=GET&path=378256442538076%2Ffeed&version=v2.3")
        # elem = driver.find_elements_by_class_name("_4qba") #note that elements is plural
        # print elem[0].text
        # print elem[1].text

        elem = driver.find_element_by_class_name("_p47").click()
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))

        elem = driver.find_element_by_name("email")
        elem.clear()
        elem.send_keys("YOUR_EMAIL@gmail.com")
        elem = driver.find_element_by_name("pass")
        elem.clear()
        elem.send_keys("YOUR_PASS")
        elem.send_keys(Keys.RETURN)

        # driver.implicitly_wait(10) # seconds
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "_58al")))
        access_token_list = driver.find_elements_by_class_name("_58al") #Note that the elements is PLURALLLLLLLLLLLL form for return all the elements in the same class
        for i in range(0, len(access_token_list)):
            te_str = access_token_list[i].get_attribute("value")
            if "EAACE" in te_str:
                ACCESS_TOKEN_USER =  te_str
        print "updated token"
        driver.close()
        driver.quit()



    def search_content(self,recipient_id):

        get_url1 = "https://graph.facebook.com/v2.3/%s/feed?access_token=%s&pretty=0&limit=%s&fields=message,comments{message,comments},actions,id" % (recipient_id, ACCESS_TOKEN_USER,'200')
        ri = requests.get(get_url1)
        recei_obj = json.loads(ri.text)
        count = 1;
        if "Session has expired" in str(recei_obj):
            print("didn't update token yet")
            return -1
        elif recei_obj.get("data"):

            for data in recei_obj["data"]:
                    if data.get("message"):
                        cm_mes_save.append(data["message"])
                        if("3940" in data["message"]):
                            print("found")
                    if data.get("comments"):
                        for data2 in data["comments"]["data"]:
                            cm_mes_save.append(data2["message"])
                            if(data2.get("comments")):
                                for data3 in data2["comments"]["data"]:
                                    cm_mes_save.append(data3["message"])

                    while(len(cm_mes_save)!=0):
                        str2 = cm_mes_save.pop()
                        # print(str2)
                        if(self.check_NOT_LIST2(str2)):
                            for k in range(0,len(VIP_KEY_LIST)):
                                if(VIP_KEY_LIST[k] in str2):
                                    str1 = self.find_idx(str2,VIP_KEY_LIST[k])
                                    if  str1 != "-1":
                                        # print(recei_obj)
                                        if self.last_check(str1):
                                            save_str = ""
                                            if q.empty() == False:
                                                save_str = str(q.queue)
                                            else:
                                                save_str = str(self.read_queue())
                                                q.put(save_str[1:len(save_str)])
                                            if(data["id"] not in save_str):
                                                # print save_str
                                                if q.full() == True:
                                                    q.get()
                                                q.put(data["id"])
                                                self.save_queue(str(q.queue))
                                                se_link = "empty link"
                                                for get_li in data["actions"]:
                                                    if get_li["name"] == "Comment":
                                                        se_link = get_li["link"]

                                                self.simple_msg("1187100788073304",str1)
                                                self.simple_msg("1187100788073304",se_link)

                                                print(count)
                                                count = count + 1
                                                print(str1)
                                                print(se_link)


    def save_queue(self,data):
        spID = open("save_processed_id.txt","w")
        spID.write(data)
        spID.close()
    def read_queue(self):
        spID = open("save_processed_id.txt","r")
        data = spID.read()
        spID.close()
        return data
    def check_NOT_LIST2(self,str2):
        for i in range(0,len(NOT_KEY_LIST2)):
            if NOT_KEY_LIST2[i] in str2:
                return False
        return True
    def last_check(self,str2):
        for i in range(0,len(NOT_KEY_LIST)):
            if NOT_KEY_LIST[i] in str2:
                return False
        return True

    def find_idx(self,str2, sub_str):
        m = 0
        k = 0
        while (k < len(str2)):
            if sub_str[0] == str2[k]:
                if(k == 0 or (k>0 and str2[k-1] == " ")):
                    flag = 1
                    while (m < len(sub_str)):
                        if k>=len(str2) or str2[k] != sub_str[m]:
                            flag = 0
                            m = 0
                            break
                        m = m + 1
                        k = k + 1

                    if flag == 1 and (k > len(str2) or (k < len(str2) and str2[k] == " ")):
                        st = k - 40;
                        ed = k + 30;
                        if st < 0:
                            st = 0
                        elif ed > len(str2):
                            ed = len(str2)
                        return str2[st:ed]
            k = k + 1
        return "-1"

    def __init__(self):
        ID_LIST.append("480091822118158")
        ID_LIST.append("1156331831095356")
        ID_LIST.append("412008888937341")
        ID_LIST.append("700505446660308")

        ID_LIST.append("614420311970372")
        # ID_LIST.append("628063213936942")
        # ID_LIST.append("649481551829720")
        # ID_LIST.append("518763954899892")
        # ID_LIST.append("482906351837231")
        # ID_LIST.append("826351990726927")
        # ID_LIST.append("197019840463328")

        VIP_KEY_LIST.append("3940")
        VIP_KEY_LIST.append(u'can em cho')
        VIP_KEY_LIST.append(u'c\u1EA7n em cho')
        VIP_KEY_LIST.append(u'can minh cho')
        VIP_KEY_LIST.append(u'c\u1EA7n m\u00ECnh cho')
        VIP_KEY_LIST.append(u'can to cho')
        VIP_KEY_LIST.append(u'can t\u1EDB cho')
        VIP_KEY_LIST.append(u'c\u1EA7n em cho')
        VIP_KEY_LIST.append(u'c\u1EA7n e cho')
        VIP_KEY_LIST.append(u'c\u1EA7n m cho')
        VIP_KEY_LIST.append(u'to cho')
        VIP_KEY_LIST.append(u't\u1EDB cho')
        VIP_KEY_LIST.append(u'minh cho')
        VIP_KEY_LIST.append(u'm\u00ECnh cho')
        VIP_KEY_LIST.append(u'e cho')
        VIP_KEY_LIST.append(u'em cho')
        VIP_KEY_LIST.append(u'c cho')
        # VIP_KEY_LIST.append(u'chi cho')
        VIP_KEY_LIST.append(u'ch\u1ECB cho')
        VIP_KEY_LIST.append(u'minh gui cho')
        VIP_KEY_LIST.append(u'm g\u1EEDi cho')
        VIP_KEY_LIST.append(u'minh g\u1EEDi cho')
        VIP_KEY_LIST.append(u'm\u00ECnh g\u1EEDi cho')
        VIP_KEY_LIST.append(u'to gui cho')
        VIP_KEY_LIST.append(u't g\u1EEDi cho')
        VIP_KEY_LIST.append(u't\u1EDB g\u1EEDi cho')
        VIP_KEY_LIST.append(u'em gui cho')
        VIP_KEY_LIST.append(u'em g\u1EEDi cho')
        VIP_KEY_LIST.append(u'e g\u1EEDi cho')

        VIP_KEY_LIST.append(u'free')
        VIP_KEY_LIST.append(u'FREE')
        VIP_KEY_LIST.append(u'moving sale')
        VIP_KEY_LIST.append(u'MOVING SALE')


        NOT_KEY_LIST.append(u'e cho h\u1ecfi')
        NOT_KEY_LIST.append(u'em cho hoi')
        NOT_KEY_LIST.append(u'em cho h\u1ecfi')
        NOT_KEY_LIST.append(u'e cho hoi')
        NOT_KEY_LIST.append(u'cho e h\u1ecfi')
        NOT_KEY_LIST.append(u'cho e hoi')
        NOT_KEY_LIST.append(u'cho em h\u1ecfi')
        NOT_KEY_LIST.append(u'cho em l\u00E0m phi\u1EC1n')
        NOT_KEY_LIST.append(u'cho em lam phien')
        NOT_KEY_LIST.append(u'cho e l\u00E0m phi\u1EC1n')
        NOT_KEY_LIST.append(u'cho e lam phien')
        NOT_KEY_LIST.append(u'cho b\u00E9 b\u00FA')
        NOT_KEY_LIST.append(u'cho be bu')
        NOT_KEY_LIST.append(u'cho b\u00E9 v\u1EC1 vi\u1EC7t') # cho be ve vn
        NOT_KEY_LIST.append(u'cho b\u00E9 v\u1EC1 vn') # cho be ve vn
        NOT_KEY_LIST.append(u'gi\u1EEF cho da')
        NOT_KEY_LIST.append(u'\u1EA9m cho da')
        NOT_KEY_LIST.append(u'cho be ve vn')
        NOT_KEY_LIST.append(u'cho be ve viet nam')
        NOT_KEY_LIST.append(u'giu cho da')
        NOT_KEY_LIST.append(u'am cho da')
        NOT_KEY_LIST.append(u'ch\u1EC9 cho em')
        NOT_KEY_LIST.append(u'ch\u1EC9 em voi')
        NOT_KEY_LIST.append(u'visa cho be')
        NOT_KEY_LIST.append(u'chia se cho')
        NOT_KEY_LIST.append(u'chia s\u1EBB cho')
        NOT_KEY_LIST.append(u'l\u00E0m ph\u00F2ng cho')
        NOT_KEY_LIST.append(u'co cach gi cho no het')
        NOT_KEY_LIST.append(u'co cach j cho no het')
        NOT_KEY_LIST.append(u'co cach gj cho no het')
        NOT_KEY_LIST.append(u'tinh yeu danh cho con')
        NOT_KEY_LIST.append(u't\u00ECnh y\u00EAu d\u00E0nh cho con')
        NOT_KEY_LIST.append(u'cho an')
        NOT_KEY_LIST.append(u'cho \u0103n')
        NOT_KEY_LIST.append(u'cho ck')
        NOT_KEY_LIST.append(u'cho chong')
        NOT_KEY_LIST.append(u'cho ong chong')
        NOT_KEY_LIST.append(u'cho \u00F4ng ch\u1ED3ng')
        NOT_KEY_LIST.append(u'cho ch\u1ED3ng')
        NOT_KEY_LIST.append(u'dt cho no roi')
        NOT_KEY_LIST.append(u'dien thoai cho no roi')
        NOT_KEY_LIST.append(u'dt cho n\u00F3 r\u1ED3i')
        NOT_KEY_LIST.append(u'\u0111i\u1EC7n tho\u1EA1i cho n\u00F3 r\u1ED3i')
        NOT_KEY_LIST.append(u'cho uong')
        NOT_KEY_LIST.append(u'cho u\u1ED1ng')
        NOT_KEY_LIST.append(u'cho mai toc')
        NOT_KEY_LIST.append(u'cho m\u00E1i t\u00F3c')
        NOT_KEY_LIST.append(u'cho t\u00F3c')
        NOT_KEY_LIST.append(u'cho toc')
        NOT_KEY_LIST.append(u'cho cac me')
        NOT_KEY_LIST.append(u'cho c\u00E1c m\u1EB9')
        NOT_KEY_LIST.append(u'cho ce')
        NOT_KEY_LIST.append(u'cho chi em')
        NOT_KEY_LIST.append(u'cho ch\u1ECB em')
        NOT_KEY_LIST.append(u'cho em biet')
        NOT_KEY_LIST.append(u'cho em bi\u1EBFt')
        NOT_KEY_LIST.append(u'cho minh \u0111\u0103ng')
        NOT_KEY_LIST.append(u'cho minh h\u1ecfi')
        NOT_KEY_LIST.append(u'cho m\u00ECnh h\u1ecfi')
        NOT_KEY_LIST.append(u'cho minh hoi')
        NOT_KEY_LIST.append(u'cho m \u0111\u0103ng')
        NOT_KEY_LIST.append(u'cho mjk \u0111\u0103ng')
        NOT_KEY_LIST.append(u'cho mik \u0111\u0103ng')
        NOT_KEY_LIST.append(u'cho minh dang')
        NOT_KEY_LIST.append(u'cho m dang')
        NOT_KEY_LIST.append(u'cho mjk dang')
        NOT_KEY_LIST.append(u'cho mik dang')
        NOT_KEY_LIST.append(u'cho con an dam')
        NOT_KEY_LIST.append(u'cho con \u0103n d\u1EB7m')
        NOT_KEY_LIST.append(u'cho co the')
        NOT_KEY_LIST.append(u'cho c\u01A1 th\u1EC3')
        NOT_KEY_LIST.append(u'cho e xin y kien')
        NOT_KEY_LIST.append(u'giay to cho')
        NOT_KEY_LIST.append(u'em cho vui')
        NOT_KEY_LIST.append(u'em cho vuj')
        NOT_KEY_LIST.append(u'c e cho minh hoi')
        NOT_KEY_LIST.append(u'minh cho bu')
        NOT_KEY_LIST.append(u'minh cho be')
        NOT_KEY_LIST.append(u'to cho con')
        NOT_KEY_LIST.append(u'minh cho con')

        NOT_KEY_LIST.append(u'feel free to ask')
        NOT_KEY_LIST.append(u'free delivery')
        NOT_KEY_LIST.append(u'free shipping')
        NOT_KEY_LIST.append(u'free pre-paid')
        NOT_KEY_LIST.append(u'free to call')
        NOT_KEY_LIST.append(u'free to message')
        NOT_KEY_LIST.append(u'free tekpe')
        NOT_KEY_LIST.append(u'free tekbe')

        NOT_KEY_LIST2.append(u'APP')
        NOT_KEY_LIST2.append(u'app')
        NOT_KEY_LIST2.append(u'sim card')
        NOT_KEY_LIST2.append(u'phone')
        NOT_KEY_LIST2.append(u'sim')
        NOT_KEY_LIST2.append(u'SIM')
        NOT_KEY_LIST2.append(u'kt')
        NOT_KEY_LIST2.append(u'lg')
        NOT_KEY_LIST2.append(u'skt')
        NOT_KEY_LIST2.append(u'lg')
        NOT_KEY_LIST2.append(u'LG')
        NOT_KEY_LIST2.append(u'full box')
        NOT_KEY_LIST2.append(u'FULL BOX')
