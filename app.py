from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

def evaluate_password_strength(password):
    score = 0

    # Check minimum length
    if len(password) >= 8:
        score += 20

    # Check for uppercase letters
    if re.search(r'[A-Z]', password):
        score += 20

    # Check for lowercase letters
    if re.search(r'[a-z]', password):
        score += 20

    # Check for numbers
    if re.search(r'[0-9]', password):
        score += 20

    # Check for special characters
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 20

    return score

def suggest_stronger_password(password):
    # Generate a stronger password by adding uppercase and lowercase letters
    # and special characters to the original password
    stronger_password = password.capitalize() + '@' + password.lower() + '123'
    return stronger_password

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_password', methods=['POST'])
def check_password():
    user_input = request.form['password']
    score = evaluate_password_strength(user_input)

    feedback = f"Password Strength: {'Weak' if score < 50 else 'Medium' if score < 75 else 'Strong'}<br>Score: {score}/100"

    if score < 50:
        feedback += "<br><br>Feedback:<br>- Your password is weak and can be easily guessed.<br>- Consider adding a mix of uppercase and lowercase letters, numbers, and special characters for better security."
        suggested_password = suggest_stronger_password(user_input)
        feedback += f"<br><br>Suggested Stronger Password: {suggested_password}"

    elif score < 75:
        feedback += "<br><br>Feedback:<br>- Your password is decent, but it could be stronger.<br>- Consider adding a mix of uppercase and lowercase letters for added complexity."
        suggested_password = suggest_stronger_password(user_input)
        feedback += f"<br><br>Suggested Stronger Password: {suggested_password}"

    return jsonify({'feedback': feedback})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
