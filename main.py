from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from datetime import datetime
import os

app = Flask(__name__)
# configuration of db
app.config["SECRET_KEY"] = "my_application123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db = SQLAlchemy(app)
# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'christasaraluke19@gmail.com'
app.config['MAIL_PASSWORD'] = os.getenv("PASSWORD")
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        start_date = request.form['start_date']
        date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        occupation = request.form['occupation']

        form = Form(first_name=first_name, last_name=last_name,
                    email=email, date=date_obj, occupation=occupation)
        db.session.add(form)
        db .session.commit()

        message_body = f"Thank you for your submission, {first_name}." \
                       f"Here are your data:\n{first_name}\n{last_name}\n{date_obj}\n" \
                       f"Thank You!"
        msg = Message(
            'Form Submission',
            sender=app.config['MAIL_USERNAME'],
            recipients=[email],
            body=message_body,
        )
        mail.send(msg)

        flash("Your form was submitted successfully!")

    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=500)
