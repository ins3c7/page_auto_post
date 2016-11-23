#!/usr/bin/python2
# -*- coding: utf-8 -*-
#

import json, os, sys
from time import sleep
from requests import get
from random import choice
from time import strftime as hour
from unidecode import unidecode as uni
from BeautifulSoup import BeautifulSoup as bs
from urllib2 import urlopen
from facebook import GraphAPI
from imgurpython import ImgurClient
from sys import argv
from getopt import getopt, GetoptError

class pageAdmin:

	def __init__(self, Fb, Imgur, pages):

		self.CE = '\033[0;0m';self.C0 = '\033[30m';self.C1 = '\033[31m';
		self.C2 = '\033[32m' ;self.C3 = '\033[33m';self.C4 = '\033[34m';
		self.C5 = '\033[35m' ;self.C6 = '\033[36m';self.C7 = '\033[37m'

		self.Fb = Fb
		self.Imgur = Imgur
		self.pages = pages
		self.verbose = False

		self.ids = ['438620006179122','234651986592310','367610546620931','432230166819904','694681767257295','174285109336431','235263107772','369050369891030','351126731639471','188829707806974','1405490743018716','165680880233643','201343919944885']

		if len(argv[1:]):
			try:
				opts, args = getopt(argv[1:],'v', ['verbose'])
			except GetoptError as err:
				print str(err)

			for o, a in opts:
				if o in ('-v', '--verbose'):
					self.verbose = True
				else:
					assert False,'Opção desconhecida'




	def getID(self, pageName):
		if self.verbose:
			print self.C0 +'[+]'+ self.CE +' Getting ID for page', pageName
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
		url = 'https://www.facebook.com/'+ pageName
		data = get(url, headers=headers)

		id = data.text.split('"page_id":')[1].split('}]')[0]
		
		if len(id) > 30:
			id = data.text.split('?page_id=')[1].split('&')[0]

		return id

	def imgur(self, link):
		if self.verbose:
			print self.C0 +'[+]'+ self.CE +' Uploading for Imgur...'
		return self.Imgur.upload_from_url(link, config=None, anon=True)['link']

	def parser(self, id):
		if self.verbose:
			print self.C0 +'[+]'+ self.CE +' Getting data...'
		return self.Fb.get_object(id=id, fields='posts.limit(15){attachments},feed.limit(15){full_picture, message}')

	def publish(self, msg, attachment):
		self.Fb.put_wall_post(message=msg, attachment=attachment)
		if self.verbose:
			print '\n'+ self.C5 +'[+] Published!', self.CE, '\n'

	def sortLink(self):
		if self.verbose:
			print self.C0 +'[+]'+ self.CE +' Sorting Page...'
		link_posted = open('link_posted.txt', 'r').readlines()
		base = []
		while len(base) < 1:
			try:
				id = choice(self.ids)
				data = self.parser(id)['posts']['data']

				for post in data:
					try:
						if len(post['attachments']['data'][0]['target']['url']) > 200:
							description = (post['attachments']['data'][0]['description']).encode('utf-8')
							link = post['attachments']['data'][0]['target']['url']

							if (description+'\n') in link_posted:
								continue

							base.append([description, link])

					except:
						continue

			except Exception, e:
				if self.verbose:
					print str(e)
				pass

		description, link = choice(base)
		
		append_file = open('link_posted.txt', 'a')
		append_file.write(description+'\n')
		append_file.close()
		if self.verbose:
			print '\n'+ self.C2 +'[+] Saved Link and Description.', self.CE

		return description, link

	def sortImage(self):
		if self.verbose:
			print self.C0 +'[+]'+ self.CE +' Sorting Image...'
		image_posted = open('image_posted.txt', 'r').readlines()
		base = []
		while len(base) < 1:
			try:
				# id = self.getID(choice(self.pages))
				id = choice(self.ids)
				data = self.parser(id)['feed']['data']

				for post in data:
					try:
						description = post['message']
						picture = post['full_picture']

						if (picture+'\n') in image_posted:
							continue

						base.append([description, picture])

					except:
						continue
			except Exception, e:
				if self.verbose:
					print str(e)
				pass

		description, picture = choice(base)

		append_file = open('image_posted.txt', 'a')
		append_file.write(picture+'\n')
		append_file.close()
		if self.verbose:
			print '\n'+ self.C2 +'[+] Saved Link and Picture.', self.CE

		return description, picture

	def postLink(self):
		if self.verbose:
			print '\n'+ self.C0 +'[+]'+ self.C4 +' Post Link Function, Initializing...'+ self.CE +'\n'
		description, link = self.sortLink()
		attachment = {'link':link, 'caption':'VIDA | VIA LARISSA LUTHAI'}
		self.publish(description, attachment)

	def postPicture(self):
		if self.verbose:
			print '\n'+ self.C0 +'[+]'+ self.C4 +' Post Picture Function, Initializing...'+ self.CE +'\n'
		description, picture = self.sortImage()
		picture = urlopen(picture)
		self.Fb.put_photo(picture, message=description +' / Curta e compartilhe nossa pagina! <3')
		if self.verbose:
			print '\n'+ self.C5 +'[+] Published!', self.CE, '\n'

	def main(self):
		# while 1:
		self.postPicture()
		# 	sleep(1000)

		hr_pic  = ['0720', '0830', '1030', '1130', '1215', '1230', '1300', '1400', '1610', '1745', '1815', '1850', '1930', '2000', '2008', '2030', '2130', '2155', '2215', '2230', '2300', '2330', '2345']
		hr_link = ['1010', '1200', '1710', '1910', '2010', '2230']

		hr_all = hr_pic + hr_link
		
		while True:
			hr = hour('%H%M')

			self.postLink()
			
			sorted(hr_all)
			
			next_post = []
			
			for h in hr_all:
				if hr < h:
					next_post.append(h)
					break
			if len(next_post) < 1:
				if self.verbose:
					print '\r'+'[+] No have more posts for today.'+ self.C7 +' / NOW: '+ hr[0:2] +':'+ hr[2:] +' / '+ self.CE, 'Next post tomorrow:', hr_all[0][0:2] +':'+ hr_all[0][2:], ' ',
				sys.stdout.flush()
				sleep(10)
				continue

			if self.verbose:
				print '\r'+ self.C4 +'[ONLINE] '+ self.C1 +'[FACEBOOK PAGE ADMIN] '+ self.C7 +'/ NOW: '+ hr[0:2] +':'+ hr[2:] +' / '+ self.CE +'Next post:'+ self.C2, next_post[0][0:2] +':'+ next_post[0][2:] +'h ', self.CE,
			sys.stdout.flush()

			if hr in hr_pic:
				try:
					print
					self.postPicture()
					sleep(60)
					print
				except Exception, e:
					if self.verbose:
						print 'POSTPIC ERROR', str(e)
					pass

			elif hr in hr_link:
				try:
					print
					self.postLink()
					sleep(60)
					print
				except Exception, e:
					if self.verbose:
						print 'POSTLINK ERROR', str(e)

			sleep(5)

if __name__ == '__main__':
	os.system('clear')

	conf = json.load(open(os.path.abspath('')+'/config.conf'))
	pages = open('names.txt', 'r').readlines()
	
	Fb = GraphAPI(conf['fb_token'], version=2.5)
	Imgur = ImgurClient(conf['imgur_client_id'], conf['imgur_client_secret'], conf['imgur_access_token'], conf['imgur_refresh_token'])

try:
	page = pageAdmin(Fb, Imgur, pages)
	page.main()
except Exception, e:
	print
	print 'ERROR IN ROOT:', str(e)
	print