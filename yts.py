# Author : @ycngmn ( Niloy 
# Date created : April 24, 2021 
# Tips : Run this script on a dedicated folder on a vps..

# Hint : * pyrogram to upload <2GB | *bs4 to scrap | *aria2 for torrents


import pyrogram
from pyrogram import Client
import requests as r
from bs4 import BeautifulSoup as bs
import os,time,aria2p,shutil

magic = 'aria2c --enable-rpc --rpc-listen-all=false --rpc-listen-port 6800  --max-connection-per-server=10 --rpc-max-request-size=1024M --seed-time=0 --min-split-size=10M --follow-torrent=true --split=10 --daemon=true --allow-overwrite=true'
root = "/root/x" # Folder to download
os.system(magic) 

aria2 = aria2p.API(
    aria2p.Client(
        host="http://localhost",
        port=6800,
        secret=""))

bot = Client(
    "ytsbotx",
    api_id = 123473, # Get from my.telegram.org
    api_hash = "", #   ^
    bot_token="" # @BotFather
)

man = Client(
    "morrents",
    api_id = 4465262, # Same as up
    api_hash = "", # Same as up
    phone_number="" # Phone_number of the account.
)

channel = '' # Channel Username/ID 

header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,
    'referer':'https://www.google.com/'
		}

clockx = time.strftime("%H:%M", time.localtime()) 

exists=os.path.exists("movies.txt")
if not exists:
	f = open("movies.txt","w+")
	f.close()


while True:
	try:
		shutil.rmtree(root)
	except:
		pass
	os.mkdir(root)
	try:
		listm = r.get('https://yts.mx/browse-movies',headers=header).content
	except r.exceptions.RequestException:
		time.sleep(15)
		print('System Restarted on req. error! ')
		os.system('python3 yts.py')
	lists = bs(listm,'lxml')
	movies = lists.find_all('div',class_="browse-movie-wrap col-xs-10 col-sm-4 col-md-5 col-lg-4")
	for movie in movies:
		name = movie.find('a',class_="browse-movie-title").text
		link = movie.find('a')['href']
		image = movie.find('img')['src'].replace('medium-cover','large-cover')
		year = movie.find('div',class_="browse-movie-year").text
		
		try:
			mainx = r.get(link).content
		except r.exceptions.RequestException:
			time.sleep(15)
			print('System Restarted on req. error! ')
			os.system('python3 yts.py')
		main = bs(mainx,'lxml')
		try:
			genrex = main.find('div',class_="visible-xs col-xs-20").find_all('h2')[1].text 
		except:
			genrex = "" 
		genre = genrex.split('/')[0]
		try:
			imdb = main.find('a',class_="icon",title="IMDb Rating")['href']
		except:
			imdb = ""
		try:
			rating = main.find('span',itemprop="ratingValue").text 
		except:
			rating = 'n/A'
		try:
			syno = main.find('p',class_="hidden-sm hidden-md hidden-lg").text 
		except:
			syno = ""
		if syno == "":
			syno = "No synopsis found on IMDB..! "
	
		if len(syno) > 800:
			syno = syno[:800]+'....'
		else:
			pass
		torx = main.find_all('div',class_="modal-torrent")
		try:
			tor1 = torx[0].find_all('a')[1]['href']
		except:
			continue
		file = main.find_all('div',class_="tech-spec-element col-xs-20 col-sm-10 col-md-5")
		hour,minute = file[6].text.strip().split(" hr ")
		try:
			length = str((60 * int(hour)) + int(minute.strip(" min"))) + " Mins"
		except ValueError:
			length = file[6].text 
			
		language1 = file[2].text.strip().split(" ")[0]
		quality1 = main.find_all('div',class_="modal-quality")[0].text
		type1 = main.find_all('p',class_="quality-size")[0].text
		sizex = main.find_all('p',class_="quality-size")[1].text
		sizel = sizex.split(" ")
		if sizel[1] == 'MB' :
			size = str(round(float(sizel[0]))) + f" {sizel[1]}"
		else:
			size = sizex
		mtext = f"🔥 <b>{name} ( {year} )</b>\n\n🎬 {syno}\n\n⚡️ {genre} | 🕒 {length} | ⭐️ {rating}\n\n<a href='{imdb}'>IMDB</a> | Stay tuned and inspire ♥"
		f1text = f"🔥<b> {name}</b>\n⚡️ {quality1} {type1} — {size} -<a href='{link}'>src</a>\n@Morrents | 🌍 {language1}"
			
		ok = {"dir":'/root/x'}
		
		z = open('movies.txt','r')
		x = z.read()
		data = x.split("\n")
		z.close()
		
		if name not in data :
			f = open('movies.txt','a')
			f.write(name + '\n')
			f.close()
			print(f"New movie Found — {name}")
			download = aria2.add_magnet(tor1,options=ok)
			time.sleep(10)
			clock = clockx
			print(f"Downloading File...  — {clock}")
			thumb = r.get(image,allow_redirects=True)
			open('thumb.jpeg','wb').write(thumb.content)
			
			timeout = time.time() + 600
			while True:
				if time.time() > timeout:
					print('Timed out..! Download took too long.. ! ')
					aria2.remove_all(force=True)
					#file_path = 'movies.txt'
					#os.system('sed -i "$ d" {0}'.format(file_path))
					shutil.rmtree(root)
					os.mkdir(root)
					print('Skipped this file..! ')
					break 
				else:
					pass
				r1x = os.listdir(root)
				if len(r1x)==1:
					clock = clockx
					print(f"File Downloaded..  — {clock}")
					
					r1 = os.listdir(root)[0]
					mf1 = os.path.join(root,r1)
					m1x = os.listdir(mf1)
					for filex in m1x:
						if filex.endswith(".mp4"):
							m1 = os.path.join(mf1,filex)
							filenm = filex
					fname = '@Morrents ' + filenm 
					
					with bot: # Thanks to pyrogram... :)
						print('Uploading Now...')
						try:
							bot.send_photo(channel,image,caption=mtext,parse_mode='html')
							print('Sent Pic ! ')
							print('Trying to send video file... ')
							bot.send_document(channel,m1,caption=f1text,parse_mode='html',file_name=fname,thumb='/root/yts/thumb.jpeg')
							clock = clockx
							print(f"Movie File sent..!  — {clock}")
							bot.send_sticker(channel,"CAACAgUAAxkBAAIBpGCGyXFavnFruAuCeCRJwDHXZRMRAAITAwACVPw5VJWnC7xljxRyHwQ")
						except Exception as e:
							print('File sending failed ! ')
							print(e)
					print("Deleting....")
					shutil.rmtree(root)
					os.remove('/root/yts/thumb.jpeg')
					os.mkdir(root)
					print("Ran once succesfully!")
					break
		else:
			time.sleep(20)