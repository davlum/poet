# poet

[![Build Status](https://travis-ci.com/davlum/poet.svg?branch=master)](https://travis-ci.com/davlum/poet)[![Coverage Status](https://coveralls.io/repos/github/davlum/poet/badge.svg?branch=master)](https://coveralls.io/github/davlum/poet?branch=master)


# Translation

In order to generate the .po file:
```
python manage.py makemessages -l <LANG_CODE> -e j2,py -i bin -i lib
```
In order to compile the files:
```
python manage.py compilemessages
```
