from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import InputRequired, DataRequired, URL
from flask_ckeditor import CKEditor


current_year = datetime.now().year

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6d2onzWlSihBXox7C0sKR6b'
Bootstrap(app=app)
ckeditor = CKEditor(app=app)


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(model_class=Base)
db.init_app(app=app)


class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    img_url: Mapped[str] = mapped_column(String, nullable=False)
    location: Mapped[str] = mapped_column(String, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default='false')
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default='false')
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default='false')
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default='false')
    seats: Mapped[str] = mapped_column(String, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String, nullable=False)


class CreateNewCafe(FlaskForm):
    name = StringField('Cafe Name', validators=[InputRequired()])
    map_url = StringField('Cafe Map URL', validators=[InputRequired(), URL()])
    img_url = StringField('Cafe Image URL', validators=[InputRequired(), URL()])
    location = StringField('Cafe Location', validators=[InputRequired()])
    has_sockets = BooleanField('Has Sockets', validators=[DataRequired()])
    has_toilet = BooleanField('Has Toilet', validators=[DataRequired()])
    has_wifi = BooleanField('Has Wi-Fi', validators=[DataRequired()])
    can_take_calls = BooleanField('Can Take Calls', validators=[DataRequired()])
    seats = StringField('Seats in Cafe', validators=[InputRequired()])
    coffee_price = StringField('Coffee Price', validators=[InputRequired()])
    submit = SubmitField('Add New Cafe')


# with app.app_context():
#     db.create_all()


@app.route('/')
def home_page():
    cafes = Cafe.query.all()
    return render_template('index.html', all_cafes=cafes, year=current_year)


@app.route('/cafe/<int:cafe_id>')
def show_cafe(cafe_id):
    cafe_to_show = Cafe.query.filter_by(id=cafe_id).first()
    return render_template('cafe_details.html', cafe=cafe_to_show, year=current_year)


@app.route('/search')
def search():
    key = request.args.get('key')
    if key:
        searched_cafe = Cafe.query.filter(Cafe.location.contains(key) | Cafe.name.contains(key))
    else:
        searched_cafe = Cafe.query.all()
    return render_template('index.html', all_cafes=searched_cafe, year=current_year)


@app.route('/add-cafe', methods=['GET', 'POST'])
def add_cafe():
    add_cafe_form = CreateNewCafe()

    if add_cafe_form.validate_on_submit():
        new_cafe = Cafe(
            name=add_cafe_form.name.data,
            map_url=add_cafe_form.map_url.data,
            img_url=add_cafe_form.img_url.data,
            location=add_cafe_form.location.data,
            has_sockets=add_cafe_form.has_sockets.data,
            has_toilet=add_cafe_form.has_toilet.data,
            has_wifi=add_cafe_form.has_wifi.data,
            can_take_calls=add_cafe_form.can_take_calls.data,
            seats=add_cafe_form.seats.data,
            coffee_price=add_cafe_form.coffee_price.data,
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('home_page'))
    return render_template('add_cafe.html', form=add_cafe_form, year=current_year)


@app.route('/delete/<int:cafe_id>')
def delete_cafe(cafe_id):
    selected_cafe = Cafe.query.filter_by(id=cafe_id).first()
    db.session.delete(selected_cafe)
    db.session.commit()
    return redirect(url_for('home_page'))


if __name__ == '__main__':
    app.run(debug=True)
