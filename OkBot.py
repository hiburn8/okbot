#!/usr/bin/env python

import os, sys, urllib2, re, getopt, getpass
import mechanize
import cookielib
 
os.system('color 0d5')
print "\n\n"
print "		            ,;;;,   ,;;;,   "
print "		           ;;;;;;;,;;;;;;;  "
print "		  .:::.   .::::;;;;;;;;;;;  "
print "		 :::::::.:::::::;;;;;;;;;'  "
print "		 :::::::::::::::;;;;;;;'    "
print "		 ':::::::::::::';;;;;'      "
print "		   ':::::::::'   ';'        "
print "		     ':::::'                "
print "		       ':'      The-OkBot   "
print "		An OkCupid Popularity Bot \n"
print "		   hiburn8.org	  \n"

vote = True
message = True

dupes = 0
victims = []
target_img = 0
match_prefs = ""

'''OKCUPID STATUS CODES
2 = error/fail
7 = action completed
'''
  
#MECH SETUP
# Browser
br = mechanize.Browser()
# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)
# Browser options
br.set_handle_equiv(True)
#br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
# Want debugging messages?
#br.set_debug_http(True)
#br.set_debug_redirects(True)
#br.set_debug_responses(True)
# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36')]

while True:
	#open the login page
	r = br.open('http://www.okcupid.com/login')
	html = r.read()

	#try login
	#username = raw_input("Username:")
	email = raw_input("Email:")
	password = getpass.getpass()
	br.select_form(nr=0)
	br.form['username']=email
	br.form['password']=password
	br.submit()
	
	#did it work?
	url = br.geturl()
	if url == "http://www.okcupid.com/home":
		print "- Login OK\n"
		break
	else:
		print "- Login Failed\n"

#get the session cookie
for cookie in cj:
	if cookie.name == "session":
		matches = re.search("(\d+)%", cookie.value)
		myid = matches.group(1)
		print	"- Session Cookie = " +myid+ "\n"

#get auth token from link below
#<iframe id="ad_frame_leader" name="ad_frame_leader" class="ad" src="http://ads.okcimg.com/daisy?format=leader&amp;base=1&amp;page=Profile&amp;authid=1%2c0%2c1385959393%2c0x9de8f52697474c10%3bbada878632300f948aedf8d815320cf9262f1efb&amp;pageurl=%2fprofile&amp;cachebust=828512" width="0" height="0" marginwidth="0" marginheight="0" frameborder="0" scrolling="no" allowtransparency="true" style="display: none !important; visibility: hidden !important; opacity: 0 !important; background-position: 728px 90px;"></iframe>
r = br.find_link(url_regex=r".*authid=.*", nr=0)
auth = r.url
matches = re.search("authid=(.*)&force=", auth)
auth = matches.group(1)
print "- Authorisation Key = " +auth+ "\n"

#ready?
raw_input("Press ENTER to become popular!")

#find our matches
matchpage_url = "http://www.okcupid.com/match?filter1=0,34&filter2=2,18,99&filter3=5,3600&filter4=1,1&locid=0&timekey=1&matchOrderBy=RANDOM_SORT&custom_search=0&fromWhoOnline=0&mygender=m&update_prefs=0&sort_type=0&sa=1&using_saved_search=0&count=1"

while True:
	r = br.open( matchpage_url )
	r = br.find_link(url_regex=r".*\?cf=regular", nr=target_img)
	target = re.search("/.*/(.*)\?", r.url) 
	target = target.group(1)
	
	#prevent hitting the same target twice.
	if target not in victims:
		if target_img != 0:
			print "hacked our way out"
		victims.append(target)
		victim_c = len(victims)
		br.open(r.url)
		r = br.find_link(url_regex=r"javascript:processVoteNote.*")
		matches = re.search("'(\d+)'", r.url)
		targetid = matches.group(1)
		print "-Next victim = "+target+" ("+targetid+")(" +str(victim_c)+ ")("+str(dupes)+") vi="+str(target_img)
		
		if vote == True:
			#votelink = str("http://www.okcupid.com/vote_handler?voterid="+ myid +"&target_userid="+ targetid +"&type=vote&target_objectid=0&vote_type=personality&score=5")
			r = br.open(votelink)
			print "-Voted 5* because she's nice"
		
		
		if message == True:
			msg = "Any+room+in+your+heart+for+a+lonely+bot%3f"
			msglink = str("http://www.okcupid.com/mailbox?ajax=1&sendmsg=1&r1=" +target+ "&subject=&body=" +msg+ "&threadid=0&authcode="+auth+"&reply=0&from_profile=1")
			print msglink
			br.open(msglink)
			print "-Sent her a nice message too\n"
			
	else:
		dupes += 1
		if target_img == 1:
			target_img -= 1
		if target_img == 0:
			target_img += 1
		print "\n-Duplicate\n"
		
raw_input()
