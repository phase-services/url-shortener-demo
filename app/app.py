from pymongo import MongoClient
from os import getenv
from flask import Flask, request, render_template, redirect, url_for, abort
from string import digits, ascii_letters
from secrets import choice

max_redirect_len = 7
alphabet = digits + ascii_letters
redirect_admin_pwd = getenv('REDIRECT_ADMIN_PASSWORD')
mongo_client = MongoClient('db',
                            username=getenv('MONGO_INITDB_ROOT_USERNAME'),
                            password=getenv('MONGO_INITDB_ROOT_PASSWORD'))
db = mongo_client['phase-services']
redirects = db.redirects

app = Flask(__name__, template_folder='/app/templates/')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:path>', methods=['GET'])
def path_redirect(path):
    global redirects

    redirect_path = redirects.find_one({'path_from': path})

    if not redirect_path:
        return render_template('404.html')
    else:
        return render_template('redirect.html', redirect_path=redirect_path['path_to'])

@app.route('/register_path', methods=['POST'])
def register_path():
    global max_redirect_len
    global redirects
    global redirect_admin_pwd

    json_data = request.get_json()
    admin_pwd, path_from, path_to = None, None, None

    try:
        admin_pwd, path_to = json_data['admin_pwd'], json_data['path_to']
    except:
        abort(500, description='Invalid parameters provided')
    
    if admin_pwd == None or path_to == None:
        abort(500, description='Invalid parameters provided')

    if path_to[:7] != 'http://' and path_to[:8] != 'https://':
        abort(400, description='Invalid URL scheme provided')

    if admin_pwd != redirect_admin_pwd:
        abort(403, description='Invalid admin password provided')
    
    existing_redirect = redirects.find_one({'path_to':path_to})

    if existing_redirect:
        return f'URL for {path_to} already exists at {existing_redirect["path_from"]}'
    else:
        path_from = ''.join([choice(alphabet) for i in range(max_redirect_len)])
        
        while redirects.find_one({'path_from':path_from}):
            path_from = ''.join([choice(alphabet) for i in range(max_redirect_len)])

        redirects.insert_one({'path_from':path_from, 'path_to':path_to})

    return f'URL created for {path_to} at /{path_from}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)