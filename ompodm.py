from selenium import webdriver
import dictionary
import threading
import time
from selenium import common
import re
import datetime



class messageRow():
    def __init__(self,mess,client):
        self.frrom = client
        self.message = mess
        self.time = time.time()


class Client():
    def __init__(self,name,driver):
        self.name = name
        self.driver = driver
        self.dc = False
        self.messages = []
        self.hms=0
        self.disconnBtn = self.driver.find_element_by_class_name("disconnectbtn")
        self.textarea = self.driver.find_element_by_class_name('chatmsg')
        self.sendbtn = self.driver.find_element_by_class_name('sendbtn')
    def loadMessages(self):
        if self.dc==False:
            self.messages = []
            logbox = self.driver.find_elements_by_class_name("strangermsg")
            regex = re.compile("^Stranger: ")
            for i in logbox:
                if(self.checkDc()):
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
            self.textarea = self.driver.find_element_by_class_name('chatmsg')
        self.textarea.clear()
        self.textarea.send_keys(text)
        self.sendbtn.click()
    def reroll(self):
        if self.dc:
            self.disconnBtn.click()
        else:
            self.disconnBtn.click()
            self.disconnBtn.click()
            self.disconnBtn.click()
        self.dc = False
    def checkDc(self):
        try:
            self.driver.find_element_by_class_name("newchatbtnwrapper")
        except common.exceptions.NoSuchElementException:
            return False
        return True

def fun(x):
        return x.time


class Conn():
    #TODO: StaleElementReferenceException at reconnect
    def __init__(self, nameClient1, nameClient2):
        d1 = webdriver.Firefox()
        d2 = webdriver.Firefox()
        d1.get("https://www.omegle.com/")
        d2.get("https://www.omegle.com/")
        textButton1 = d1.find_element_by_id("textbtn")
        textButton1.click()
        textButton2 = d2.find_element_by_id("textbtn")
        textButton2.click()

        self.c1 = Client(nameClient1,d1)
        self.c2 = Client(nameClient2,d2)
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
        self.conversation.append(messageRow("------------------------------------------",""))

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

con = Conn("S","M")


for i in range(10):
    while(not con.isDc()):
        con.run()

        time.sleep(1)
        print([i.message for i in con.conversation])
    con.reroll()

