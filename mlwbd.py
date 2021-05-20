# Author : @ycngmn ( Niloy
# Date Created : April 2021

## See the yts.py for hints to edit..


import asyncio
import requests as r 
from pyrogram import Client 
from bs4 import BeautifulSoup as bs
import os,time,aria2p,shutil,re,traceback
from imdb import IMDb,IMDbError

magic = 'aria2c --enable-rpc --rpc-listen-all=false --rpc-listen-port 6800  --max-connection-per-server=10 --rpc-max-request-size=1024M --seed-time=0 --min-split-size=10M --follow-torrent=true --split=10 --daemon=true --allow-overwrite=true'
os.system(magic) 

root = "/app/y" # Heroku XD

aria2x = aria2p.API(aria2p.Client(
	host="http://localhost",
	port=6800,
	secret=""))

bot = Client(
    "ytsbotx",
    api_id = 123455, #
    api_hash = "",
    bot_token=""
)

man = Client(
    "morrents",
    api_id = ,
    api_hash = "",
    phone_number = ''
)

channel = '@...' 
im = IMDb()

header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,
    'referer':'https://www.google.com/'
		}

exists=os.path.exists("movies.txt")
if not exists:
	f = open("movies.txt","w+")
	f.close()

namesx = []

while True:
	mlwbd = f"https://mlwbd.mobi/movie/"
	try:
		lm = r.get(mlwbd,headers=header)
	except r.exceptions.RequestException:
		time.sleep(15)
		print('System Restarted on req. error! ')
		os.system('python3 tmv.py')
	soup = bs(lm.content,"lxml")
	menus = soup.find("div",{'id':'archive-content'}).find_all('div',class_='data')
	
	for menu in menus:
		try:
			shutil.rmtree(root)
		except:
			pass
		os.mkdir(root)
		title = menu.find('a').text 
		pattern = '\(\d{4}\)'
		try:
			ititle = re.split(pattern,title)[0].strip(' ')
			year = re.findall(pattern,title)[0].strip('()')
		except:
			continue
		link = menu.find('a')['href']
		rlink = r.get(link).content
		ink = bs(rlink,"lxml")
		#imgx = ink.find('img',itemprop="image")['src']
		try:
			name = ink.find('b',class_="variante",text='Original title').find_next('span').text.strip(' ')
		except:
			name = ititle 
		try:
			pdl = ink.find('input',attrs={'type':'hidden'},value=re.compile('^https://techus.me'))['value']
		except:
			print(ititle)
			continue
		rpdl = r.get(pdl).content 
		dpg = bs(rpdl,"lxml")
		sp = r'\d*\.\d*GB|\d*GB|\d*MB|\d*\.\d*MB'
		#ep = "^(EP|Epi) \d*$|^(EP|Epi) \d*-\d*$|(Epi|Ep) —"                              
		dtxts = dpg.find_all('strong',text=re.compile(sp)) 
				
		for dtxt in dtxts[::-1]:
			info = dtxt.text 
			split = info.split( )
			size = split[0]
			try:
				o = re.search("[A-Z]",size).start()
			except:
				continue
			if size[o:]=='GB' and float(size[:o])>=1.9:
				continue 
			elif dtxt.find_next('a').find_previous('strong',text=re.compile(sp))!=dtxt:
				continue
			else:
				size = size[:o] + f" {size[o:]}"
				uri = dtxt.find_next('a')['href']
				uris = []
				uris.append(uri)
				ok = {"dir":root}
				z = open('movies.txt','r')
				x = z.read()
				data = x.split("\n")
				z.close()
				
				if (title not in data) and (name not in namesx) :
					ititlex = ititle + f" ({year})"
					try:
						sh = im.search_movie(ititlex)
						iid = sh[0].movieID
						imo = im.get_movie(iid) 
						syno = imo.get('plot')[0].split('::')[0]
						if len(syno) > 800:
						  syno = syno[:800]+'....'
						genre = imo.get('genre')[0]
						runtime = imo.get('runtime')[0] + ' Mins'
						ratings = imo.get('rating')
						#language = imo.get('languages')[0]
						img = imo.get('full-size cover url')
						imdb = 'https://www.imdb.com/title/tt'+iid	
					except :
						try:
							sh = im.search_movie(ititle)
							iid = sh[0].movieID
							imo = im.get_movie(iid) 
							syno = imo.get('plot')[0].split('::')[0]
							if len(syno) > 800:
								syno = syno[:800]+'....'
							genre = imo.get('genre')[0]
							runtime = imo.get('runtime')[0] + ' Mins'
							ratings = imo.get('rating')
							#language = imo.get('languages')[0]
							img = imo.get('full-size cover url')
							imdb = 'https://www.imdb.com/title/tt'+iid	
						except:
							f = open('movies.txt','a')
							f.write(title + '\n')
							f.close()
							traceback.print_exc()
							print(name)
							continue
					
					f = open('movies.txt','a')
					f.write(title + '\n')
					f.close()
					print(f"New movie Found — {name}")
					#print(uris[0])
					try:
						download = aria2x.add_uris(uris,options=ok)
					except Exception as e:
						print(e)
						continue 
					time.sleep(15)
					
					print("Downloading File...")
					thumb = r.get(img,allow_redirects=True)
					open('thumb.jpeg','wb').write(thumb.content)
				
					while True:
						r1x = os.listdir(root)
						try:
							vr = os.listdir(root)[0]
						except:
						  print('Download Error...! ')
						  aria2x.remove_all(force=True)
						  break
						
						if len(r1x)==1 and vr.endswith('.aria2')==False:
							print("File Downloaded..")
							r1 = os.listdir(root)[0]
							mf1 = os.path.join(root,r1)
							
							try:
								m1x = os.listdir(mf1)
								for filex in m1x:
									if filex.endswith(('.mp4','.mkv','.avi')):
										m1 = os.path.join(mf1,filex)
										filenm = filex
										#print(filenm)
										fname = filenm.replace("MLWBD.com","@Morrents")
							except NotADirectoryError:
								m1 = mf1
								fname = r1.replace("MLWBD.com","@Morrents")
							# Get type and quality from file_name
							if fname.endswith(('.mp4','.mkv','.avi'))!=True:
								print('Skipped for 2s download.. ! ')
								break
							tp = "Blu-Ray|BluRay|HDRip|BR-Rip|WEB-DL|HDCAMRip|Blu_Ray|WEB_DL|BR_Rip|PreDVD|Pre-DVD|WEBRip|WEB-HD|HDCAM"                 
							qp = "1080p|720p|480p"
							try:
								quality = re.findall(qp,fname)[0]
							except:
								quality = "Xp"
							try:
								type1 = re.findall(tp,fname)[0]
							except:
								try:
									type1 = re.findall(tp,title)[0]
								except:
									type1 = "Unknown"
							# If has any other name...
							if name != ititle:
								name = f"{ititle} | {name}"
							# Find languages in the filename
							rq = "Bangla|Hindi|English|Tamil|Malayalam|Malayala|French|Korean|KOREAN|Turkish|Spanish|Kannada|Telugu|Japanese|Chinese"                  
							lans = re.findall(rq,fname)
							language = ""
							for lan in lans:
								language += lan+' + '
							language = language.strip(" + ")
							if language == "":
								language = imo.get('languages')[0]
							# Telrgram Bot functions
							with bot: 
								mtext = f"🔥 <b>{name} ( {year} )</b>\n\n🎬 {syno}\n\n⚡️ {genre} | 🕒 {runtime} | ⭐️ {ratings}\n\n<a href='{imdb}'>IMDB</a> | Stay tuned and inspire ♥"
								f1text = f"🔥<b> {ititle}</b>\n⚡️ {quality} {type1} — {size} -<a href='{link}'>src</a>\n@Morrents | 🌍 {language}"
								print('Uploading Now...')		
								try:
									bot.send_photo(channel,img,caption=mtext,parse_mode='html')
									print('Sent Pic ! ')
									print('Trying to send video file... ')
									bot.send_document(channel,m1,caption=f1text,parse_mode='html',file_name=fname,thumb='/app/thumb.jpeg')
									print("Movie File sent..!")
									bot.send_sticker(channel,"CAACAgUAAxkBAAIBpGCGyXFavnFruAuCeCRJwDHXZRMRAAITAwACVPw5VJWnC7xljxRyHwQ")
									
								except Exception as e:
									print('File sending failed ! ')
									print(e)
									break
							#break
							with man:
								print("Forwarding to @Morrents")
								while True:
									target = man.get_history('@Morrents',limit=1,offset=0)
									parent = man.get_history('@Nckofry',limit=3,offset=0)
									
									if target[0].sticker!=None and parent[0].sticker!=None :
										mid = parent[-1].message_id
										fid = parent[-2].message_id
										man.copy_message('@Morrents','@Nckofry',mid)
										man.copy_message('@Morrents','@Nckofry',fid)
										man.send_sticker('@Morrents',"CAACAgUAAxkBAAIBpGCGyXFavnFruAuCeCRJwDHXZRMRAAITAwACVPw5VJWnC7xljxRyHwQ")
										print('Forwarded... :)') 
										namesx.append(name)
										break 
							
							print("Ran once succesfully!")
							break
				else:
					time.sleep(14)