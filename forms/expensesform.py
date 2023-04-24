from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DateField
from wtforms.validators import DataRequired


class ExpenseForm(FlaskForm):
    title = StringField('Категория расходов', validators=[DataRequired()])
    money = IntegerField("Сумма")
    created_date = DateField("Дата", format="%Y-%m-%d")
    submit = SubmitField('Добавить')
