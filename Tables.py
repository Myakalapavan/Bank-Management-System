#for createing the tables

import mysql.connector as db
conn = db.connect(user = 'root', password = 'Haran@62',
                  host = 'localhost', database = 'project')

print(conn)

cur = conn.cursor()

'''
cur.execute('DROP TABLE IF EXISTS transactions;')
cur.execute('DROP TABLE IF EXISTS accounts;')
cur.execute('DROP TABLE IF EXISTS users;')
'''

#create users table
cur.execute('''
CREATE TABLE users (
    userid INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(60) NOT NULL
);                  
''')

#create accounts table
cur.execute('''
CREATE TABLE accounts (
    accountid INT AUTO_INCREMENT PRIMARY KEY,
    userid INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    accountnumber VARCHAR(20) UNIQUE NOT NULL,
    aadharnumber VARCHAR(20),
    phonenumber VARCHAR(15),
    address VARCHAR(100),
    email VARCHAR(40),
    accounttype VARCHAR(20),
    balance DECIMAL(15,2) DEFAULT 0.00,
    pin VARCHAR(10) NOT NULL,
    createdate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (userid) REFERENCES users(userid)
);
''')

#create transactions table

cur.execute('''
CREATE TABLE transactions (
    transactionid INT AUTO_INCREMENT PRIMARY KEY,
    accountid INT NOT NULL,
    transactiontype ENUM('debit', 'credit') NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    transactiondate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (accountid) REFERENCES accounts(accountid)
);
''')
conn.commit()
cur.close()
conn.close()
print('user side tables created successfully')

