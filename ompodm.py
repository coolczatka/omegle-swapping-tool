from selenium import webdriver
import dictionary
import time
import re
import datetime



class messageRow():
    def __init__(self,mess,client):
        self.frrom = client
        self.message = mess
        self.time = time.time()


class Client():
    def __init__(self,name):
        self.name = name
        self.driver = webdriver.Firefox()
        self.driver.get("https://www.omegle.com/")
        textButton = self.driver.find_element_by_id("textbtn")
        textButton.click()
        self.disconnBtn = self.driver.find_element_by_class_name("disconnectbtn")
        self.dc = False
        self.messages = []
        self.hms=0
        self.textarea = self.driver.find_element_by_class_name('chatmsg')
        self.sendbtn = self.driver.find_element_by_class_name('sendbtn')
    def loadMessages(self):
        if self.dc==False:
            self.messages = []
            logbox = self.driver.find_elements_by_class_name("strangermsg")
            regex = re.compile("^Stranger: ")
            end = re.compile('Stranger has disconnected')
            for i in logbox:
                if(end.match(i.text)):
                    self.dc = True
                    break
                if(not regex.match(i.text)):
                    logbox.remove(i)
            for i in range(self.hms,len(logbox)):
                    self.messages.append(messageRow(logbox[i].text[10:],self.name))
            self.hms = self.hms + len(self.messages)
    def isSthNew(self):
        return len(self.messages)!=0
    def swapMessages(self, dictionary):
        for i in dictionary:
            regex = re.compile(i)
            for j in self.messages:
                self.messages[self.messages.index(j)].message=regex.sub(dictionary[i],self.messages[self.messages.index(j)].message)
    def sendText(self,text):
        if text=="" or text==None:
            return
        while(not self.textarea.is_enabled()):
            pass
        self.textarea.clear()
        self.textarea.send_keys(text)
        self.sendbtn.click()
    def reroll(self):
        self.disconnBtn.click()
        self.dc = False

def fun(x):
        return x.time


class Conn():
    def __init__(self, nameClient1, nameClient2):
        self.c1 = Client(nameClient1)
        self.c2 = Client(nameClient2)
        self.conversation = []
        self.sendCount = 0

    def loadConversation(self):
        self.c1.loadMessages()
        self.c2.loadMessages()

        temp = self.c1.messages + self.c2.messages
        temp.sort(key=fun)
        for i in temp:
            self.conversation.append(i)

    def send(self):
        for i in range(self.sendCount,len(self.conversation)):
            if(self.conversation[i].frrom==self.c1.name):
                self.c2.sendText(self.conversation[i].message)
            else:
                self.c1.sendText(self.conversation[i].message)
        self.sendCount = len(self.conversation)

    def sendSwapped(self):
        self.c1.swapMessages(dictionary.dictionary)
        self.c2.swapMessages(dictionary.dictionary)
        self.send()

    def run(self):
        self.loadConversation()
        self.sendSwapped()

    def reroll(self):
        self.c1.reroll()
        self.c2.reroll()
        self.conversation.append("------------------------------------------")

    def __del__(self):
        try:
           file = open(datetime.datetime.now().strftime('%d%m%Y%H%M%S.txt'), 'w')
        except:
            print("File open error")
        for i in self.conversation:
            file.write(i.frrom+": "+i.message+"\n")
        file.close()
    def isDc(self):
        return self.c1.dc or self.c2.dc



#driver = webdriver.Firefox()
#driver.get("https://www.omegle.com/")
#textButton = driver.find_element_by_id("textbtn")
#textButton.click()

con = Conn("Seba","Mati")
#regex = re.compile("^Stranger: ")
#if regex.match('Stranger is typing...'):
#    print("nd")
#else:
#    print('d')
while True:
    while(not con.isDc()):
        con.run()

        time.sleep(1)
        print([i.message for i in con.conversation])
    con.reroll()

