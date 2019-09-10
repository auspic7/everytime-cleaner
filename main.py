import tkinter as tk
from tkinter import messagebox
import selenium
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import os

from selenium.webdriver.support.wait import WebDriverWait

print(os.getcwd())



class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey'):
        super().__init__(master)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.checkVar1 = tk.IntVar()
        self.checkVar2 = tk.IntVar()
        self.create_widgets()

    def create_widgets(self):
        self.username = EntryWithPlaceholder(self, "username", 'blue')
        self.username.pack(side="top")
        self.password = EntryWithPlaceholder(self, "password", 'blue')
        self.password.pack(side="top")

        self.article_option = tk.Checkbutton(self, variable=self.checkVar1)
        self.article_option["text"] = "글 다 지우기"
        self.article_option.pack(side="top")

        self.comment_option = tk.Checkbutton(self, variable=self.checkVar2)
        self.comment_option["text"] = "댓글 다 지우기"
        self.comment_option.pack(side="top")

        self.checkVar1.set(1)
        self.checkVar2.set(1)

        self.start_button = tk.Button(self)
        self.start_button["text"] = "시작"
        self.start_button["command"] = self.start_delete
        self.start_button.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def start_delete(self):
        print("Action Started")
        deleted_comment, deleted_article = 0, 0

        # get module
        browser = webdriver.Chrome(os.getcwd() + '/chromedriver')

        # get login page
        browser.get("https://everytime.kr/login")

        # login
        browser.find_element_by_xpath('//*[@id="container"]/form/p[1]/input').send_keys(self.username.get())
        browser.find_element_by_xpath('//*[@id="container"]/form/p[2]/input').send_keys(self.password.get())
        browser.find_element_by_xpath('//*[@id="container"]/form/p[3]/input').click()

        if self.checkVar1:
            # get myarticle page
            browser.get("https://everytime.kr/myarticle")
            try:
                while True:
                    WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="container"]/div[2]/article[1]/a'))).click()
                    WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.CLASS_NAME, 'del'))).click()  # del button click
                    Alert(browser).accept()
                    deleted_article += 1
                    browser.get("https://everytime.kr/myarticle")
            except selenium.common.exceptions.NoSuchElementException:
                pass
            except TimeoutException:
                print("Loading took too much time!")

        if self.checkVar2:
            browser.get("https://everytime.kr/mycommentarticle")
            try:
                while True:
                    WebDriverWait(browser, 2).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="container"]/div[2]/article[1]/a'))).click()  # topmost article click

                    try:
                        while True:
                            WebDriverWait(browser, 1).until(
                                    EC.presence_of_element_located((By.CLASS_NAME, 'del'))).click()  # del button click
                            Alert(browser).accept()
                            deleted_comment += 1
                            time.sleep(0.5)

                    except selenium.common.exceptions.NoSuchElementException:
                        pass
                    except TimeoutException:
                        print("달린 댓글을 전부 삭제했습니다")
                    except selenium.common.exceptions.NoAlertPresentException:
                        pass
                    browser.get("https://everytime.kr/mycommentarticle")
            except selenium.common.exceptions.NoSuchElementException:
                pass
            except TimeoutException:
                print("댓글을 전부 삭제했습니다")

        tk.messagebox.showinfo("완료", "%d개의 글과 %d개의 글을 삭제했습니다" % (deleted_article, deleted_comment), parent=root)


root = tk.Tk()
app = Application(master=root)
app.mainloop()

