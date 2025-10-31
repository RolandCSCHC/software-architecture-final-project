from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

@app.route('/')
def index():
    return render_template('index.html', title='Home')

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        # Here you would typically save to database or send email
        return render_template('contact.html', title='Contact', success=True)
    return render_template('contact.html', title='Contact')

@app.route('/api/data')
def api_data():
    # Example API endpoint
    data = {
        'message': 'Hello from Flask API!',
        'status': 'success',
        'data': [1, 2, 3, 4, 5]
    }
    return jsonify(data)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', title='Page Not Found'), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
