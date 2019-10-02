import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donor, Donation

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)

@app.route('/create/', methods=['GET', 'POST'])
def new_donations():

	if request.method == 'POST':

		name = request.form['name']
		new_donation = int(request.form['new_donation'])

		try:
			donor= Donor.select().where(Donor.name == name).get()
		except Donor.DoesNotExist as e: 
			donor = Donor(name=name)
			donor.save()
		
		donation_made = Donation(donor=donor, value=new_donation)
		donation_made.save()

		return redirect(url_for('all'))
	return render_template('new_donations.jinja2')


# Route for handling the login page logic
@app.route('/login/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('new_donations'))
    return render_template('login.jinja2', error=error)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

