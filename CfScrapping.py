from bs4 import BeautifulSoup
import requests
import xlsxwriter
import os



#i/o files

UserIds = open('input.txt', 'r')


#Creating workbook and worksheet

workbook = xlsxwriter.Workbook(os.path.join(os.path.dirname(os.path.abspath(__file__)),"users.xlsx"))
worksheet = workbook.add_worksheet()
fmt = workbook.add_format(properties={'bold': False, 'font_color': 'red'})
ufmt = workbook.add_format(properties={'bold': True, 'font_color': 'blue'})

grow = 0
gcol = 0



# function to scrape user details

def scrapProfile(link, UserId, count):
	source = requests.get(str(link)).text
	soup = BeautifulSoup(source, 'lxml')
	info = soup.find('div', class_ = 'info')
	
	UserInfo = info.find('div', style = 'margin-top: 0.5em;').text
	UserRank = info.find('span', class_ = 'smaller').text
	
	InfoLis = UserInfo.split(',')
	
	worksheet.write(grow, gcol, count, ufmt)
	worksheet.write(grow, gcol+1, InfoLis[0] + "   " + UserRank, ufmt)
	
	print(UserInfo, 'User Rank:' + UserRank)
	try:
		sunmissionLink = f"https://codeforces.com/submissions/{UserId}"
		contestLink = f"https://codeforces.com/contests/with/{UserId}"
	except Exception as e:
			return
	
	trow = grow + 2;
	tcol = 0
	
	
	scrapSubmission(sunmissionLink, trow, tcol)
	scrapContests(contestLink, trow, tcol + 4)
	
	
	
	
# function to scrape user submissions

def scrapSubmission(link, trow, tcol):
	source = requests.get(str(link)).text
	soup = BeautifulSoup(source, 'lxml')
	tableout = soup.find('div', class_= 'datatable')
	tablein = tableout.find('table', class_ = 'status-frame-datatable')
	
	worksheet.write(trow, tcol, "Date", fmt)
	worksheet.write(trow, tcol+1, "Problem Solved", fmt)
	trow += 1
	
	
	datecount = {}
	tdate = ''
	for row in tablein.find_all('tr'):
		try:
			date = row.find('span', class_ = 'format-time').text
			p = ""
			for problem in row.find_all('a'):
				p = problem.text.strip()
			verdict = row.find('span', class_ = 'verdict-accepted').text
		except Exception as e:
			continue
		if(date[0:9] in datecount):
			if(verdict == 'Accepted'):
				datecount[date[0:9]] += 1
		else:
			if(verdict == 'Accepted'):
				datecount[date[0:9]] = 1
	for i in datecount:
		worksheet.write(trow, tcol, i)
		worksheet.write(trow, tcol+1, datecount[i])
		trow += 1



# function to scrape user Contest details

def scrapContests(link, trow, tcol):
	source = requests.get(str(link)).text
	soup = BeautifulSoup(source, 'lxml')
	tableout = soup.find('div', class_= 'datatable')
	tablein = tableout.find('table', class_ = 'tablesorter user-contests-table')
	
	worksheet.write(trow, tcol, "Contest", fmt)
	worksheet.write(trow, tcol+1, "Rank", fmt)
	worksheet.write(trow, tcol+2, "Solved", fmt)
	worksheet.write(trow, tcol+3, "Rating change", fmt)
	worksheet.write(trow, tcol+4, "New Rating", fmt)
	trow += 1
	
	
	for row in tablein.find_all('tr', limit = 10):
		lis = []
		try:
			for trd in row.find_all('td'):
				lis.append(trd.text.strip())
		except Exception as e:
			continue
		print(lis)
		if(len(lis) > 4):
			worksheet.write(trow, tcol, lis[1])
			worksheet.write(trow, tcol+1, lis[2])
			worksheet.write(trow, tcol+2, lis[3])
			worksheet.write(trow, tcol+3, lis[4])
			worksheet.write(trow, tcol+4, lis[5])
			trow += 1
	

#main function

lis = [line.strip() for line in open("input.txt", 'r')]
lis[0] = lis[0][1:len(lis[0])]
print(lis)
count = 0

for UserId in lis:
	try:
		profileLink = f"https://codeforces.com/profile/{UserId}"
	except Exception as e:
			continue
	count += 1
	scrapProfile(profileLink, UserId, count)
	grow += 15
	
UserIds.close()
workbook.close()


