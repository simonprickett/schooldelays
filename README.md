schooldelays
============

Determine if the school system is delayed (usually for snow).  Working on this for Fairfax County schools in Virginia.

Work in progress.  Need to see some delay examples!

Setup Environment

Raspberry Pi B+ with Raspian from the Raspberry Pi Foundation.

Some sort of internet connection.

sudo apt-get install libxslt-dev
sudo apt-get install libxml2-dev
sudo pip install lxml
sudo pip install requests
sudo pip install schedule
... unicorn hat setup

Why have to sudo python to get Unicorn Hat working? -- looks like this is a 
known thing:

"The method UnicornHat uses to actually drive the pixels involves some low-level memory twiddling that only the root user has access to. It's a bit of a hassle, but there's currently no way around it."

Here's an example of the Unicorn Hat working on my Raspberry Pi B+, this 
will be driven by this script in the near future...

https://www.youtube.com/watch?v=caxBljIjARE
