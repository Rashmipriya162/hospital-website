from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)

# Secret key for admin login session
app.secret_key = "hospital_secret_key"


# ---------------------------------------------------
# HOME PAGE
# ---------------------------------------------------

@app.route('/')
def home():
    return render_template('index.html')


# ---------------------------------------------------
# BOOK APPOINTMENT
# ---------------------------------------------------

@app.route('/book', methods=['POST'])
def book():

    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    contactnumber = request.form['contactnumber']
    address = request.form['address']
    problem = request.form['problem']

    # Save data in text file
    with open("data.txt", "a") as file:

        file.write(
            f"{name}, {age}, {gender}, {contactnumber}, {address}, {problem}\n"
        )

    return f"""
    <h2>Appointment Booked Successfully ✅</h2>

    <p><b>Name:</b> {name}</p>
    <p><b>Age:</b> {age}</p>
    <p><b>Gender:</b> {gender}</p>
    <p><b>Contact Number:</b> {contactnumber}</p>
    <p><b>Address:</b> {address}</p>
    <p><b>Problem:</b> {problem}</p>

    <br>

    <a href="/">Go Back To Home</a>
    """


# ---------------------------------------------------
# SECRET ADMIN LOGIN PAGE
# ---------------------------------------------------

@app.route('/hospitaladminaccess', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        # CHANGE YOUR USERNAME & PASSWORD HERE
        if username == "rashmi" and password == "Rashmi@2026":

            session['admin_logged_in'] = True

            return redirect('/admin')

        else:

            return """
            <h3>Invalid Username or Password ❌</h3>

            <a href="/hospitaladminaccess">
                Try Again
            </a>
            """

    return render_template('login.html')


# ---------------------------------------------------
# PROTECTED ADMIN PAGE
# ---------------------------------------------------

@app.route('/admin')
def admin():

    # Protect admin page
    if not session.get('admin_logged_in'):

        return redirect('/hospitaladminaccess')

    patients = []

    try:

        with open("data.txt", "r") as file:

            for line in file:

                patient = line.strip().split(", ")

                patients.append(patient)

    except FileNotFoundError:

        pass

    return render_template('admin.html', patients=patients)


# ---------------------------------------------------
# LOGOUT
# ---------------------------------------------------

@app.route('/logout')
def logout():

    session.pop('admin_logged_in', None)

    return redirect('/')


# ---------------------------------------------------
# RUN FLASK APP
# ---------------------------------------------------

if __name__ == '__main__':

    app.run(debug=True)