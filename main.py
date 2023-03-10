from flask.views import MethodView
from wtforms import Form, StringField, SubmitField
from flask import Flask, render_template, requests
from calorie import Calorie
from temperature import Temperature

app = Flask(__name__)

class HomePage(MethodView):
    def get(self):
        return render_template('index.html')

class CaloriesFormPage(MethodView):

    def get(self):
        calories_form = CaloriesForm()

        return render_template('calories_form_page.html',
                               caloriesform=calories_form)

    def post(self):
        calories_form = CaloriesForm(request.form)

        temperature = Temperature(country=calories_form.country.data,
                                  city=calories_form.city.data).get()

        calorie = Calorie(weight=float(calories_form.weight.data),
                          height=float(calories_form.height.data),
                          age=float(calories_form.age.data),
                          temperature=temperature)
        calories = calorie.calculate()

        return render_template('calories_form_page.html',
                               caloriesform=calories_form,
                               calories=calories,
                                 result=True)

class CaloriesForm(Form):
    weight = StringField("Weight: ", default=80)
    height = StringField("height: ", default=185)
    age = StringField("Age: ", default=36)
    country = StringField("Country: ", default='Sweden')
    city = StringField("City: ", default="Stockholm")
    button = SubmitField("Calculate")


# Initialize pages
app.add_url_rule('/',
                 view_func=HomePage.as_view('home_page'))
app.add_url_rule('/calories_form',
                 view_func=CaloriesFormPage.as_view('calories_form_page'))

# Run the app
app.run(debug=True)