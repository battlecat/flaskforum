# Based on David-Guo's flask-forum,please see https://github.com/David-Guo/flaskforum.git

This is a full function forum/bbs system include insert picture or attachment of any type file.It can be very simple and easy to be installed

# How to install and run it?

## Get the code

    git clone https://github.com/battlecat/flaskforum.git
    
## 
Create db

    mysql -u root -p < create_db.sql
    
Create tables
    
    $ python manager.py shell
    >>> db.create_all()
    
