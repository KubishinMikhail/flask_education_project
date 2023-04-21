from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DateField
from wtforms.validators import DataRequired


class ExpenseForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    money = IntegerField("стоимость")
    created_date = DateField("Дата", format="%Y-%m-%d")
    submit = SubmitField('добавить')
