# Flask-forum, a full function forum/bbs system.

Based on David-Guo's flask-forum,please see https://github.com/David-Guo/flaskforum.git

This is  a full function forum/bbs system include insert picture or attachment of any type file.It can be very simple and easy to be installed

# How to install and run it under Ubuntu 14.04?

## 1.installed mysql first under ubuntu

    sudo -s
    apt-get install mysql-server mysql-client libmysqlclient-dev
    
## 2.change the mysql root password to be 123456 and normally start mysql

    # /etc/init.d/mysql stop 
    # mysqld_safe --user=mysql --skip-grant-tables --skip-networking & 
    # mysql -u root mysql 
    mysql> UPDATE user SET Password=PASSWORD(’123456’) where USER=’root’; 
    mysql> FLUSH PRIVILEGES; 
    mysql> quit 
    # /etc/init.d/mysql restart 
    # mysql -uroot -p 
    Enter password: <input your newpassword:123456> 
    mysql> 
    mysql>exit
    # /etc/init.d/mysql restart 
    
## 3.Get the code

    git clone https://github.com/battlecat/flaskforum.git

## 4.Create db

    cd flask-forum
    mysql -u root -p < create_db.sql
    
## 5.Repeat the above step 2 and change the mysql root password to 123456
     but be carefully don't repeat the step 4

## 6.Create tables
    
    $ python manager.py shell
    >>> db.create_all()
    
    Please repeat the step 2 and to change the mysql root password to 123456 if spawned any erro about access dennied problem.
    
## 7.Run server

    #python manager.py runserver
    
## 8.Please find the page of http://127.0.0.1:5000

good luck!
    


    

