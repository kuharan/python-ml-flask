from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from score_iris import score

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


class ReusableForm(Form):
    sepallength = TextField('Sepal Length:', validators=[validators.required()])
    sepalwidth = TextField('Sepal Width:', validators=[validators.required()])
    petallength = TextField('Petal Length:', validators=[validators.required()])
    petalwidth = TextField('Petal Width:', validators=[validators.required()])


@app.route("/", methods=['GET', 'POST'])
def func():
    form = ReusableForm(request.form)

    print
    form.errors

    if request.method == 'POST':
        sepallength = request.form['sepallength']
        sepalwidth = request.form['sepalwidth']
        petallength = request.form['petallength']
        petalwidth = request.form['petalwidth']


        if form.validate():
            #Save the comment here.
            flash('All the fields are - ' + sepallength + "," + sepalwidth + "," + petallength + "," + petalwidth)
        else:
            flash('All the form fields are required. ')

        res = score(sepallength, sepalwidth, petallength, petalwidth)
        flash(res)

    return render_template('Hello.html', form=form)


if __name__ == "__main__":
    app.run()
