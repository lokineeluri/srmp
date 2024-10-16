from flask import Flask, request

app = Flask(__name__)

@app.route('/secure-data', methods=['GET'])
def secure_data():
    return "This is mTLS-protected data."

if __name__ == "__main__":
    context = ('../certificates/server-cert.pem', '../certificates/server-key.pem')
    app.run(ssl_context=context)
