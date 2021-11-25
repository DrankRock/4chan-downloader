import requests, re, os, sys, getopt
from bs4 import BeautifulSoup

def help():
	print("hello there !")

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

def Main(url, isSingle, singleFolderName):
	#re.sub("[^a-zA-Z]+", "", "ABC12abc345def")
	#<div class="fileText"
	page = requests.get(url)
	soup = BeautifulSoup(page.content, "html.parser")
	name = soup.find_all("span", class_="subject")
	name = name[1]
	name = re.search('>(.*)<', str(name))
	name = name.group(1)
	listOfLinksToDownload = soup.find_all("div", class_="fileText")

	foldername = re.sub("[^a-zA-Z0-9]+", "", str(name))
	if isSingle:
		foldername=singleFolderName
	os.makedirs(foldername, exist_ok=True)
	lth = len(listOfLinksToDownload)
	for i in range(lth):
		printProgressBar(i, lth, prefix = 'Progress:', suffix = 'Complete', length = 25)
		link = re.search('<a href="//(.*)" target', str(listOfLinksToDownload[i])).group(1)
		downloadFileFromURL(foldername, link)
	printProgressBar(lth, lth, prefix = 'Progress:', suffix = 'Complete', length = 25)
	#<a href="//

def ifList(listfile, isSingle, singleFolderName):
	fileIn = open(listfile, 'r')
	Lines = fileIn.readlines()
	nline = len(Lines)
	i=1
	for line in Lines:
		print("[{}/{}] - Getting Files from {}".format(i,nline,line))
		Main(line, isSingle, singleFolderName)
		i+=1



def downloadFileFromURL(folder, url):
	folderToUse = folder
	splitted_URL = url.split("/")
	filename = splitted_URL[2]
	fileDir = os.path.dirname(os.path.realpath('__file__'))
	fileWfolder = "{}/{}".format(folderToUse, filename)
	filename = os.path.join(fileDir, fileWfolder)

	#print("folder : {}, url : {}, filename : {}, filedir : {}".format(folder, url, filename, fileDir))
	url = "http://{}".format(url)
	r = requests.get(url, allow_redirects=True)
	open(filename, 'wb').write(r.content)

def main(argv):
	# credit : https://www.tutorialspoint.com/python/python_command_line_arguments.htm
	try:
		opts, args = getopt.getopt(argv,"hu:l:sf:",["url=","list=","single-folder="])
	except getopt.GetoptError as err:
		print ('usage : ',err)
		sys.exit(2)
	useList=False
	for opt, arg in opts:
		if opt in ("-u", "--url"):
			url = arg
		elif opt in ("-l", "--list"):
			listOfLinks=arg
			useList=True
		elif opt in ("-sf", "--single-folder"):
			singleFolder=True
			singleFolderName=arg
		elif opt in ("-h", "--help"):
			help()
			sys.exit(2)
			

	if useList:
		ifList(listOfLinks, singleFolder, singleFolderName)
	else:
		Main(url, singleFolder, singleFolderName)

if __name__ == "__main__":
   main(sys.argv[1:])