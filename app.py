import subprocess
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/setup')
def setup():
    return render_template('Setup_Page.html')

@app.route('/run_1')
def run_1():
    return render_template('run_C.html')

@app.route('/run', methods=['POST'])
def run():
    code = request.form['code']
    user_input = request.form['user_input']  # Retrieve user input from the form

    with open('temp.c', 'w') as f:
        f.write(code)

    # Run the code using subprocess
    result = subprocess.run(['gcc', 'temp.c', '-o', 'temp'], 
                            input=user_input.encode(),  # Pass user input to the subprocess
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode == 0:
        # Run the compiled code
        output = subprocess.run(['./temp'], 
                                input=user_input.encode(),  # Pass user input to the subprocess
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return render_template('run_C.html', code=code, user_input=user_input, result=output.stdout.decode(), error=output.stderr.decode())
    else:
        return render_template('run_C.html', code=code, user_input=user_input, error=result.stderr.decode())

if __name__ == '__main__':
    app.run()
