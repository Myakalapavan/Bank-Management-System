#user side procedures

import mysql.connector as db

def newuser_register():
    conn = db.connect(user = 'root', password = 'Haran@62',
                      host = 'localhost', database = 'project')

    username = input('Enter username: ')
    password = input('Password: ')

    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM users WHERE username=%s;', [username])
    cnt = cur.fetchone()[0]
    #print(cnt)

    if cnt>0:
        print('username already exists')
    else:
        cur.execute('INSERT INTO users(username,password) VALUES(%s,%s);', [username,password])
        userid = cur.lastrowid
        name = input('Enter full name: ')
        accountnumber = input('Enter your Account number: ')
        aadharnumber = input('Enter your Aadhar number: ')
        phonenumber = input('Enter your Phone number: ')
        address = input('Enter your address: ')
        email = input('Enter your Email: ')
        accounttype = input('Enter your Account Type(Saving/Checking): ')
        balance = float(input('Enter Initial Balance: '))
        pin = input('Set a 4-Digit pin: ')

        cur.execute('INSERT INTO accounts(userid,name,accountnumber,aadharnumber,phonenumber,address,email,accounttype,balance,pin)\
                     VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);',
                     [userid,name,accountnumber,aadharnumber,phonenumber,address,email,accounttype,balance,pin])
        conn.commit()
        print()
        print('New user registered successfully')
        print()
        
        cur.close()
        conn.close()



def login_to_get_account_number():
    conn = db.connect(user = 'root', password = 'Haran@62',
                      host = 'localhost', database = 'project')
    print()
    username = input('Enter username: ')
    password = input('Password: ')
    
    cur = conn.cursor()
    cur.execute('SELECT userid FROM users WHERE username=%s and password=%s', [username,password])
    data = cur.fetchone()
    
    if data:
        user_id = data[0]
        cur.execute('SELECT accountnumber FROM accounts WHERE userid=%s;', [user_id])
        a_number = cur.fetchone()
        if a_number:
            print()
            print('___________________________________________')
            print()
            print('         Successfully Login')
            print(f'         Account Number : {a_number[0]}')
            print()
            print('___________________________________________')
            print()
        else:
            print('No account number corresponding to the Userid')
    else:
        print('Invalid Username or Password')
        print('Login failed')
    cur.close()
    conn.close()
            
          

def login_with_account_number_and_pin():
    conn = db.connect(user = 'root', password = 'Haran@62',
                      host = 'localhost', database = 'project')
    
    a_number = input('Enter an account Number: ')
    pin = input('Enter your 4-digit pin: ')
    
    cur = conn.cursor()
    cur.execute('SELECT accountid FROM accounts WHERE accountnumber=%s and pin=%s;', [a_number, pin])
    a_id = cur.fetchone()
    cur.close()
    conn.close()
    if a_id:
        print()
        print('____________________________________________')
        print()
        print(f'       Your Accountid is : {a_id[0]}')
        print('       Login Successfully Completed')
        print()
        print('____________________________________________')
        print()
        return True
    else:
        print('Invalid account number or pin')
        print('Login Failed')
        return False      


def view_Account():
    conn = db.connect(user = 'root', password = 'Haran@62',
                      host = 'localhost', database = 'project')
    print()
    a_id = int(input('Enter your accountid: '))
    cur = conn.cursor()
    cur.execute('SELECT name, accountnumber, accounttype, balance FROM accounts WHERE accountid=%s;', [a_id])
    details = cur.fetchone()

    if details:
        print()
        print('____________Account Details______________')
        print()
        print(f'         Name : {details[0]}')
        print(f'         Account Number : {details[1]}')
        print(f'         Account Type : {details[2]}')
        print(f'         Balance : {details[3]}')
        print()
        print('_________________________________________')
        print()
    else:
        print('Account Not Found')
    cur.close()
    conn.close()


def transactions():
    
    conn = db.connect(user = 'root', password = 'Haran@62',
                      host = 'localhost', database = 'project')
    print()
    account_id = int(input('Enter your Accountid: '))
    transaction_type = input('Enter your transaction Type(credit/debit): ')
    
    cur = conn.cursor()
    cur.execute('SELECT balance FROM accounts WHERE accountid=%s;', [account_id])
    b = cur.fetchone()[0]
    b = float(b)
                     
    if transaction_type == 'credit':
        print()
        a = float(input('Enter an Amount to Add: '))
        b_a = b+a
               
    elif transaction_type == 'debit':
        print()
        a = float(input('Enter an Amount to subtract: '))
        if a<=b:
            b_a = b-a
        else:
            print('Insufficient Balance')
            return
    else:
        print('Invalid Transaction Type')
        return
            
    cur.execute('UPDATE accounts SET balance=%s WHERE accountid=%s;', [b_a, account_id])
    cur.execute('INSERT INTO transactions(accountid, transactiontype,amount) VALUES(%s, %s, %s);', [account_id, transaction_type, a])
    conn.commit()
    
    cur.close()
    conn.close()
    print()
    print('Transaction successfully Completed')
    print()
        
                   
