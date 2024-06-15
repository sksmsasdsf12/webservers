from flask import Flask, render_template, request, redirect
from util import database, regex

app = Flask(__name__)

def getip():
    return request.headers.get("CF-Connecting-IP", request.remote_addr)

@app.route('/', methods = ['POST', 'GET'])
def main():
    if request.method == 'POST':
        key = request.form['key']
        link = request.form['redirect']
        if key == '' or link == '': # 공백인 칸이 존재하는 경우 
            return render_template("create.html")
        if not regex.check_url(link): # 올바르지 않은 url 인 경우
            return render_template("error.html", error = '올바르지 않은 URL 입니다.')
        if len(key) > 6: # key 길이가 6보다 큰 경우
            return render_template("error.html", error = 'URL 이 6자 이상입니다.')
        result = database.gen_url(getip(), key, link)
        if result[0] == 'FAIL':
            return result[1]
        return render_template('success.html', url=f'http://#DOMAIN/{key}')
    else:
        return render_template("create.html")

@app.route('/<key>')
def user(key):
    result = database.get_url(key)
    if result[0] == 'FAIL': # 올바르지 않은 키값인 경우
        return render_template('error.html', error = result[1])
    return redirect(result[1])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)