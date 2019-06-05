from flask import Blueprint, render_template, request, url_for, Flask
from werkzeug.utils import redirect

vegetables = Blueprint('vegetables', __name__, template_folder='templates')

VEGETABLES = [
     'Carrot',
     'Onion',
     'Paprika',
     'Cucumber',
     'Garlik',

]

@vegetables.route('/vegetables')
def vegetables_page():
    return render_template('vegetables.html', title='Vegetables', vegetables=VEGETABLES)


@vegetables.route('/vegetables/add/', methods=('POST', 'GET'))
def add_vegetable():
    name = request.form['vegetable']
    VEGETABLES.append(name)
    return redirect(url_for('vegetables.vegetables_page'))


@vegetables.route('/vegetables/del/', methods=('POST', 'GET'))
def del_vegetable():
    name = request.form['vegetable']
    VEGETABLES.remove(name)
    return redirect(url_for('vegetables.vegetables_page'))