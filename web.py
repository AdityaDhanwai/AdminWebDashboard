from flask import Flask,render_template,request,jsonify,session,send_file
import mysql.connector,json
import subprocess
import random,string,re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import subprocess
login=False
print(login)

app=Flask(__name__,static_folder='static')
app.secret_key = 'Amazon'  # set a secret key for session management
cnx = mysql.connector.connect(
    user='root',
    password='root@2003',
    host='localhost',
    database='Hotel'
)
# Create a cursor object to execute SQL queries
cursor = cnx.cursor()


def generate_password(length=8):
    """Generate a random password."""
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password
@app.get("/")
def index_get():
     global login
     login=False 
     return render_template("login.html")

@app.get("/error_login")
def get_error_login():
    return render_template("error.html")

# RequestMapping for SignUp
@app.get("/newuser")
def Create():
    # Generate a random password
    password = generate_password()
    return render_template("index.html",password=password)

@app.get("/home")
def homepage():
    if (login==True):
        name = session.get('username')
        return render_template("dashboard.html",name=name)
    else:
        return render_template("error.html")
    

@app.get("/Loader")
def Email_Loader():
    if (login==True):
        name = session.get('username')
        return render_template("Email_Loader.html",name=name)
    else:
        return render_template("error.html")
# @app.get("/room_data")
# def RoomData():
#     if (login==True):
#         name = session.get('username')
#         return render_template("Room_Data.html",name=name)
#     else:
#         return render_template("error.html")
# @app.get("/customer_data")
# def CustomerData():
#     if (login==True):
#         name = session.get('username')
#         return render_template("Customer_Data.html",name=name)
#     else:
#         return render_template("error.html")
@app.route('/login_valid',methods=['POST'])
def login_validation():
    username=request.form.get('username')
    password=request.form.get('password')
    # Define the SELECT query to check if the username and password match
    query = "SELECT * FROM Login WHERE username=%s AND password=%s"
    
        # Define the values to pass into the query
    values = (username, password)

        # Execute the query and fetch the result
    cursor.execute(query, values)
    result = cursor.fetchone()

    # Close the cursor and the database connection    
    # Check if the result is not None, which means the login is successful
    if result is not None:
        global login
        login=True
        username = result[0]
        email=result[2]
        contact=result[3]
        password=result[1]
        session['username']=username
        session['email']=email
        session['contact']=contact
        session['password']=password
        # replace_placeholder_with_session_variable('intents.json','{name}',name)
        # data_list = []
        # for row in cursor.fetchall():
        #     data_list.append(row)
         # Determine the appropriate greeting based on the current time
         # Get the current time
        current_time = datetime.now().time()
        greeting = ""
        if current_time.hour < 12:
            greeting = "Good morning"
        elif current_time.hour < 18:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"

        return f"""
            <script>
                var username = "{username}";
                var greeting = "{greeting}";
                alert('Login successful\\nWelcome, ' + username + '!\\n' + greeting);
                window.location.href = '/home';
            </script>
        """
    else:
        return """
            <script>
                alert('Login failed. Please try again.');
                window.location.href = '/error_login';
            </script>
        """
    

@app.get("/profile")
def get_profile():
    data = session.get('username')  # retrieve data from the session variable
    email = session.get('email')
    contact = session.get('contact')
    password = session.get('password')
    print(data + email + contact + password)

    # Determine the appropriate greeting based on the current time
    # Note: You need to import the 'datetime' module at the top of your code
    from datetime import datetime, time
    current_time = datetime.now().time()
    if current_time < time(12, 0):
        greeting = "Good morning"
    elif current_time < time(17, 0):
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    return f"""
            <script>
                var email = "{email}";
                var data = "{data}";
                var contact = "{contact}";
                var password = "{password}";
                var greeting = "{greeting}";
                alert('Profile Info>>>\\nEmail: ' + email + '\\nUsername: ' + data + '\\nContact: ' + contact + '\\nPassword: ' + password + '\\n' + greeting);
                window.location.href = '/home';
            </script>
        """

# OTP Verification code 
@app.get("/forgot")
def forgot():
    return render_template("forgot_password.html")



@app.route("/send_email", methods=["GET", "POST"])
def send_email():
    if request.method == "POST":
        recipients = request.form.get("emails")
        message = request.form.get("message")
        # Debugging statement
        print("Recipients:", recipients)
        print("Message:", message)
        try:
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            smtp_username = "adityadhanwai8@gmail.com"  # Your email address
            smtp_password = "gzgoxvodajxtltlo"  # Your email password
            from_email = "adityadhanwai8@gmail.com"  # Your email address

            # Create an SMTP connection
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)

            # Create the email message
            msg = MIMEMultipart()
            msg["Subject"] = "Test Email"  # Set your email subject here
            msg["From"] = from_email
            msg["To"] = recipients

            # Attach the message to the email
            msg.attach(MIMEText(message, "plain"))

            # Send the email
            server.sendmail(from_email, recipients.split(","), msg.as_string())

            # Close the SMTP connection
            server.quit()

            return """
                <script>
                    alert('Email sent successfully.');
                    window.location.href = '/home';
                </script>
            """
        except Exception as e:
            print("Failed to send email. Error:", e)
            return """
                <script>
                    alert('Failed to send email. Please try again later.');
                    window.location.href = '/home';
                </script>
            """

    return render_template("index.html")


# End
if __name__=="__main__":
    app.run(debug=True)