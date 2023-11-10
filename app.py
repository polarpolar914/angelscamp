from flask import Flask, request, render_template_string
from opnet import find_oil_station
from key import sk_api_key
app = Flask(__name__)

@app.route('/')
def index():
    html_form = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>주유소 검색</title>
    </head>
    <body>
        <form action="/submit" method="post">
            <label for="출발지">출발지:</label>
            <input type="text" id="출발지" name="출발지"><br><br>
            <label for="도착지">도착지:</label>
            <input type="text" id="도착지" name="도착지"><br><br>
            <input type="submit" value="Submit">
        </form>
    </body>
    </html>
    """
    return render_template_string(html_form)

@app.route('/submit', methods=['POST'])
def submit():
    string1 = request.form['출발지']
    string2 = request.form['도착지']


    result = find_oil_station(string1, string2)


    return result, 200, {'Content-Type': 'application/json; charset=utf-8'}

if __name__ == '__main__':
    app.run(debug=True, charset='utf-8')
