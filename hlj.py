# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import re
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

path=r'C:\Users\33119\Desktop\hljuSCalculate-master\s.txt'
class NotEqualException(Exception):
    '''
    Custom exception types
    '''
    def __init__(self,errorinfo,i,j):
        self.errorinfo = errorinfo
        Exception.__init__(self,errorinfo)
        self.i = i
        self.j = j
    def __str__(self):
        return self.errorinfo


def check(i,j):
	if i == j:
		return True
	else:
		return False

def postive(a,b):
	if b < 60 :
		return 0
	else:
		return a

def calc(a,b):
	a = postive(a,b) 
	return a*b


def websimulation():
	username=raw_input("[*]Username:")
	password=raw_input("[*]Passwrod:")
	driver = webdriver.Chrome()
	driver.get('http://ssfw2.hlju.edu.cn/ssfw/login/ajaxlogin.do')
	elemU = driver.find_element_by_xpath("//*[@id='j_username']")
	elemU.send_keys(username)
	elemP = driver.find_element_by_xpath("//*[@id='j_password']")
	elemP.send_keys(password)
	elemV = driver.find_element_by_xpath("//*[@id='validateCode']")
	verify=raw_input()
	elemV.send_keys(verify)
	elemC=driver.find_element_by_xpath("//*[@id='loginBtn']")
	elemC.click()
	time.sleep(2)
	js='window.open("http://ssfw2.hlju.edu.cn/ssfw/jwnavmenu.do?menuItemWid=0BCD80CE5AB5C8BBE0534B01DF7DDDE7");'
	driver.execute_script(js)
	normal_window = driver.current_window_handle
	all_Handles = driver.window_handles
	for pay_window in all_Handles:
		if pay_window != normal_window:
			driver.switch_to_window(pay_window)
	elem = driver.find_elements_by_xpath("/html/body/div[1]/div/div[2]/div[2]/div[1]/table/tbody")   
	#print elem[0].text
	f=open(path,"wb")
	f.write((elem[0].text).encode('UTF-8'))
	f.close()

def main():
	websimulation()
	total=0
	c = 0
	dic=[]
	score=[]
	a=[]
	b=[]
	f=open(path,"r")
	for i in f.readlines():
		for j in i.split():
			dic.append(j.decode("UTF-8"))
	f.close()
	for i in dic:
		value = re.compile('^(\\-|\\+)?\\d+(\\.\\d+)?$')
		result = value.match(i)
		if result:
			score.append(float(i))
		else:
			pass
	#print score,"\n\n"
	for i in range(len(score)/4):
		for j in range(0,4):
			if j%2 == 0 and j != 0:
				a.append(score[i*4+j])
			if j%3 == 0 and j != 0:
				b.append(score[i*4+j])
			else:
				pass
	try:
		switch=check(len(a),len(b))
		if switch == False:
			raise(NotEqualException(('NotEqual ERROR! :: The number of credits is not equal to the number of grades ==>> {0} and {1}'.format(len(a),len(b))),len(a),len(b)))
		else:
			for i,j in zip(range(len(a)),range(len(b))):
				total = total + calc(float(a[i]),float(b[j]))
				c =  c + postive(float(a[i]),float(b[j]))
			print "[*]Credit grade point:%f"%(total/c)
	except NotEqualException as e:
		print e





if __name__=='__main__':
	main()