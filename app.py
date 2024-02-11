from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
db = SQLAlchemy(app)

# Определение модели Feedback
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(255))
    full_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100))
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

    def __init__(self, comment, full_name, address, email, phone):
        self.comment = comment
        self.full_name = full_name
        self.address = address
        self.email = email
        self.phone = phone


@app.route('/')
@app.route('/feedback', methods=['GET'])
def feedback_form():
    return render_template('feedback_form.html')


@app.route('/feedback', methods=['POST'])
def add_feedback():
    comment = request.form.get('comment')
    name = request.form.get('full_name')
    address = request.form.get('address')
    email = request.form.get('email')
    phone = request.form.get('phone')

    error = get_validate_error(name, email)
    if error:
        return render_template('feedback_form.html', message=error)

    else:
        save_in_db(Feedback(comment, name, address, email, phone))

        return render_template('feedback_form.html', message='Successed')


def get_validate_error(name, email):
    if not name or not email:
        error = 'Пожалуйста, заполните все обязательные поля!'
    elif '@gmail.com' in email:
        error = 'Регистрация пользователей с почтовым адресом @gmail.com невозможна'
        return error

def save_in_db(feedback):
    db.session.add(feedback)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
