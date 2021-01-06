import requests
from urllib import request
from http import cookiejar
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import Select
import json
from selenium.webdriver.common.keys import Keys
import time
from  sendemail import mail

class loginfo:
	mail_addr = ""
	mail_content = ""




def sign():
	with open('config.json', 'r',encoding='utf-8') as f:
		config = json.load(f)

	print_log("本次打卡的详细信息：")
	for key in config.keys():
		print_log(key + ": " + config[key])



	loginfo.mail_addr = config["mailnotifation"]

	user_val = config["user"]
	password_val = config["passwd"]
	reason_val = config["reason"]
	major_val = config["major"]
	grade_val = config["grade"]
	counselor_val = config["counselor"]
	department_val = config["department"]
	room_val = config["room"]
	province_val = config["province"]
	city_val = config["city"]
	part_val = config["part"]
	detail_val = config["detail"]

	location_val = config["location"]
	character_val = config["character"]
	phone_number_val = config["phone"]


	url_login = 'https://ehall.jlu.edu.cn/taskcenter/'

	chrome_options = Options()
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--disable-dev-shm-usage')
	from selenium import webdriver
	driver = webdriver.Chrome(chrome_options=chrome_options)
	print_log("Chrome启动成功")
	driver.get(url_login)
	print_log("获取登录页")
	time.sleep(2)
	driver.find_element_by_id('username').clear()
	driver.find_element_by_id('password').clear()

	driver.find_element_by_id('username').send_keys(user_val)
	driver.find_element_by_id('password').send_keys(password_val)
	driver.find_element_by_id('login-submit').click()
	time.sleep(2)
	print_log("登陆成功，获取taskcenter")

	response = driver.get(url_login)
	time.sleep(10)


	while len(driver.find_elements_by_link_text("研究生每日健康打卡")) <= 0:
		print_log("未能成功进入taskcenter，正在重试")
		driver.get(url_login)
		time.sleep(10)

	driver.find_elements_by_link_text("研究生每日健康打卡")[0].click()
	windows = driver.window_handles
	driver.switch_to.window(windows[1])
	print_log("尝试关闭空白标签页")
	driver.close()
	driver.switch_to.window(windows[2])
	print_log("切换至打卡标签页，获取表单")
	time.sleep(10)
	if not driver.find_elements_by_id('V1_CTRL40')[0].is_displayed():
		print_log("当前时间段已打卡，请勿重复提交")
		return True , '[{0}]:{1}'.format(get_now_time(), "当前时间段已打卡，请勿重复提交")

	driver.find_element_by_id('V1_CTRL40').clear()
	driver.find_element_by_id('V1_CTRL40').send_keys(major_val)
	time.sleep(1)


	phone_number = driver.find_elements_by_name('fieldSQsjh')[0]
	phone_number.clear()
	phone_number.send_keys(phone_number_val)

	counselor1 = driver.find_elements_by_id('V1_CTRL68_Container')[0]
	counselor1.click()
	counselor = driver.find_element_by_xpath('//*[@class="infoplus_control active_input validate[funcCall[checkRenderFormFields]] active_input_focus"]')

	for _ in range(10):
		counselor.send_keys(Keys.BACKSPACE)

	counselor.send_keys(counselor_val)

	if location_val == 'school':
		driver.find_elements_by_id('V1_CTRL63')[0].click()
		stay_reason = Select(driver.find_element_by_name('fieldXNSY'))
		department = Select(driver.find_element_by_id("V1_CTRL7"))
		department.select_by_visible_text(department_val)

		room = (driver.find_element_by_id('V1_CTRL8'))
		room.clear()
		room.send_keys(room_val)


		submit = driver.find_element_by_id('V1_CTRL28')

	else:
		# 校外居住
		driver.find_elements_by_id('V1_CTRL64')[0].click()
		stay_reason = Select(driver.find_element_by_name('fieldXWSY'))

		location = driver.find_elements_by_id('V1_CTRL35_Container')[0]
		location.click()
		location = driver.find_element_by_xpath(
			'//*[@class="infoplus_control active_input validate[funcCall[checkRenderFormFields]] active_input_focus"]')

		for _ in range(10):
			location.send_keys(Keys.BACKSPACE)

		location.send_keys(province_val)
		time.sleep(2.8)

		driver.find_element_by_xpath('//*[@class="infoplus_suggester_item suggest_selected"]').click()

		time.sleep(2.8)

		location = driver.find_elements_by_id('V1_CTRL37_Container')[0]
		location.click()
		location = driver.find_element_by_xpath(
			'//*[@class="infoplus_control active_input validate[funcCall[checkRenderFormFields]] active_input_focus"]')

		for _ in range(10):
			location.send_keys(Keys.BACKSPACE)

		location.send_keys(city_val)
		time.sleep(2.8)
		driver.find_elements_by_xpath('//*[@class="infoplus_suggester_item suggest_selected"]')[1].click()
		time.sleep(2.8)

		location = driver.find_elements_by_id('V1_CTRL38_Container')[0]
		location.click()
		location = driver.find_element_by_xpath(
			'//*[@class="infoplus_control active_input validate[funcCall[checkRenderFormFields]] active_input_focus"]')

		for _ in range(10):
			location.send_keys(Keys.BACKSPACE)

		location.send_keys(part_val)
		time.sleep(2.8)
		driver.find_elements_by_xpath('//*[@class="infoplus_suggester_item suggest_selected"]')[2].click()
		time.sleep(2.8)
		driver.find_element_by_id("V1_CTRL39").clear()
		driver.find_element_by_id("V1_CTRL39").send_keys(detail_val)

		driver.find_element_by_id("V1_CTRL66").click()

		submit = driver.find_elements_by_xpath('//*[@class="command_li color0"]')



	stay_reason.select_by_visible_text(reason_val)






	grade = Select(driver.find_element_by_name('fieldSQnj'))
	grade.select_by_visible_text(grade_val)

	# if
	if character_val == 'master':
		driver.find_element_by_id('V1_CTRL44').click()
	else:
		driver.find_element_by_id('V1_CTRL45').click()

	submit.click()


	driver.find_elements_by_link_text("提交")[0].click()



	time.sleep(2)
	print_log("提交成功")
	driver.find_element_by_xpath('//*[@class="dialog_button default fr"]').click()
	time.sleep(1)

	driver.find_element_by_xpath('//*[@class="dialog_button default fr"]').click()
	driver.quit()
	return True , '[{0}]:{1}'.format(get_now_time(), "任务完成")
		

		
		
