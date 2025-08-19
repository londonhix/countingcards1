from flask import Flask, render_template, request, redirect, url_for, session
from count_systems import hi_lo, ko
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
suits = ['hearts', 'spades', 'clubs', 'diamonds']

systems = {
    'Hi-Lo': hi_lo,
    'KO': ko
}


@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        selected_system
    except NameError:
        selected_system = 'none'
    if request.method == 'POST':
        selected_system = request.form.get('system', 'none')
        session['system'] = selected_system
        session['count'] = 0
        session['history'] = []
        #return redirect(url_for('round'))
    return render_template('index.html', systems=systems.keys(), system = selected_system)

@app.route('/round', methods=['GET', 'POST'])
def round():
    suit = random.choice(suits)
    rank = random.choice(ranks)
    card_key = f"{suit}_{rank}"
    session['card'] = card_key

    # Get the count value using selected system
    system_module = systems.get(session['system'])  # Default to Hi-Lo if none
    count_value = system_module.card_value(rank)
    session['count'] += count_value

    # Save history
    session['history'].append({
        'card': card_key,
        'value': count_value,
        'total': session['count']
    })
    print(session['system'])
    advice = system_module.betting_advice(session['count'])

    return render_template(
        'round.html',
        card=card_key,
        system=session['system'],
        count=session['count'],
        advice=advice
    )

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))

@app.route('/train', methods=['GET', 'POST'])
def train():
    if request.method == 'POST':
        interval = float(request.form.get('interval', 2))
        session['train_cards'] = []
        session['train_count'] = 0
        session['interval'] = interval
        system=session['system']
        return redirect(url_for('training_session'))
    return render_template('train.html')

@app.route('/training_session')
def training_session():
    suit = random.choice(suits)
    rank = random.choice(ranks)
    card_key = f"{suit}_{rank}"
    print(session['system'])
    system_module = systems.get(session['system'])
    count_value = system_module.card_value(rank)
    session['train_count'] += count_value

    return render_template('training_session.html', card=card_key, interval=session['interval'], system=session['system'],)

@app.route('/training_end', methods=['POST'])
def training_end():
    guess = int(request.form['guess'])
    actual = session.get('train_count', 0)
    result = {
        'guess': guess,
        'actual': actual,
        'correct': guess == actual
    }
    return render_template('training_result.html', result=result)

@app.route('/training_guess')
def training_guess():
    return render_template('training_guess.html')

@app.route('/learn')
def learn():
    return render_template('learn.html')

if __name__ == '__main__':
    app.run(debug=True)
