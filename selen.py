# coding:utf-8
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC



# 基类封装，单独建脚本base.py
class Base():
    def __init__(self, driver):
        self.driver = driver
        self.timeout = 30
        self.poll = 0.5

    def findElement(self, loctor):
        '''
        args:
        loctor 传元祖，如（"id","xx"）
        '''
        element = WebDriverWait(self.driver, self.timeout, self.poll).until(lambda x: x.find_element(*loctor))
        return element

    def findElementNew(self, loctor):
        # 找到了返回element，没找到抛异常
        element = WebDriverWait(self.driver, self.timeout, self.poll).until(EC.presence_of_element_located(loctor))
        return element

    def findElementsNew(self, loctor):
        # 找到了返回list, 没找到抛异常
        elements = WebDriverWait(self.driver, self.timeout, self.poll).until(EC.presence_of_all_elements_located(loctor))
        return elements

    def findElements(self, loctor):
        '''
        args:
        loctor 传元祖，如（"id","xx"）
        '''
        elements = WebDriverWait(self.driver, self.timeout, self.poll).until(lambda x: x.find_elements(*loctor))
        return elements

    def sendKeys(self, loctor, text):
        ele = self.findElement(loctor)
        ele.send_keys(text)

    def click(self, loctor):
        ele = self.findElement(loctor)
        ele.click()


# 封装登录页面 单独建脚本loginpage.py

class LoginPage(Base):
    '''登录页面'''
    user_loc = ("id", "account")  # 输入账号
    psw_loc = ("name", "password")  # 输入密码
    sub_loc = ("id", "submit")    # 点登录
    zhanghao_loc = ("css selector", "#userMenu>a")

    def open_login_page(self):
        self.driver.get("http://127.0.0.1:81/zentao/user-login.html")

    def logout(self):
        '''登出'''
        # driver = webdriver.Firefox()
        self.driver.delete_all_cookies() # 删除所有的cookies
        self.driver.refresh()

    def input_username(self,usrname):
        '''输入账号'''
        self.sendKeys(self.user_loc, usrname)

    def input_psw(self, psw):
        '''输入密码'''
        self.sendKeys(self.psw_loc, psw)

    def click_login_button(self):
        '''点击登录按钮'''
        self.click(self.sub_loc)

    def login(self,username="admin",psw="123456"):
        '''登录流程:'''
        self.open_login_page()
        self.input_username(username)
        self.input_psw(psw)
        self.click_login_button()

    def get_login_result(self):
        '''获取登录的结果'''
        try:
            t = self.findElement(self.zhanghao_loc).text
            return t
        except:
            print("登录失败！！！，返回空字符")
            return ""

# 封装提交BUG页面元素

class NewBug(Base):
    '''提交BUG页面'''
    test_tab_loc = ("xpath", ".//*[@id='mainmenu']/ul/li[4]/a")  # 测试tab
    bug_loc = ("link text", "Bug")  # Bug按钮
    add_bug_loc = ("xpath", ".//*[@id='createActionMenu']/a")  # 点提BUG
    title_loc = ("id", "title")                           # 标题
    body_loc = ("class name", "article-content")        # 正文
    save_loc = ("id", "submit")    # 保存
    truck_loc = ("class name", "chosen-choices")
    add_truck_loc = ("css selector",".active-result.highlighted")
    title = ("xpath", ".//*[@id='bugList']/tbody/tr[1]/td[4]")

    def click_test_tab(self):
        '''点Tab页切换：测试'''
        self.click(self.test_tab_loc)

    def click_bug(self):
        '''点加号'''
        self.click(self.bug_loc)

    def click_add_bug(self):
        self.click(self.add_bug_loc)

    def input_title(self, text):
        self.sendKeys(self.title_loc, text)

    def input_bug_detail(self, text):
        # 富文本里面输入内容
        self.driver.switch_to_frame(1)
        self.sendKeys(self.body_loc, text)
        self.driver.switch_to_default_content()

    def add_truk(self):
        # 影响版本
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

# 开始写提交BUG的一个流程

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
        # 以下步骤跟手工用例没啥区别，先把手工步骤写清楚，代码就是翻译的事情
        print("手工登录步骤，1.先打开登录页，2.输入账号3.密码，4.点登录")
        self.loginpa.login()  # 登录方法合成了手工的四步
        print("手工步骤点测试tab、点bug、点添加bug")
        self.addbug.click_test_tab()
        self.addbug.click_bug()
        self.addbug.click_add_bug()
        print("bug提交页面,输入tile,输入正文，点保存")
        # 考虑到bug不能重复提交，title加时间戳
        nowtime = time.strftime("%Y_%m_%d_%H_%M_%S")
        inputtitle = "提交一个BUG啦%s"%nowtime
        self.addbug.input_title(inputtitle)
        self.addbug.input_bug_detail("bug步骤1,2,3")
        print("勾选影响版本：truck")
        self.addbug.add_truk()
        self.addbug.click_save()
        print("bug提交完成后获取结果")
        result = self.addbug.get_bug_title()
        print("实际结果：%s" %result)
        # 判断输入的tile与列表里面的title
        self.assertTrue(inputtitle in result)
        
    def tearDown(self):
        self.loginpa.logout()
        
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
















