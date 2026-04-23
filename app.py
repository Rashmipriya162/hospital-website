from flask import Flask, render_template, request

app = Flask(__name__)

# Home Page
@app.route('/')
def home():
    return render_template('index.html')


# Appointment Booking
@app.route('/book', methods=['POST'])
def book():
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    contactnumber = request.form['contactnumber']
    address = request.form['address']
    problem = request.form['problem']

    # Save data into file
    with open("data.txt", "a") as file:
        file.write(f"{name}, {age}, {gender}, {contactnumber}, {address}, {problem}\n")

    return f"""
    <h2>Appointment Booked Successfully!</h2>
    <p><b>Name:</b> {name}</p>
    <p><b>Age:</b> {age}</p>
    <p><b>Gender:</b> {gender}</p>
    <p><b>Contact:</b> {contactnumber}</p>
    <p><b>Address:</b> {address}</p>
    <p><b>Problem:</b> {problem}</p>
    <br>
    <a href="/">Go Back</a>
    """


# Admin Panel (View All Patients)
@app.route('/admin')
def admin():
    patients = []

    try:
        with open("data.txt", "r") as file:
            for line in file:
                data = line.strip().split(", ")
                patients.append(data)
    except FileNotFoundError:
        pass

    return render_template('admin.html', patients=patients)


if __name__ == '__main__':
    app.run(debug=True)