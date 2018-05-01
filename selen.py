# coding:utf-8
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC



# �����װ���������ű�base.py
class Base():
    def __init__(self, driver):
        self.driver = driver
        self.timeout = 30
        self.poll = 0.5

    def findElement(self, loctor):
        '''
        args:
        loctor ��Ԫ�棬�磨"id","xx"��
        '''
        element = WebDriverWait(self.driver, self.timeout, self.poll).until(lambda x: x.find_element(*loctor))
        return element

    def findElementNew(self, loctor):
        # �ҵ��˷���element��û�ҵ����쳣
        element = WebDriverWait(self.driver, self.timeout, self.poll).until(EC.presence_of_element_located(loctor))
        return element

    def findElementsNew(self, loctor):
        # �ҵ��˷���list, û�ҵ����쳣
        elements = WebDriverWait(self.driver, self.timeout, self.poll).until(EC.presence_of_all_elements_located(loctor))
        return elements

    def findElements(self, loctor):
        '''
        args:
        loctor ��Ԫ�棬�磨"id","xx"��
        '''
        elements = WebDriverWait(self.driver, self.timeout, self.poll).until(lambda x: x.find_elements(*loctor))
        return elements

    def sendKeys(self, loctor, text):
        ele = self.findElement(loctor)
        ele.send_keys(text)

    def click(self, loctor):
        ele = self.findElement(loctor)
        ele.click()


# ��װ��¼ҳ�� �������ű�loginpage.py

class LoginPage(Base):
    '''��¼ҳ��'''
    user_loc = ("id", "account")  # �����˺�
    psw_loc = ("name", "password")  # ��������
    sub_loc = ("id", "submit")    # ���¼
    zhanghao_loc = ("css selector", "#userMenu>a")

    def open_login_page(self):
        self.driver.get("http://127.0.0.1:81/zentao/user-login.html")

    def logout(self):
        '''�ǳ�'''
        # driver = webdriver.Firefox()
        self.driver.delete_all_cookies() # ɾ�����е�cookies
        self.driver.refresh()

    def input_username(self,usrname):
        '''�����˺�'''
        self.sendKeys(self.user_loc, usrname)

    def input_psw(self, psw):
        '''��������'''
        self.sendKeys(self.psw_loc, psw)

    def click_login_button(self):
        '''�����¼��ť'''
        self.click(self.sub_loc)

    def login(self,username="admin",psw="123456"):
        '''��¼����:'''
        self.open_login_page()
        self.input_username(username)
        self.input_psw(psw)
        self.click_login_button()

    def get_login_result(self):
        '''��ȡ��¼�Ľ��'''
        try:
            t = self.findElement(self.zhanghao_loc).text
            return t
        except:
            print("��¼ʧ�ܣ����������ؿ��ַ�")
            return ""

# ��װ�ύBUGҳ��Ԫ��

class NewBug(Base):
    '''�ύBUGҳ��'''
    test_tab_loc = ("xpath", ".//*[@id='mainmenu']/ul/li[4]/a")  # ����tab
    bug_loc = ("link text", "Bug")  # Bug��ť
    add_bug_loc = ("xpath", ".//*[@id='createActionMenu']/a")  # ����BUG
    title_loc = ("id", "title")                           # ����
    body_loc = ("class name", "article-content")        # ����
    save_loc = ("id", "submit")    # ����
    truck_loc = ("class name", "chosen-choices")
    add_truck_loc = ("css selector",".active-result.highlighted")
    title = ("xpath", ".//*[@id='bugList']/tbody/tr[1]/td[4]")

    def click_test_tab(self):
        '''��Tabҳ�л�������'''
        self.click(self.test_tab_loc)

    def click_bug(self):
        '''��Ӻ�'''
        self.click(self.bug_loc)

    def click_add_bug(self):
        self.click(self.add_bug_loc)

    def input_title(self, text):
        self.sendKeys(self.title_loc, text)

    def input_bug_detail(self, text):
        # ���ı�������������
        self.driver.switch_to_frame(1)
        self.sendKeys(self.body_loc, text)
        self.driver.switch_to_default_content()

    def add_truk(self):
        # Ӱ��汾
        self.click(self.truck_loc)
        self.click(self.add_truck_loc)

    def click_save(self):
        self.click(self.save_loc)

    def get_bug_title(self):
        try:
            t = self.findElement(self.title).text
            return t
        except:
            return ""

# ��ʼд�ύBUG��һ������

import unittest
from selenium import webdriver
import time
class TestAddBug(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.loginpa = LoginPage(cls.driver)
        cls.addbug = NewBug(cls.driver)


    def test_add_bug_01(self):
        # ���²�����ֹ�����ûɶ�����Ȱ��ֹ�����д�����������Ƿ��������
        print("�ֹ���¼���裬1.�ȴ򿪵�¼ҳ��2.�����˺�3.���룬4.���¼")
        self.loginpa.login()  # ��¼�����ϳ����ֹ����Ĳ�
        print("�ֹ���������tab����bug�������bug")
        self.addbug.click_test_tab()
        self.addbug.click_bug()
        self.addbug.click_add_bug()
        print("bug�ύҳ��,����tile,�������ģ��㱣��")
        # ���ǵ�bug�����ظ��ύ��title��ʱ���
        nowtime = time.strftime("%Y_%m_%d_%H_%M_%S")
        inputtitle = "�ύһ��BUG��%s"%nowtime
        self.addbug.input_title(inputtitle)
        self.addbug.input_bug_detail("bug����1,2,3")
        print("��ѡӰ��汾��truck")
        self.addbug.add_truk()
        self.addbug.click_save()
        print("bug�ύ��ɺ��ȡ���")
        result = self.addbug.get_bug_title()
        print("ʵ�ʽ����%s" %result)
        # �ж������tile���б������title
        self.assertTrue(inputtitle in result)
        
    def tearDown(self):
        self.loginpa.logout()
        
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
















