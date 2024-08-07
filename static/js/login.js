const csrftoken = getCookie('csrftoken');
var baseUrl = window.location.protocol + "//" + window.location.host;
$(document).ready(function() {
    $('#loginForm').submit(function(event) {
      event.preventDefault(); // Prevent default form submission
  
      // Collect form data
      var formData = {
        username: $('#username').val(),
        password: $('#password').val()
      };
  
      // Send AJAX request
      $.ajax({
        type: 'POST',
        url: `${baseUrl}/api/login/`,
        contentType: 'application/json',
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin', // Do not send CSRF token to another domain.
        data: JSON.stringify(formData),
        success: function(response) {
          console.log('Login successful:', response['access']);
          localStorage.setItem('LoginToken', response['access']);
          // Handle success, e.g., redirect to dashboard
          window.location.href = `/api/home?user=${response['payload']['username']}`;
        },
        error: function (xhr, status, error) {
            // Handle errors (e.g., show an error message)
            console.log("Error: " + error);
            console.log("Status: " + status);
            console.log("Response: " + xhr.responseText);
        }
      });
    });
  });

 // Get CSRF Token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
} 