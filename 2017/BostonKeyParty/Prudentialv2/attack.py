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

