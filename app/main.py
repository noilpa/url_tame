from hashlib import md5
from json import dumps
from re import escape

from flask import Flask, request, Response, redirect, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL

app = Flask(__name__)
prefix = 'v1'
storage = {}
host = 'localhost:5000'

@app.route('/')
@app.route('/index')
def hello_world():
    form = InputForm()
    return render_template('index.html', form=form)


@app.route(f'/{prefix}/url/<path:sub_path>', methods=['GET'])
def handle_short_url(sub_path):
    url = storage.get(sub_path)
    if url is None:
        Response(response=dumps({'status': 404, 'error': 'url not found'}), status=200, content_type='application/json',
                 headers={})
    return redirect(url)


@app.route(f'/{prefix}/url', methods=['POST'])
def create_short_url():
    url = request.form.get('url')
    if url is None:
        return render_template('index.html', result='empty url')
    short_url = request.form.get('custom')
    if short_url == '':
        m = md5()
        m.update(url.encode())
        short_url = m.hexdigest()
        # check short_url existence in storage
    storage[short_url] = url
    result = escape('/'.join([host, prefix, 'url', short_url]))
    return render_template('index.html', result=result)


class InputForm(FlaskForm):
    url = StringField('target url', validators=[DataRequired(), URL()], description='url description')
    custom = StringField('custom name', description='custom name description')
    submit = SubmitField('Tame!')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
