<p>
  
# Password manager in textual

My project is a simple password manager that uses MySQL database and has UI created in Python framework textual

### It uses:
* Python 3.12
* textual 3.1.1
* mysql.connector 2.2.9

You can install it by using this commands:

```
pip install textual==3.1.1
pip install mysql.connector==2.2.9
```

## Guide
### 1. Log in
<img src="https://i.postimg.cc/h48QWjgY/login.png">

First you need to log in. At the moment there is no option to set your own PIN diffrent way than changing it in the code.

### 2. Add password

<img src="https://i.postimg.cc/kgydq0Dq/add.png">

You can add password on this screen. You need to insert password and password's purpose and confirm it by clicking add button.

### 3. Manage passwords

<img src="https://i.postimg.cc/90TQpLb0/manage.png">

To manage passwords go to the manage passwords screen, here you have list of your passwords. From there, you can view your password and update your password by clicking the blue button or delete password by clicking red button. 

<img src="https://i.postimg.cc/02BVmZ3D/ask.png">

Both require confirming by inserting a PIN.

<img src="https://i.postimg.cc/85ZRGzgM/select.png">

The update button transports you to update password screen.

<img src="https://i.postimg.cc/gJ7x4XPS/update.png">

Here, you need to insert a new password and repeat it, after clicking update button password will be updated.

### !Important!

The MySQL server has to be enabled when running the program.
</p>

