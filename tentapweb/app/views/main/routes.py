from flask import render_template
from datetime import datetime, timedelta
import requests
import locale

from app.views.main import bp

from app.utils.helper_functions import fetchStartPageContent
from app.utils.helper_functions import getApiDetails

locale.setlocale(locale.LC_TIME, 'sv_SE.UTF-8')

def getBookings():
    todayBooking = ""
    tommorrowBooking = ""
    overMorrowBooking = ""
    data = []
    
    today = datetime.today().strftime('%Y-%m-%d')
    
    endpoint = f"bookings?with_names=true&start_date={today}"
    API_LINK, API_KEY = getApiDetails(endpoint)    
    
    response = requests.get(API_LINK, headers={
        'X-API-Key': API_KEY
    })

    if response.status_code == 200:
        data = response.json()
        today = datetime.today().strftime('%Y-%m-%d')
        tommorrow = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
        overMorrow = (datetime.today() + timedelta(days=2)).strftime('%Y-%m-%d')
        
        for booking in data:
            if booking["date"] == today:
                todayBooking = booking
            elif booking["date"] == tommorrow:
                tommorrowBooking = booking
            elif booking["date"] == overMorrow:
                overMorrowBooking = booking
                
        #add the column day based on the date to data
        for booking in data:
            booking["day"] = datetime.strptime(booking["date"], '%Y-%m-%d').strftime('%a')
            

    return data, todayBooking, tommorrowBooking, overMorrowBooking

# Route to serve the webpage
@bp.route('/')
def index():
    information = fetchStartPageContent("INFORMATION")
    priorities = fetchStartPageContent("PRIORITIES")
    heading = fetchStartPageContent("HEADING")

    bookings, todaysBooking, tommorrowsBooking, overMorrowsBooking = getBookings()

    return render_template('index.html', information=information, priorities=priorities,\
                                        heading=heading, tomorrowsBooking=tommorrowsBooking,\
                                        todaysBooking=todaysBooking, overMorrowsBooking=overMorrowsBooking, bookings=bookings)