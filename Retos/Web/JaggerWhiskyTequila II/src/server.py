import os, sys, jwt
from flask import Flask, render_template, send_from_directory, request, make_response

app = Flask(__name__, static_folder='static')

with open(os.path.join(sys.path[0], 'static/id_rsa'), 'rb') as secret, open(os.path.join(sys.path[0], 'static/id_rsa.pub'), 'rb') as pub:
    public  = pub.read()
    private = secret.read()
token = jwt.encode({'edad': 17}, private, algorithm='RS256') 

def check(cookie) -> bool:
    alg = jwt.get_unverified_header(cookie)
    data = jwt.decode(cookie, public, algorithms='RS256')
    return 'edad' in data.keys() and data['edad'] >= 18

@app.route('/id_rsa', methods=['GET'])
@app.route('/robots.txt', methods=['GET'])
def robots():
    return send_from_directory(app.static_folder, request.path[1:]), 200

@app.route('/comprar', methods=['GET'])
def buy():
    ok = False
    try:
        cookie = request.cookies.get('cliente')
        ok = check(cookie)
    except:
        pass
    return render_template('buy.html', ok=ok), 200

@app.route('/', methods=['GET'])
def index():
    r = make_response(render_template('index.html'))
    if request.cookies.get('session'):
        r.delete_cookie('session')
    if request.cookies.get('cliente') == None:
        r.set_cookie('cliente', token)
    return r, 200

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000)