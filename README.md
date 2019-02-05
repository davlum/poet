# poet

[![Build Status](https://travis-ci.com/davlum/poet.svg?branch=master)](https://travis-ci.com/davlum/poet)[![Coverage Status](https://coveralls.io/repos/github/davlum/poet/badge.svg?branch=master)](https://coveralls.io/github/davlum/poet?branch=master)

This is the code for the digital audio repository, [Poética Sonora](https://poeticasonora.me/). More about Poética Sonora can be found [here](https://poeticasonora.mx/).

# Translation

In order to generate the .po file:
```
python manage.py makemessages -l es -e j2,py -i bin -i lib
```
In order to compile the files:
```
python manage.py compilemessages
```

# Server setup

The server is currently running Debian, Nginx, Python and PostgreSQL.

It is running on 1GB of Ram, 25GB of harddrive and 2GB of Swap memory. Swap memory was added with the help of [this tutorial](https://www.digitalocean.com/community/tutorials/how-to-configure-virtual-memory-swap-file-on-a-vps).
Permissions for files and directories follow [these conventions](https://www.digitalocean.com/community/questions/proper-permissions-for-web-server-s-directory).
```
sudo find /path/to/dir -type d -exec chmod 755 {} \;

sudo find /path/to/dir -type f -exec chmod 644 {} \;
```

If you find yourself needing to update PostgreSQL, I recommend [this tutorial](https://www.pontikis.net/blog/update-postgres-major-version-in-debian).