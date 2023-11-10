from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    html_form = """
    <form action="/submit" method="post">
        <label for="string1">String 1:</label>
        <input type="text" id="string1" name="string1"><br><br>
        <label for="string2">String 2:</label>
        <input type="text" id="string2" name="string2"><br><br>
        <input type="submit" value="Submit">
    </form>
    """
    return render_template_string(html_form)

@app.route('/submit', methods=['POST'])
def submit():
    string1 = request.form['출발지']
    string2 = request.form['도착지']

    return f'Received string1: {string1} and string2: {string2}'

if __name__ == '__main__':
    app.run(debug=True)
