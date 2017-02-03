import json
import urllib.request
from bs4 import BeautifulSoup

def loadAllCourses():
	global json_response
	response = urllib.request.urlopen(urllib.request.Request('https://udacity.com/public-api/v0/courses'))
	json_response = json.loads(response.read().decode('utf-8'))

def printAllCourses():
	for course in json_response['courses']:
		print(course['title'] + ": " + course['homepage'] + "\n")

def getLessonDetails(url, i):
	htmlfile = urllib.request.urlopen(urllib.request.Request(url))
	htmltext = htmlfile.read()
	soup = BeautifulSoup(htmltext, "html.parser")
	course_type = IsLessonOrSyllabusOrHidden(soup, url)
	print(course_type)
	if course_type == "lesson":
		handleLesson(soup, url, i)
		# pass
	elif course_type == "syllabus":
		handleSyllabus(soup, url, i)
		# pass
	elif course_type == "hidden":
		# handleHidden(soup, url)
		pass

def handleLesson(soup, url, index):
	card_lessons = soup.find_all("a", class_="card--lesson")

	all_lesson_names = []
	all_lesson_descriptions = []
	for card in card_lessons:
		lesson_names = card.div.find_all(text=True)
		lesson_names = remove_values_from_list(lesson_names, '\n')
		for i in range(0, len(lesson_names)):
			lesson_names[i] = lesson_names[i].rstrip()
		all_lesson_names.append("\"" + lesson_names[1] + "\"")

	for card in card_lessons:
		lesson_descriptions = card.ul.find_all(text=True)
		lesson_descriptions = remove_values_from_list(lesson_descriptions, '\n')
		for i in range(0,len(lesson_descriptions)):
			lesson_descriptions[i] = lesson_descriptions[i].rstrip()
		lesson_descriptions = ".".join(lesson_descriptions)
		all_lesson_descriptions.append("\"" + lesson_descriptions + "\"")

	for i in range(0,len(all_lesson_names)):
		f.write(str(index) + "," + all_lesson_names[i] + "," + all_lesson_descriptions[i] + "\n")

def handleSyllabus(soup, url, index):
	syllabus_content = soup.find_all("div", class_="syllabus__content")
	lesson_names_tags = syllabus_content[0].find_all("h3")
	lesson_desc_tags = syllabus_content[0].find_all("p")
	lesson_desc_tags_ul = syllabus_content[0].find_all("ul")
	all_lesson_descriptions = []
	all_lesson_names = []

	for x in lesson_names_tags:
		temp = x.find_all(text=True)
		temp = remove_values_from_list(temp, '\n')
		for i in range(0,len(temp)):
			temp[i] = temp[i].rstrip()
		all_lesson_names.append("\"" + temp[0] + "\"")
	
	if len(lesson_desc_tags) == 0:
		for x in lesson_desc_tags_ul:
			temp = x.find_all(text=True)
			temp = remove_values_from_list(temp, '\n')
			for i in range(0,len(temp)):
				temp[i] = temp[i].rstrip()
			complete_desc = ". ".join(temp)
			all_lesson_descriptions.append("\"" + complete_desc + "\"")
	else:
		for x in lesson_desc_tags:
			temp = x.find_all(text=True)
			temp = remove_values_from_list(temp, '\n')
			for i in range(0,len(temp)):
				temp[i] = temp[i].rstrip()
			all_lesson_descriptions.append("\"" + temp[0] + "\"")

	if len(all_lesson_names) != len(all_lesson_descriptions):
		print("Mismatch")
	else:
		for i in range(0,len(all_lesson_names)):
			f.write(str(index) + "," + all_lesson_names[i] + "," + all_lesson_descriptions[i] + "\n")

def handleHidden(soup, url):
	pass

def getAllLessonsDetails(typeOf, upperBound):
	global f
	f = open('udacity_course_lessons.csv', 'w')
	if typeOf == "single":
		print(json_response['courses'][upperBound]['homepage'])
		print(upperBound)
		getLessonDetails(json_response['courses'][upperBound]['homepage'])
		print("\n")
	else:
		i = 0
		for url in json_response['courses'][0:upperBound]:
			print(url['homepage'])
			print(i)
			getLessonDetails(url['homepage'], i)
			print("\n")
			i = i + 1
	f.close()

def getAllCourseTitles():
	c = open('udacity_course_details.csv', 'w')
	j = 0
	for course in json_response['courses']:
		c.write(str(j) + "," + "\"" + course['key'] + "\"" + "," + "\"" + course['title'] + "\"" + "\n")
		j = j + 1
	c.close()

def IsLessonOrSyllabusOrHidden(soup, url):
	lesson = soup.find_all("section", class_="lessons")
	syllabus = soup.find_all("section", class_="syllabus")
	hidden = soup.find_all("div", attrs={"data-ng-class" : "{'hidden-xs': !showSyllabus}"})

	if len(lesson) == 1:
		return "lesson"
	elif (len(syllabus) == 1):
		return "syllabus"
	elif (len(hidden) == 1):
		return "hidden"

def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]

loadAllCourses()
getAllCourseTitles()
getAllLessonsDetails("", len(json_response['courses']))