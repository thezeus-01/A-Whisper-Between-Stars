from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'a_very_secret_and_random_key_here_for_security_shhh'

@app.route('/')
def login():
    session.pop('authenticated', None)
    return render_template('login.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    password = request.form.get('password')
    if password == '28/05/2004':
        session['authenticated'] = True
        return render_template('login.html', authenticated=True)
    else:
        return render_template('login.html', error="Invalid password. Are you sure you're Shruthi?")

@app.route('/proceed/<choice>')
def proceed(choice):
    if session.get('authenticated') and choice == 'yes':
        return redirect(url_for('questions'))
    else:
        session.pop('authenticated', None)
        return render_template(
            'final_page.html',
            message="It's okay. Maybe another time. If you change your mind, try logging in again! 😉",
            show_start_over=True
        )

@app.route('/questions', methods=['GET', 'POST'])
def questions():
    if not session.get('authenticated'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        answers = [
            request.form.get('q1'),
            request.form.get('q2'),
            request.form.get('q3')
        ]
        yes_count = answers.count('yes')
        no_count = answers.count('no')

        if yes_count >= 2:
            return render_template('proposal_message.html')
        elif no_count >= 2:
            session.pop('authenticated', None)
            return render_template(
                'final_page.html',
                message="It's okay. Maybe another time. If you change your mind, try logging in again! 😉",
                show_start_over=True
            )
        else:
            return render_template(
                'result.html',
                message="Hmm… not enough 'Yes' or 'No' answers. No worries, let's try again from the start?",
                show_start_over=True
            )

    return render_template('questions.html')

@app.route('/waiting_question', methods=['GET', 'POST'])
def waiting_question():
    if not session.get('authenticated'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        wait_answer = request.form.get('wait_for_me')
        if wait_answer == 'yes':
            return redirect(url_for('contact_page'))
        else:
            session.pop('authenticated', None)
            return render_template(
                'final_page.html',
                message="It's okay, I understand. But I'll still be hoping. ❤️",
                show_start_over=True
            )
    return render_template('waiting_question.html')

@app.route('/contact_page')
def contact_page():
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    return render_template('contact_page.html')

@app.route('/final_page')
def final_page():
    return render_template(
        'final_page.html',
        message="Thank you for your time. Goodbye!",
        show_start_over=True
    )

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000)) 
    app.run(host="0.0.0.0", port=port)

