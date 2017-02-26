Prudentialv2
============

* Category : Cloud

* Link : http://54.202.82.13/

* Challenge:
	We fixed our challenge from two years ago.

The problem starts with simple login form accepting name and password which are authenticated by server from GET request parameter. On checking [this](https://github.com/swapnilgm/CTF-Writeups/blob/master/2017/BostonKeyParty/Prudentialv2/index.txt) is how page source looked like.Clearly it was appending flag to page on colliding SHA1 input to name and password field.

I google for SHA1 collision and came across <https://shattered.io/>. And i got to know that this was quick challenge based on SHA1 collision attack pdf published by google just day before CTF. Hats off to up-to date knowledge of designer.

So my attack was simple, just to pass both shattered pdf string mentioned on site to server as parameter. But it failed becuase of length limit on URI. 

Next thing I gone though the [paper](https://shattered.io/static/shattered.pdf). The both pdf were made from commmon prefix P (length 192) and two different nearly colliding SHA1 input byte stream (length 128) e.g [m1](https://github.com/swapnilgm/CTF-Writeups/blob/master/2017/BostonKeyParty/Prudentialv2/m1.txt) & [m2](https://github.com/swapnilgm/CTF-Writeups/blob/master/2017/BostonKeyParty/Prudentialv2/m2.txt). Suffix can be any payload of any length you want.
Using this information to minimize URI length I just attacked site with first 321 characters as input from both pdf. And response i got the flag.

Here is the code for [attack.py](https://github.com/swapnilgm/CTF-Writeups/blob/master/2017/BostonKeyParty/Prudentialv2/attack.py) :

	#!/usr/bin/python
	import hashlib
	import urllib

	with open('./shattered-1.pdf', 'r') as f:
    	passwd=f.read()

	with open('./shattered-2.pdf', 'r') as f:
    	name=f.read()

	def longest_common_prefix(seq1, seq2):
    	start = 0
    	while start < min(len(seq1), len(seq2)):
        	if seq1[start] != seq2[start]:
            	break
        	start += 1
    	return start



	i=longest_common_prefix(name,passwd)
	print 'longest_common_prefix : ', i

	with open('./m1.txt','r') as f:
    	m1 = f.read()[:-1].decode('hex')
   	   
	with open('./m2.txt','r') as f:
    	m2 = f.read()[:-1].decode('hex')
   	   
	assert name.find(m1) == i
	assert passwd.find(m2) == i

	i = i+len(m1)

	#verify sha1
	nm = hashlib.sha1()
	pw = hashlib.sha1()
	nm.update(name[:i])
	pw.update(passwd[:i])
	assert nm.digest() == pw.digest()

	params = { 'name': name[:i], 'password' : passwd[:i] }
	enparams = urllib.urlencode(params)

	req = urllib.urlopen("http://54.202.82.13/?"+ enparams)

	response = req.read()

	print response

Server responded with flag __FLAG{AfterThursdayWeHadToReduceThePointValue}__
