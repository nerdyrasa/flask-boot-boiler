from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    #return 'hello world'
    #return render_template('index.html')
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
