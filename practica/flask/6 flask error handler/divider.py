from flask import Flask
from flask_wtf import FlaskForm
from wtforms.fields.numeric import IntegerField
from wtforms.validators import InputRequired

app = Flask(__name__)
class DivdeForm(FlaskForm):
    a = IntegerField(validators=[InputRequired()])
    b = IntegerField(validators=[InputRequired()])

@app.route('/divide/', methods=["POST"])
def divide():
    form = DivdeForm()
    if form.validate_on_submit():
        a, b = form.a.data, form.b.data
        return f"a/b={a / b:.2f}\n"
    return f"Bad request. Error={form.errors}", 400

@app.errorhandler(ZeroDivisionError)
def handle_exception(e: ZeroDivisionError):
    return "На ноль делить нельзя\n"

if __name__ == "__main__":
    app.config["WTF_CSRF_ENABLED"] = False
    app.run()
