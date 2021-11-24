import requests, re, os, sys, getopt
from bs4 import BeautifulSoup

# Print iterations progress
# Source : https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def Main(url):
	#re.sub("[^a-zA-Z]+", "", "ABC12abc345def")
	#<div class="fileText"
	page = requests.get(url)
	soup = BeautifulSoup(page.content, "html.parser")
	name = soup.find_all("span", class_="subject")
	name = name[1]
	name = re.search('>(.*)<', str(name))
	name = name.group(1)
	foldername = re.sub("[^a-zA-Z]+", "", str(name))
	listOfLinksToDownload = soup.find_all("div", class_="fileText")
	os.makedirs(foldername, exist_ok=True)
	lth = len(listOfLinksToDownload)
	for i in range(lth):
		printProgressBar(i, lth, prefix = 'Progress:', suffix = 'Complete', length = 25)
		link = re.search('<a href="//(.*)" target', str(listOfLinksToDownload[i])).group(1)
		downloadFileFromURL(foldername, link)
	printProgressBar(lth, lth, prefix = 'Progress:', suffix = 'Complete', length = 25)
	#<a href="//

def downloadFileFromURL(folder, url):
	splitted_URL = url.split("/")
	filename = splitted_URL[2]
	fileDir = os.path.dirname(os.path.realpath('__file__'))
	fileWfolder = "{}/{}".format(folder, filename)
	filename = os.path.join(fileDir, fileWfolder)

	#print("folder : {}, url : {}, filename : {}, filedir : {}".format(folder, url, filename, fileDir))
	url = "http://{}".format(url)
	r = requests.get(url, allow_redirects=True)
	open(filename, 'wb').write(r.content)

def main(argv):
	# credit : https://www.tutorialspoint.com/python/python_command_line_arguments.htm
	try:
		opts, args = getopt.getopt(argv,"u:l",["url=","list="])
	except getopt.GetoptError:
		print ('usage')
		sys.exit(2)
	useURL=False
	useList=False
	for opt, arg in opts:
		if opt in ("-u", "--url"):
			url = arg
			useURL=True
		elif opt in ("-l", "--list"):
			#Please note that list is currently not supported, it would take 10 minutes to do i'll do later.
			listOfLinks=arg
			useList=True
	Main(url)

if __name__ == "__main__":
   main(sys.argv[1:])