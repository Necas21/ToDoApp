from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SubmitField, TimeField
from wtforms.validators import DataRequired, Length
from wtforms.fields import DateTimeLocalField


class TaskForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=64)])
    description = TextAreaField(
        "Description", validators=[DataRequired(), Length(max=140)]
    )
    due_date = DateTimeLocalField("Due Date (UTC)", format="%Y-%m-%dT%H:%M")
    submit = SubmitField("Create")
