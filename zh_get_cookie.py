# -*- conding:utf-8 -*-
import base64
import random
import time
from urllib import request

from selenium import webdriver
from selenium.webdriver import ChromeOptions

from YDMHTTP import identify


class Zhihu(object):

    def __init__(self):
        url = 'https://www.zhihu.com/signin?next=%2F'
        chrome_path = 'C:\Program Files (x86)\chromedriver\chromedriver.exe'
        # 构建一个模拟谷歌浏览器的配置文件
        self.option = ChromeOptions()
        # 添加开发者模式配置信息到配置文件
        # 即开启了Google Chrome的开发者模式，默认的js都会变成和真的浏览器登录一样，然后就是继续模拟输入用户名、密码和点击登录按钮
        self.option.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 将self.option添加到浏览器配置中启动
        self.driver = webdriver.Chrome(executable_path=chrome_path, chrome_options=self.option)
        self.driver.get(url)

    def __del__(self):
        self.driver.close()

    def get_pwd_login(self):
        t = random.uniform(0.5, 1)
        pwd_login = self.driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div[1]/div/form/div[1]/div[2]')
        pwd_login.click()
        time.sleep(1)
        username = self.driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div[1]/div/form/div[2]/div/label/input')
        username.send_keys('账号')
        time.sleep(t)
        password = self.driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div[1]/div/form/div[3]/div/label/input')
        password.send_keys('密码')
        time.sleep(t)
        try:
            image_code = self.driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div[1]/div/form/div[4]/div/span/div/img').get_attribute('src')
            # print(image_code)
            if 'null' not in str(image_code):
                '''
                # 截取整个网页图片
                self.driver.save_screenshot(r'./Images/zh_full.png')
                # 定位验证码位置
                image_code_input = self.driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div[1]/div/form/div[4]/div/div/div[1]/input')
                # 获取验证码x,y轴 尺寸
                location = image_code_input.location
                # 获取验证码的长和宽
                size = image_code_input.size
                # 截取的验证码位置坐标
                left, top, right, bottom = location['x'], location['y'], location['x']+size['width'], location['y'] + size['height']
                image_full = Image.open(r'./Images/zh_full.png')
                # 使用Image的crop函数，从截图中再次截取我们需要的区域
                image_code_pic = image_full.crop((left, top, right, bottom))
                '''
                # 定位验证码位置
                image_code_input = self.driver.find_element_by_xpath(
                    '//*[@id="root"]/div/main/div/div/div[1]/div/form/div[4]/div/div/div[1]/input')
                # 保存截取的验证码图片
                # image_code_pic = image_code_pic.convert('RGB')
                # image_code_pic.save('code.jpg')
                request.urlretrieve(image_code, './Images/zh_code.png')
                time.sleep(1)
                # 调用打码平台解析验证码，  缺少代码 如果打码平台解析错误需要做出判断并重新调用，且设置重调次数
                image_code_cont = identify(r'./Images/zh_code.png')
                image_code_input.send_keys(image_code_cont)
        except Exception as e:
            if '//*[@id="root"]' in str(e):
                pass
            else:
                print(e)
        try:

            zh_code_cn = self.driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div[1]/div/form/div[4]/div/div[2]/img').get_attribute('src')
            # print(zh_code_cn)
            if 'null' not in str(zh_code_cn):
                '''
                request.urlretrieve(zh_code_cn, './Images/zh_code_cn.png')
                time.sleep(5)  # 睡5秒-->人工点击（目前还没有好的解决方法）
                '''
                # 定位抓取文字验证码图片
                chinese_captcha_element = self.driver.find_element_by_class_name("Captcha-chineseImg")
                ele_postion = chinese_captcha_element.location
                x_relative = ele_postion["x"]
                y_relative = ele_postion["y"]
                browser_navigation_panel_height = 70
                base64_text = chinese_captcha_element.get_attribute("src")
                code = base64_text.replace("data:image/jpg;base64,", "").replace("%0A", "")
                fh = open("./Images/zh_code_cn.png", "wb")
                fh.write(base64.b64decode(code))
                fh.close()
                # 调用zheye库
                from zheye import zheye
                from mouse import move, click
                z = zheye()
                positions = z.Recognize('./Images/zh_code_cn.png')
                print(positions)
                last_position = []
                if len(positions) == 2:
                    if positions[0][1] > positions[1][1]:
                        last_position.append([positions[1][1], positions[1][0]])
                        last_position.append([positions[0][1], positions[0][0]])
                    else:
                        last_position.append([positions[0][1], positions[0][0]])
                        last_position.append([positions[1][1], positions[1][0]])
                    first_position = [int(last_position[0][0] / 2), int(last_position[0][1] / 2)]
                    second_position = [int(last_position[1][0] / 2), int(last_position[1][1] / 2)]
                    # +15 是x轴坐标上右移15，+30是y轴下移30
                    move(x_relative + first_position[0]+15,
                         y_relative + browser_navigation_panel_height + first_position[1]+30)
                    click()

                    move(x_relative + second_position[0]+15,
                         y_relative + browser_navigation_panel_height + second_position[1]+30)
                    click()

                else:
                    last_position.append([positions[0][1], positions[0][0]])
                    first_position = [int(last_position[0][0] / 2), int(last_position[0][1] / 2)]
                    move(x_relative + first_position[0]+15,
                         y_relative + browser_navigation_panel_height + first_position[1]+30)
                    click()
                print(last_position)
        except Exception as e:
            if '//*[@id="root"]' in str(e):
                pass
            else:
                print(e)
        time.sleep(3)
        login_button = self.driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div[1]/div/form/button')
        login_button.click()
        time.sleep(2)
        print('------------')
        # 获取cookie
        cookie = {}
        cookies = self.driver.get_cookies()
        for i in cookies:
            a = i['name']
            b = i['value']
            cookie[a] = b
        return cookie

    def main(self):
        cookie = self.get_pwd_login()
        return cookie


# if __name__ == '__main__':
#     zhihu = Zhihu()
#     zhihu.main()
