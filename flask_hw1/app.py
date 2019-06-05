import json
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)


def read_from_file(file):
    with open(file, 'r') as f:
        return json.load(f)


def save_to_file(file, data):
    with open(file, 'w') as f:
        json.dump(data, f)


def add_product(value, file):
    data = read_from_file(file)
    data.append(value)
    save_to_file(file, data)


def delete_product(value, file):
    data = read_from_file(file)
    for i, elem in enumerate(data):
        if elem == value:
            data.pop(i)
    save_to_file(file, data)


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/fruits')
@app.route('/fruits/<string:value>', methods=['GET', 'POST', 'DELETE'])
def fruits(value=None):
    if request.method == 'POST':
        do_post_fruits(value)
        return do_get_fruits()
    if request.method == 'DELETE':
        do_delete_fruits(value)
        return do_get_fruits()
    else:
        return do_get_fruits()


def do_get_fruits():
    return render_template('fruits.html', values=read_from_file('fruits.json'))


def do_post_fruits(value):
    add_product(value, 'fruits.json')


def do_delete_fruits(value):
    delete_product(value, 'fruits.json')


@app.route('/vegetables')
@app.route('/vegetables/<string:value>', methods=['GET', 'POST', 'DELETE'])
def vegetables(value=None):
    if request.method == 'POST':
        do_post_vegetables(value)
        return do_get_vegetables()
    if request.method == 'DELETE':
        do_delete_vegetables(value)
        return do_get_vegetables()
    else:
        return do_get_vegetables()


def do_get_vegetables():
    return render_template('vegetables.html', values=read_from_file('vegetables.json'))


def do_post_vegetables(value):
    add_product(value, 'vegetables.json')


def do_delete_vegetables(value):
    delete_product(value, 'vegetables.json')


@app.route('/return_to_main')
def redirect_to_main():
    return redirect(url_for("main"))


@app.errorhandler(404)
def error_404_handler(error):
    return render_template("error_404.html")


if __name__ == '__main__':
    app.run()