// Wait for the DOM content to be loaded before executing the script
document.addEventListener('DOMContentLoaded', () => {

  // Get references to HTML elements
  const cityNameInput = document.getElementById('city');
  const submitButton = document.getElementById('submit-btn');
  const weatherDataDiv = document.getElementById('weather-data');

  // Add a click event listener to the submit button
  submitButton.addEventListener('click', () => {

    // Retrieve the value of the city name input field
    const cityName = cityNameInput.value.trim();

    // Check if the city name is empty
    if (cityName.length === 0) {
      // Display an error message in the weather data div and exit the function
      weatherDataDiv.innerHTML = `<p>Please enter a city name</p>`;
      return;
    }

    // Make a request to the server for weather data
    fetch(`http://localhost:8000/weather?city=${encodeURIComponent(cityName)}`)
      .then(response => {
        // Check if the response was successful
        if (!response.ok) {
          // Throw an error if the response was not successful
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        // Parse the response as JSON
        return response.json();
      })
      .then(data => {
        // Check if the data contains an error message
        if (data.error) {
          // Display the error message in the weather data div
          weatherDataDiv.innerHTML = `<p>Error: ${data.error}</p>`;
        } else {
          // Extract the relevant data from the response
          const { temp, humidity, sunrise, sunset, timezoneOffset } = data;

          // Create a table to display the weather data
          const table = `
            <table>
              <tr>
                <th>Property</th>
                <th>Value</th>
              </tr>
              <tr>
                <td>Temperature</td>
                <td>${temp}&deg;C</td>
              </tr>
              <tr>
                <td>Humidity</td>
                <td>${humidity}%</td>
              </tr>
              <tr>
                <td>Sunrise</td>
                <td>${sunrise}</td>
              </tr>
              <tr>
                <td>Sunset time</td>
                <td>${sunset}</td>
              </tr>
            </table>
          `;

          // Display the table in the weather data div
          weatherDataDiv.innerHTML = table;
        }
      })
      .catch(error => {
        // Log the error to the console and display it in the weather data div
        console.error(error);
        weatherDataDiv.innerHTML = `<p>Error: ${error.message}</p>`;
      });
  });
});
 