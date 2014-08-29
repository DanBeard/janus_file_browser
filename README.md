janus_file_browser
==================

A simple file browser for janusVR

![Imgur](http://i.imgur.com/NPbr2Sl.png)
![Imgur2](http://i.imgur.com/79ZHxHJ.jpg)

requirements:
Python 2.7

How to use:
Launch like:

    python server.py

Then in JanusVR create a portal to 127.0.0.1:9191

That's it!

DISCLAIMER:
This script hosts a web server bound to localhost:9191 that will give a directory listing 
and serve files from your root directory. It should, by default,  not serve to other IPs.
However hosting anything like this is inherently dangerous. Do not use
this unless you know what you are doing and you are doing it securely.
