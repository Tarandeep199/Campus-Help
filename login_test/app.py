# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session, flash
import csv
import datetime
from functools import wraps
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

# create the application object
app = Flask(__name__)

account_sid = 'AC1f968d1925c1e431bf48d6b7ed41aadb'
auth_token = 'f3caf3bf91f8d435bfe0eca1b25fdab8'
app.secret_key = 'secret_key_here'

client = Client(account_sid, auth_token)


issues = []
times = []
usernames = []
phonenumbers = []
message = ''


def check_credentials(username, password):
    with open('users.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields= csvreader.next()
        for row in csvreader:
            print(row)
            if(row[0]==username and row[1]==password):
                return True
        return False


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap



# use decorators to link the function to a url
@app.route('/')
@login_required
def home():
    #return "Hello, World!"  # return a string
    return render_template('tickets_all.html')

#TICKET SYSTEM
@app.route('/ticket_create', methods=['GET','POST'])
def ticketCreate():
    error=None
    if request.method == 'POST':
        issue = request.form.get("ticket_content")
        time = datetime.datetime.now()
        print(issue, time, session['username'])
        issues.append(issue)
        times.append(time)
        usernames.append(session['username'])
        return redirect('all_tickets')
    return render_template('ticket.html', error=error)

@app.route('/all_tickets', methods=['GET','POST'])
def showTickets():
    numBoxes = len(issues)
    message = ''
    if 'button0' in request.form:
        message = client.messages \
                .create(
                     body='your request for ' + issues[0] + ' has been accepted by ' + session['username'],
                     from_='+12063123749',
                     to='+1' + phonenumbers[0]
                 )
        #issues.remove[issues[0]]
    #print(message.sid)

    if 'button1' in request.form:
        message = client.messages \
                .create(
                    body='your request for ' + issues[1] + ' has been accepted by ' + session['username'],
                    from_='+12063123749',
                    to='+1' + phonenumbers[1]
                 )
        #issues.remove[1]


   # print(message.sid)

    if 'button2' in request.form:
        message = client.messages \
                .create(
                    body="Someone has accepted your request",
                    from_='+12063123749',
                    to='+12096036030'
                )
      #  issues.remove[2]

  #  print(message.sid)

    if 'button3' in request.form:
        message = client.messages \
                .create(
                    body="Someone has accepted your request",
                    from_='+12063123749',
                    to='+12096036030'
                 )
     #   issues.remove[3]


   # print(message.sid)
#
    if 'button4' in request.form:
        message = client.messages \
                .create(
                    body="Someone has accepted your request",
                    from_='+12063123749',
                    to='+12096036030'
                )
  #  print(message.sid)
      #  issues.remove[4]

    if 'button4' in request.form:
        message = client.messages \
                .create(
                    body="Someone has accepted your request",
                    from_='+12063123749',
                    to='+12096036030'
                 )
     #   issues.remove[5]


  #  print(message.sid)

    if 'button5' in request.form:
        message = client.messages \
                .create(
                    body="Someone has accepted your request",
                    from_='+12063123749',
                    to='+12096036030'
                 )

   # print(message.sid)

    if 'button6' in request.form:
        message = client.messages \
                .create(
                    body="Someone has accepted your request",
                    from_='+12063123749',
                    to='+12096036030'
                 )
     #   issues.remove[6]

  #  print(message.sid)

    return render_template('tickets_all.html', issues=issues, times=times, usernames=usernames, numBoxes=numBoxes)


#USER REGISTER FUNCTION
@app.route('/register', methods=['GET', 'POST'])
def registration():
    error = None
    if request.method == 'POST':
        user1 = request.form.get("username")
        pass1= request.form.get("password")
        phone = request.form.get("phone")
        phonenumbers.append(phone)
        print(phonenumbers)
        print(user1 + " registered successfully")
        with open('users.csv', mode='a') as user_file:
            user_writer = csv.writer(user_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            user_writer.writerow([user1,pass1,phone])
        flash(user1 + " registered succesfully")
        return redirect(url_for('login'))
    return render_template('registration.html', error=error)


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template


# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if check_credentials(request.form['username'],request.form['password']) == False:
            error = 'Invalid Credentials. Please try again.'
        else:
            username=request.form['username']
            session['username'] = username
            session['logged_in'] = True
            flash('Logged in successfully')
            return redirect(url_for('showTickets'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('logged out successfully')
    return redirect(url_for('welcome'))


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)