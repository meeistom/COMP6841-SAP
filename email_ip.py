from flask import Flask, request, redirect

app = Flask(__name__)

@app.route('/')
def get_ip():
    visitor_ip = request.remote_addr
    print(f'IP: {visitor_ip}')
    return redirect(request.args.get('url', 'https://google.com'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)