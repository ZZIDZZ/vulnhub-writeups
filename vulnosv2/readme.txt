PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.6 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   1024 f5:4d:c8:e7:8b:c1:b2:11:95:24:fd:0e:4c:3c:3b:3b (DSA)
|   2048 ff:19:33:7a:c1:ee:b5:d0:dc:66:51:da:f0:6e:fc:48 (RSA)
|   256 ae:d7:6f:cc:ed:4a:82:8b:e8:66:a5:11:7a:11:5f:86 (ECDSA)
|_  256 71:bc:6b:7b:56:02:a4:8e:ce:1c:8e:a6:1e:3a:37:94 (ED25519)
80/tcp   open  http    Apache httpd 2.4.7 ((Ubuntu))
|_http-title: VulnOSv2
| http-methods: 
|_  Supported Methods: POST OPTIONS GET HEAD
|_http-server-header: Apache/2.4.7 (Ubuntu)
6667/tcp open  irc     ngircd

3 open ports, ssh, http, and an irc port

further investigating the http page with nikto or gospider, we found a url that leads to /jabc/

we explore further and found that robots.txt is present and is excluding many urls, here are the most interesting ones:
# Paths (no clean URLs)
Disallow: /?q=admin/
Disallow: /?q=comment/reply/
Disallow: /?q=filter/tips/
Disallow: /?q=node/add/
Disallow: /?q=search/
Disallow: /?q=user/password/
Disallow: /?q=user/register/
Disallow: /?q=user/login/
Disallow: /?q=user/logout/

further, when we go to the rss.xml in the front page, we see that a user named 
"webmin"
is present in the site. Take a note as this will be useful later on

later we also found some keywords named "drupal". Small google searches found that this version of drupal is especially vulnerable to something called drupalgeddon

we go to 
msfconsole 
and type
search drupalgeddon
we set the url to /jabc/ and run it

BOOM we got a shell

obviously, as usual, we upgrade the shell with
python3 -c 'import pty;pty.spawn("/bin/bash")'

we also search for several suid binaries and found nothing useful

so we explore the files used for the websites at jabcd0cs. 
since its a php site and a mysql stack, we expect to find a database config on it, and kaboom
on config.php, there's a mysql credential:
username: root 
password: toor

we login to mysql
mysql -u root -p 
type in toor

and we're in
let me summarize what i did in the mysql:

i select the database jabcd0cs, and the user table.
And then I dump all the contents of that table:
SELECT * FROM odm_user;

we got a password hash for the user called webmin, we try to reverse find it, and we found that
username: webmin
password: webmin1980

we ssh with this credentials and got a second shell
obviously, we try and go for linpeas.sh 
we got some CVE-2021-4034 polkit privilege escalation exploit

we use this exploit https://github.com/berdav/CVE-2021-4034.git
and KABOOM, we got root
PWNED