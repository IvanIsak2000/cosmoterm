from flask import Flask, render_template
from flask import send_file

app = Flask(__name__)


@app.route('/')
def get_home_page():
    return render_template('home.html')


@app.route('/download')
def download_file():
    path = 'cosmoterm'
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
