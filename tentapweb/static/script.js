// Populate the date dropdown with options
window.addEventListener('DOMContentLoaded', () => {
  // Call the function to add the event listener after the elements have been loaded
  document.getElementById('saveButton').addEventListener('click', saveUpdatedValue);
  updateData();
});

// Fetch and return the bookings
function fetchBookings() {
  return fetch('http://skolmen.ddns.net:56234/get_bookings')
    .then(response => response.json())
    .then(bookings => {
      return bookings;
    })
    .catch(error => {
      console.error('Error fetching bookings:', error);
      return [];
    });
}

// Save the updated value to the server
function saveUpdatedValue() {
  const date = document.getElementById('dateDropdown').value;
  const type = document.getElementById('typeDropdown').value;
  const value = document.getElementById('valueInput').value;

  // Send the updated value to the server
  fetch('http://skolmen.ddns.net:56234/update_booking', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ date, type, value })
  })
    .then(response => response.json())
    .then(result => {
      if (result.success) {
        // Fetch and update the table
        document.getElementById('valueInput').value = '';
        updateData();
      } else {
        switch (result.error_type) {
          case 1: //Fel bokningstyp
            alert('Felaktigt bokningstyp. Endast EM eller FM!');
            break;
          case 2: //Felaktigt salsnamn
            alert('Felaktigt salsnamn. Ange ett giltigt salsnamn!');
            break
          default:
            alert('Misslyckades att ändra sal. Försök igen senare.');
            break;
        }

      }
    })
    .catch(error => {
      console.error('Error updating value:', error);
      alert('Ett fel uppstod vid salsändring. Försök igen senare.');
    });
}

// Updates the data
function updateData() {
  fetchBookings()
    .then(bookings => {
      // Update the table with the fetched bookings
      updateTable3(bookings);
      // Update who books
      updateWhoBooks(bookings);
      // Update todays and tommorows rooms 
      updateRooms(bookings);
      // Populate the dropdown
      updateDateDropdown(bookings);
    })
    .catch(error => {
      console.error('Error retrieving bookings:', error);
    });
}

// Populates the date dropdown menu
function updateDateDropdown(bookings) {
  bookings.forEach(booking => {
    const option = document.createElement('option');
    option.value = booking.date;
    option.textContent = booking.date;
    dateDropdown.appendChild(option);
  });
}

function updateBookingNames() {
  const bookingDateSpan = document.getElementById('bookingDate');
  const bookingNamesDiv = document.getElementById('bookingNames');

  // Get the date two days forward
  const today = new Date();
  const twoDaysForward = new Date(today);
  twoDaysForward.setDate(today.getDate() + 2);

  // Format the date
  const formattedDate = formatDate(twoDaysForward);

  // Set the date in the heading
  bookingDateSpan.textContent = formattedDate;

  // Fetch bookings for the two days forward
  fetch('/bookings')
    .then(response => response.json())
    .then(bookings => {
      // Filter bookings for the two days forward
      const filteredBookings = bookings.filter(booking => booking.date === formattedDate);

      // Check if there are any bookings for the date
      if (filteredBookings.length > 0) {
        // Create a string of booking names
        const bookingNames = filteredBookings.map(booking => booking.person_1 + ' FM och ' + booking.person_2 + ' EM').join(', ');

        // Set the booking names in the div
        bookingNamesDiv.textContent = bookingNames;
      } else {
        // No bookings for the date, display '-'
        bookingNamesDiv.textContent = '-';
      }
    })
    .catch(error => {
      console.error('Error fetching bookings:', error);
      bookingNamesDiv.textContent = 'Error fetching bookings';
    });
}

//Updates the rooms
function updateRooms(bookings) {
  const currentDate = new Date().toLocaleDateString('sv-SE');

  const today_salFmValue = document.getElementById('today-salFmValue');
  const today_salEmValue = document.getElementById('today-salEmValue');
  const tomorrow_salFmValue = document.getElementById('tomorrow-salFmValue');
  const tomorrow_salEmValue = document.getElementById('tomorrow-salEmValue');

  
  // Get the date for tommorow
  const today = new Date();
  const tomorrowsDate = new Date(today);
  tomorrowsDate.setDate(today.getDate() + 1);

  // Find the booking for the current date
  const tomorrowsBooking = bookings.find(booking => booking.date === formatDate(tomorrowsDate));

  // Find the booking for the current date
  const todaysBooking = bookings.find(booking => booking.date === currentDate);

  // Update the values in the sal boxes
  if (todaysBooking) {
    today_salFmValue.textContent = todaysBooking.sal_fm;
    today_salEmValue.textContent = todaysBooking.sal_em;
  } else {
    today_salFmValue.textContent = '-';
    today_salEmValue.textContent = '-';
  }

  // Update the values in the sal boxes
  if (tomorrowsBooking) {
    tomorrow_salFmValue.textContent = tomorrowsBooking.sal_fm;
    tomorrow_salEmValue.textContent = tomorrowsBooking.sal_em;
  } else {
    tomorrow_salFmValue.textContent = '-';
    tomorrow_salEmValue.textContent = '-';
  }

}

// Update who books
function updateWhoBooks(bookings) {
  const bookingDateSpan = document.getElementById('bookingDate');
  const bookingNamesDiv = document.getElementById('bookingNames');

  // Get the date two days forward
  const today = new Date();
  const twoDaysForward = new Date(today);
  twoDaysForward.setDate(today.getDate() + 2);

  // Format the date
  const formattedDate = formatDate(twoDaysForward);

  // Set the date in the heading
  bookingDateSpan.textContent = formattedDate;

  const filteredBookings = bookings.filter(booking => booking.date === formattedDate);

  if (filteredBookings.length > 0) {
    // Create a string of booking names
    const bookingNames = filteredBookings.map(booking => booking.person_1 + ' FM och ' + booking.person_2 + ' EM').join(', ');

    // Set the booking names in the div
    bookingNamesDiv.textContent = bookingNames;
  } else {
    // No bookings for the date, display '-'
    bookingNamesDiv.textContent = '-';
  }

} 

// Updates the table 
function updateTable3(bookings) {
  // Populate table with bookings
  const table = document.getElementById('id-main-mid-list-table');

  // Clear existing table rows
  while (table.rows.length > 1) {
    table.deleteRow(1);
  }

  // Populate table with bookings
  bookings.forEach(booking => {
    const row = table.insertRow();

    // Format the date
    const date = new Date(booking.date);
    const formattedDate = booking.date;
    const day = date.toLocaleString('sv-se', { weekday: 'short' });
    const currentDate = new Date();
    currentDate.setHours(0, 0, 0, 0); // Set current date to midnight for comparison

    if (date < currentDate) {
      row.classList.add('main-mid-list-table-tr-completed');
    }
    
    const dateCell = row.insertCell();
    dateCell.textContent = formattedDate;

    const dayCell = row.insertCell();
    dayCell.textContent = day;

    const person1Cell = row.insertCell();
    person1Cell.textContent = booking.person_1;

    const person2Cell = row.insertCell();
    person2Cell.textContent = booking.person_2;

    const salFmCell = row.insertCell();
    salFmCell.textContent = booking.sal_fm;

    const salEmCell = row.insertCell();
    salEmCell.textContent = booking.sal_em;
  });
}

// Returns js date as iso 8601 yyyy-mm-dd
function formatDate(date) {
  return date.toISOString().split('T')[0];
}
