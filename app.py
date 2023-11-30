from flask import Flask, request
from flask import render_template
import secret_santa

app = Flask(__name__)

@app.route("/", methods = ['GET', 'POST'])
def get_home_page():
    if request.method == 'POST':
        couples = [couple.strip().split(',') for couple in (request.form.get('names') or '').split('\n') if couple.strip()]
        assignments_per_person = int(request.form.get('assignments-per-person') or '1')
        use_brute_force = request.form.get('algorithm') == 'brute-force-algorithm'

        santa_assigner: secret_santa.SantaBase = secret_santa.BruteForceSanta(couples, assignments_per_person) if use_brute_force else secret_santa.BacktrackingSanta(couples, assignments_per_person)
        santa_assigner.generate_assignments()

        return render_template('page.html', assignments=santa_assigner.assignments)

    return render_template('page.html', assignments=None)