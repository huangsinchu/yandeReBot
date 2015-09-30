import urllib,urllib2
import json
import os

save_dir = 'F:\\Picture\\yandeReBot'
domain = 'https://yande.re'

pixiv_dir = os.path.join(save_dir,"FromPixiv")
if not os.path.exists(pixiv_dir):
	os.makedirs(pixiv_dir)

def downloadimg(url,dir):
	list = url.split('/')
	tmp = list[-1]
	name = urllib.unquote(tmp)
	for i in ('\\','/',':','*','?','"','<','>','|'):
		name=name.replace(i,'-')
	conn = urllib2.urlopen(url)
	f = open(os.path.join(dir,name),'wb')
	f.write(conn.read())
	f.close()

url_post_json = domain+'/post.json?limit=1'
req_post = urllib2.urlopen(url_post_json)
json_post = req_post.read()
decodejson = json.loads(json_post)
new_id = decodejson[0]['id']

update_over = 0

ini_read = open("yandeReBot.ini",'a+')
old_id = ini_read.read()
if old_id=='':
	old_id = new_id-20
if int(old_id)==int(new_id):
	update_over = 1
if int(new_id)-int(old_id)>100:
	old_id = int(new_id)-100
ini_read.close()

if update_over:
	print "No new pictures."
else:
	print str(old_id)+" to "+str(new_id)

ini_write = open("yandeReBot.ini",'w')
ini_write.write(str(new_id))
ini_write.close()

page = 1
while update_over==0:
	url_post_json = domain+'/post.json?limit=20&page='+str(page)
	req_post = urllib2.urlopen(url_post_json)
	json_post = req_post.read()
	decodejson = json.loads(json_post)
	for item in decodejson:
		id = item['id']
		source = item['source']
		from_pixiv = (len(source and "pixiv")>4)
		if id>int(old_id):
			imgurl=item['file_url']
			print "downloading "+str(id)+" "+imgurl
			try:
				if from_pixiv:
					downloadimg(imgurl,pixiv_dir)
				else:
					downloadimg(imgurl,save_dir)
			except IOError,e:
				print "Fail to download "+str(id)
				print e
		else:
			update_over = 1
			break
	page=page+1
	
