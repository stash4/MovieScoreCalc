from flask import Flask, render_template
import pickle

app = Flask(__name__)


@app.route('/')
def list_page():
    with open('movies.pickle', 'rb') as f:
        movies = pickle.load(f)
    return render_template('list.html', title='test', movies=movies)


if __name__ == "__main__":
    app.run(debug=True)
