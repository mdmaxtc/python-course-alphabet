from flask import Blueprint, render_template, request, url_for, Flask
from werkzeug.utils import redirect

FRUITS = [
    'Papaya',
    'Passion Fruit',
    'Pomegranate',
    'Apricot',
    'Pineapple',

]

fruits = Blueprint('fruits', __name__, template_folder='templates')

@fruits.route('/fruits')
def fruits_page():
    return render_template('fruits.html', title='Fruits', fruits=FRUITS)


@fruits.route('/fruits/add/', methods=('POST', 'GET'))
def add_fruit():
    name = request.form['fruit']
    FRUITS.append(name)
    return redirect(url_for('fruits.fruits_page'))


@fruits.route('/fruits/del/', methods=('POST', 'GET'))
def del_fruit():
    name = request.form['fruit']
    FRUITS.remove(name)
    return redirect(url_for('fruits.fruits_page'))