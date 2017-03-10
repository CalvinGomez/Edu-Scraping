import requests
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

courseUrls = []
classroomCourseUrls = []
def get_course_urls():
	global courseUrls
	apiUrl = "https://udacity.com/public-api/v0/courses"
	httpResponse = requests.get(apiUrl)
	jsonResponse = httpResponse.json()
	for course in jsonResponse['courses']:
		url = course['homepage']
		urlWithoutParams = url[0:len(course['homepage'])-37]
		courseUrls.append(urlWithoutParams)

def get_classroom_course_urls():
	global classroomCourseUrls
	baseUrl = "https://classroom.udacity.com/courses/"
	for url in courseUrls:
		m = re.search('--(.*)', url)
		classroomCourseUrls.append(baseUrl + m.group(1))

def retrieve_all_courses_transcripts():
	driver = webdriver.Firefox()
	driver.get('https://auth.udacity.com/sign-in?next=https%3A%2F%2Fclassroom.udacity.com%2Fauthenticated')
	username = driver.find_element_by_xpath("//input[@type='email']")
	password = driver.find_element_by_xpath("//input[@type='password']")
	username.send_keys("calvingomezdev@gmail.com")
	password.send_keys("1dnaleel")
	driver.find_element_by_xpath("//button[@type='button']").click()
	try:
		catalog_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@title='Catalog']")))
	finally:
		for i in range(19,20):
			retrieve_course_transcripts(driver,classroomCourseUrls[i])

def retrieve_course_transcripts(driver, url):
	driver.get(url)
	# try:
	# 	pause_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='youtube-player--youtube-player--1kyG7']")))
	# finally:
	# 	pass

get_course_urls()
get_classroom_course_urls()
retrieve_all_courses_transcripts()