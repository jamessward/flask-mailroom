import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor

app = Flask(__name__)


@app.route('/')
def home():
    return redirect(url_for('all'))


@app.route('/add/', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('add.jinja2')

    else:  # POST
        donor_name = request.form['donor']
        # Retrieve the donor record from DB, if one exists
        try:
            donor = Donor.get(Donor.name == donor_name)
        except Exception as e:
            # No record in the donor table matches donor_name
            return render_template('add.jinja2', error='Donor {} not found'.format(donor_name))
        donation = Donation(value=request.form['amount'], donor=donor)
        donation.save()
        return redirect(url_for('all'))


@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)
    

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)