def pin_change():
    conn = db.connect(user = 'root', password = 'Haran@62',
                      host = 'localhost', database = 'project')

    account_id = int(input('Enter your Accountid: '))
    old_pin = input('Enter your old pin: ')
    
    cur = conn.cursor()
    cur.execute('SELECT pin FROM accounts WHERE accountid=%s;', [account_id])
    p = cur.fetchone()

    if p is None:
        print()
        print('Account ID not found.')
        cur.close()
        conn.close()
        return
    
    elif p[0] == old_pin:
        print()
        new_pin = input('Enter 4-digit New Pin: ')
        confirm_pin = input('Enter 4-digit New Confirm Pin: ')
        print()
        if new_pin == confirm_pin:
            cur.execute('UPDATE accounts SET pin=%s WHERE accountid=%s;', [confirm_pin,account_id])
            conn.commit()
            print('PIN changed successfully!')
            print()
        else:
            print('Incorrect confirm_pin')
    else:
        print('Incorrect old pin')
    cur.close()
    conn.close()


def view_transactions_of_a_particular_days_between():
    conn = db.connect(user = 'root', password = 'Haran@62',
                      host = 'localhost', database = 'project')
    print()
    account_id = input('Enter your AccountId: ')
    datestart = input('Enter starting Date to get details(YYYY-MM-DD): ')
    dateend = input('Enter ending Date to get details(YYYY-MM-DD): ')
    cur = conn.cursor()
    cur.execute('SELECT * FROM transactions where accountid=%s and DATE(transactiondate) BETWEEN %s and %s;',[account_id,datestart,dateend])
    data = cur.fetchall()
    if data:
        print()
        print('________________Days between Transaction Details_________________')
        print()
        for i in data:
            print(f'       TransactionID : {i[0]}')
            print(f'       Accountid : {i[1]}')
            print(f'       TransactionType : {i[2]}')
            print(f'       Amount : {i[3]}')
            print(f'       Transaction Date : {i[4]}')
            print()
        print('________________________________________________________')
        print()
    else:
        print('No transaction Details to this accountId')
    cur.close()
    conn.close()

#_________________________________________________
    
#Admin side procedures
    
def admin_login():
    adminid = '62'
    password = 'pavan@62'

    while True:
        print()
        AdminId = input('Enter your Admin id: ')
        Password = input('Enter your Password: ')
        if AdminId == adminid and Password == password:
            print('Successfully Login')
            print()
            return 
        else:
            print('Login Failed')
            print('Enter correct adminid and password')


def view_all_users():
    conn = db.connect(user = 'root', password = 'Haran@62',host = 'localhost', database = 'project')
    cur = conn.cursor()
    cur.execute('SELECT * from users')
    data = cur.fetchall()
   

    if data:
        print()
        print('______________________User Details_________________________')
        print()
        print(f'Total users retrieved {len(data)}')
        print()
        for i in data:
            print(f'       User Id is : {i[0]},     User Name is : {i[1]}')
        print()
        print('___________________________________________________________')
        print()
    else:
        print('Users Not Found')
    cur.close()
    conn.close()

              
def view_account_datails_of_a_particular_user():
    conn = db.connect(user = 'root', password = 'Haran@62',
                      host = 'localhost', database = 'project')
    print()
    account_n = input('Enter an Account Number: ')
    cur = conn.cursor()
    cur.execute('select * from accounts where accountnumber=%s;', [account_n])
    data = cur.fetchall()
    if data:
        print()
        print('________________Account Details______________________')
        for details in data:
            print()
            print()
            print(f'       accountid          : {details[0]}')
            print(f'       userid             : {details[1]}')
            print(f'       name               : {details[2]}')
            print(f'       accountnumber      : {details[3]}')
            print(f'       aadharnumber       : {details[4]}')
            print(f'       phonenumber        : {details[5]}')
            print(f'       address            : {details[6]}')
            print(f'       email              : {details[7]}')
            print(f'       accounttype        : {details[8]}')
            print(f'       balance            : {details[9]}')
            print(f'       pin                : {details[10]}')
            print(f'       createdate         : {details[11]}')
            print()
            print('_____________________________________________________')
            
    else:
        print('Account Details Not Found')
    cur.close()
    conn.close()



