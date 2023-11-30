import json
from datetime import datetime
from flask import Flask, render_template, request, flash


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__, template_folder="templates")
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    matching_clubs = [club for club in clubs if club['email'] == request.form['email']]
    if matching_clubs:
        club = matching_clubs[0]
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        flash("Sorry, this email was not found.")
        return render_template('index.html')


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        competition_date_str = foundCompetition['date']
        current_date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if competition_date_str < current_date_str:
            flash("You can't book places for a past competition.")
            return render_template('welcome.html', club=foundClub, competitions=competitions,
                                   message="You can't book places for a past competition.")
        else:
            return render_template('booking.html', club=foundClub, competition=foundCompetition)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition_name = request.form['competition']
    club_name = request.form['club']
    places_required = int(request.form['places'])

    competition = next((c for c in competitions if c['name'] == competition_name), None)
    club = next((c for c in clubs if c['name'] == club_name), None)

    if competition and club:
        places_available = int(competition.get('numberOfPlaces', 0))

        # Vérification des points disponibles
        points_available = int(club.get('points', 0))

        if places_available >= places_required:
            if points_available >= places_required:
                # Déduction des points
                club['points'] = str(points_available - places_required)

                # Mise à jour du nombre de places disponibles pour la compétition
                competition['numberOfPlaces'] = str(places_available - places_required)
                flash('Great-booking complete!')
                return render_template('welcome.html', club=club, competitions=competitions)
            else:
                flash('Not enough points to make the booking.')
                return render_template('booking.html', club=club, competition=competition,
                                       message='Not enough points to make the booking.')
        else:
            flash('Not enough places available for booking.')
            return render_template('booking.html', club=club, competition=competition,
                                   message='Not enough places available for booking.')
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions,
                               message='Something went wrong-please try again')

@app.route('/pointsDisplay', methods=['GET'])
def points_display():
    clubs = loadClubs()
    return render_template('points_display.html', clubs=clubs)


@app.route('/logout')
def logout():
    return render_template('index.html')
