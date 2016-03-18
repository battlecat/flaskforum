# SYSU flea market


Get the code

    git clone https://github.com/David-Guo/flaskforum.git
    
Create db

    mysql -u root -p < create_db.sql
    
Create tables
    
    $ python manager.py shell
    >>> db.create_all()
    