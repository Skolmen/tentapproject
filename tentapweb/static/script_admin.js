window.addEventListener('DOMContentLoaded', () => {
    document.getElementById('removeBookingButton').addEventListener('click', removeBooking);
    document.getElementById('bookingForm').addEventListener('submit', function(event) {
      event.preventDefault(); // Prevent the default form submission
      // Gather the form data
      const formData = new FormData(this);
      const data = {
        date: formData.get('date'),
        person_fm: formData.get('person_fm'),
        person_em: formData.get('person_em'),
        sal_fm: formData.get('sal_fm'),
        sal_em: formData.get('sal_em')
      };
      addBooking(data).then(() => {
        updateData();
      });
    });
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

// Updates the data
function updateData() {
  fetchBookings()
    .then(bookings => {
      // Update the table with the fetched bookings
      updateTable(bookings);
      // Populate the dropdown
      updateDateDropdown(bookings);
    })
    .catch(error => {
      console.error('Error retrieving bookings:', error);
    });
}

// Updates the table 
function updateTable(bookings) {
  // Populate table with bookings
  const table = document.getElementById('booking-table');

  // Clear existing table rows
  while (table.rows.length > 1) {
    table.deleteRow(1);
  }

  // Populate table with bookings
  bookings.forEach(booking => {
    const row = table.insertRow();
    
    const idCell = row.insertCell();
    idCell.textContent = booking.id;

    const dateCell = row.insertCell();
    dateCell.textContent = booking.date;

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

// Populates the date dropdown menu
function updateDateDropdown(bookings) {
  // Clear the existing options
  removeBookingDropdown.innerHTML = '';

  bookings.forEach(booking => {
    const option = document.createElement('option');
    option.value = booking.id; // Assuming there's an "id" field in the database
    option.textContent = booking.date; // Display the date as the option text
    removeBookingDropdown.appendChild(option);
  });
}

// Remove the selected booking
function removeBooking() {
  const bookingId = document.getElementById('removeBookingDropdown').value;

  // Send the request to remove the booking
  fetch('http://skolmen.ddns.net:56234/remove_booking', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ id: bookingId })
  })
    .then(response => response.json())
    .then(result => {
      if (result.success) {
        // Refresh the table and remove booking dropdown
        updateData();
      } else {
        alert('Misslyckades ta bort bokning. Försök igen senare.');
      }
    })
    .catch(error => {
      console.error('Error removing booking:', error);
      alert('Ett fel skede vid borttagande. Försök igen senare.');
    });
}

function addBooking(data) {  
  // Send the data as JSON using fetch
  return fetch('http://skolmen.ddns.net:56234/add_booking', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
    .then(response => response.json())
    .then(result => {
      if (result.success) {
        // Handle success case
        console.log('Booking added successfully');
      } else {
        // Handle error case
        console.error('Failed to add booking:', result.error);
      }
    })
    .catch(error => {
      console.error('Error adding booking:', error);
    });
}