def view_transaction_details_of_a_particular_user():
    conn = db.connect(user = 'root', password = 'Haran@62',
                      host = 'localhost', database = 'project')
    print()
    account_id = input('Enter an AccountId: ')
    cur = conn.cursor()
    cur.execute('SELECT * FROM transactions where accountid=%s;',[account_id])
    data = cur.fetchall()
    if data:
        print()
        print('__________________Transaction Details___________________')
        print()
        print(f'Total transactions retrieved {len(data)}')
        print()
        for i in data:
            print(f'       TransactionID           : {i[0]}')
            print(f'       Accountid               : {i[1]}')
            print(f'       TransactionType         : {i[2]}')
            print(f'       Amount                  : {i[3]}')
            print(f'       Transaction Date        : {i[4]}')
            print()
        print('________________________________________________________')
        print()
    else:
        print('No transaction details found for the given AccountId.')
    cur.close()
    conn.close()


def view_transaction_of_a_particular_day():
    conn = db.connect(user = 'root', password = 'Haran@62',
                      host = 'localhost', database = 'project')
    print()
    account_id = input('Enter your AccountId: ')
    date = input('Enter a Date to get details(YYYY-MM-DD): ')
    cur = conn.cursor()
    cur.execute('SELECT * FROM transactions where accountid=%s and DATE(transactiondate)=%s;',[account_id,date])
    data = cur.fetchall()
    if data:
        print()
        print('________________Day Transaction Details_________________')
        print()
        for i in data:
            print(f'       TransactionID : {i[0]}')
            print(f'       Accountid : {i[1]}')
            print(f'       TransactionType : {i[2]}')
            print(f'       Amount : {i[3]}')
            print(f'       Transaction Date : {i[4]}')
            print()
        print('________________________________________________________')
        print()
    else:
        print('No transaction Details to this accountId')
    cur.close()
    conn.close()
    
#_________________________________________________

if __name__ == '__main__':
    print()
    print('1.USER')
    print('2.ADMIN')
    print()
    
    ch = input('Choose One Option: ')
    if ch == '1':
        while True:
            print()
            print('***********************************************')
            print()
            print('         1.New User Register')
            print('         2.Login to get Account Number')
            print('         3.Login with account Number and Pin')
            print('         4.Pin Change')
            print('         5.view_transactions_of_a_particular_days_between')
            print('         6.Exit')
            print()
            print('***********************************************')
            print()
            ch = input('Choose one Option: ')
            print()
            if ch == '1':
                newuser_register()
            elif ch == '2':
                login_to_get_account_number()
            elif ch == '3':
                if login_with_account_number_and_pin():
                    while True:
                        print()
                        print('************************************')
                        print()
                        print('     1.View Account Details')
                        print('     2.Make Transactions')
                        print('     3.Main Menu')
                        print()
                        print('************************************')
                        print()

                        sub_ch = input('Choose One Option: ')
                        if sub_ch == '1':
                            view_Account()
                        elif sub_ch == '2':
                            transactions()
                        elif sub_ch == '3':
                            break
                        else:
                            print('Choose Correct Option')
            elif ch == '4':
                pin_change()
            elif ch == '5':
                view_transactions_of_a_particular_days_between()
            elif ch == '6':
                print('Exit User Menu')
                print('ThankYou! Visit Again!')
                break
            else:
                print('Choose Correct Option')
    elif ch == '2':
        admin_login()
        while True:
            print()
            print('1.view_all_users')
            print('2.view_account_datails_of_a_particular_user')
            print('3.view_transaction_details_of_a_particular_user')
            print('4.view_transaction_of_a_particular_day')
            print('5.Exit')
            print()
            ch = input('CHoose One Option: ')
            
            if ch == '1':
                view_all_users()
                
            elif ch == '2':
                view_account_datails_of_a_particular_user()
                
            elif ch == '3':
                view_transaction_details_of_a_particular_user()
                
            elif ch == '4':
                view_transaction_of_a_particular_day()
                
            elif ch == '5':
                print('Exit Admin Menu')
                print('ThankYou! Visit Again!')
                break
            else:
                print('Choose Correct Option')
                break
    else:
        print('Choose Correct Option')

            
                    
                           

     


            





















