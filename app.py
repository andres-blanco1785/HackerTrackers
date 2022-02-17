from flask import Flask, json, jsonify, request, Response

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route("/fibonacci/<int:number>")
def calc_fibonacci(number):
    fibonacci = [0]
    c1 = 0
    c2 = 1
    fib = 0
    check = 0

    if number < 0:
        return jsonify(input=number, output=False)
    elif number == 0:
        fibonacci = [0]
    else:
        while check == 0:
            fib = c1 + c2
            c2 = c1
            c1 = fib
            if fib <= number:
                fibonacci.append(fib)
            else:
                check = 1
    return jsonify(input=number, output=fibonacci)


if __name__ == '__main__':
    app.run()
