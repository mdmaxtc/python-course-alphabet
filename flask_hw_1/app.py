from flask import Flask, render_template, request, flash, url_for
from flask_restful import abort

from home import home
from vegetables import vegetables
from fruits import fruits

app = Flask(__name__)

app.register_blueprint(home)
app.register_blueprint(vegetables)
app.register_blueprint(fruits)


@app.route('/interesting')
def page_not_implemented():
    abort(404)
    return render_template('')


@app.errorhandler(404)
def error_404_handler(error):
    return "Page doesn`t exist"


if __name__ == '__main__':
    app.run(debug=True)