def get_now_time():
    time_array = time.localtime()
    return time.strftime('%Y-%m-%d %H:%M:%S', time_array)
import os
def print_log(log):
    info = '[{0}]:{1}'.format(get_now_time(), log)
    loginfo.mail_content += "\n\r"
    loginfo.mail_content += info
    print(info)
    #os.system('echo "' + info + '" >> D:\\my program\\daka\\signlog.txt')

import datetime

def time_satisfied():

    if datetime.datetime.now().hour >= 7 and datetime.datetime.now().hour <= 11:
        return 1 , True
    if datetime.datetime.now().hour >= 20 and datetime.datetime.now().hour < 23:
        return 2 , True

    return 0 , False

if __name__ == '__main__':

	sign_log = [True , False , False]
	while True:
		if datetime.datetime.now().hour >= 0 and datetime.datetime.now().hour <= 3:
			sign_log = [True , False , False]
		timerange , sat = time_satisfied()
		if not sign_log[ timerange ] and sat:
			loginfo.mail_content = "-- 最后一行提示任务完成即打卡成功. --"
			try:
				_ , re = sign()
				#mail(re , mail_addr)
				print_log("完成")
				sign_log[ timerange ] = True
			except Exception as e:
				log = ("Exception-{0}".format([e]))
				print_log(log)
				#mail(log , mail_addr)
			print_log("出现问题请至https://github.com/ShiningDeadFishEyes/daka/issues提交issue.")
			mail(loginfo.mail_content , loginfo.mail_addr)
		print_log("heartbeat - "  +str(sign_log))
		time.sleep(300)

