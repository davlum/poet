# Setup

The server is currently running Debian, Nginx, Python and PostgreSQL. [This tutorial](
https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-) is a very similar to how the server is configured now.

Because of limited resouces, swap memory is used on the server. Swap memory was added with the help of [this tutorial](https://www.digitalocean.com/community/tutorials/how-to-configure-virtual-memory-swap-file-on-a-vps).

If you find yourself needing to update PostgreSQL, I recommend [this tutorial](https://www.pontikis.net/blog/update-postgres-major-version-in-debian).

# Translation

In order to generate the .po file:
```
python manage.py makemessages -l es -e j2,py -i bin -i lib
```
In order to compile the files:
```
python manage.py compilemessages
```