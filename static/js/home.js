const csrftoken = getCookie('csrftoken');
const token = localStorage.getItem('LoginToken'); 
var socket = null; // Initialize WebSocket variable

$(document).ready(function() {
    console.log(`Token: ${token}`)
  
    // Function to join a chat room
    $('#joinChatBtn').click(function() {
      const roomId = $('#roomIdInput').val().trim();
      console.log(`roomid: ${roomId}`);
      
      if (roomId !== '') {
        // Redirect to the chat room using WebSocket
        socket = new WebSocket(`ws://localhost:5000/chat/${roomId}/?token=${token}`);
      }
  
      socket.onopen = function() {
        console.log('WebSocket connection opened');
      };
  
      socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        console.log(data);
        var user = data['User'];
        var content = data['content'];
        console.log("User " + user);
  
        if (content['history']) {
          displayHistory(content['history']);
        } else if (content['message']) {
          receiveMessage(user, content['message']);
        }
      };
    });
  
    // Function to send a chat message (assuming WebSocket handling)
    $('#sendMessageBtn').click(function() {
      const message = $('#messageInput').val().trim();
      if (message !== '') {
        const data = {
          message: message,
        };
        socket.send(JSON.stringify(data));
        console.log('Sending message:', message);
        // receiveMessage('You', message, true); // Display the sent message on the left
        $('#messageInput').val(''); // Clear message input after sending
      }
    });
  
    function displayHistory(history) {
      console.log("history")
      console.log(history)
      // $('#chatMessages').empty(); // Clear current messages
      history.forEach(item => {
        receiveMessage(item['sender_username'], item['text']);
      });
    }
  
    // Example: Function to receive and display chat messages via WebSocket
    function receiveMessage(user, message, isSender = false) {
      const messageClass = isSender ? 'my-message' : 'other-message';
      const messageHtml = `<div class="${messageClass}"><strong>${user}:</strong> ${message}</div>`;
      $('#chatMessages').append(messageHtml);
      // Scroll to bottom of chat messages
      $('#chatMessages').scrollTop($('#chatMessages')[0].scrollHeight);
    }
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

// Proper Logout Mechanism
async function Logout(){
  await $.ajax({
      url: `/api/logout/`,
      method: "POST",
      headers: {
          'Authorization': `Bearer ${token}`,
          'X-CSRFToken': csrftoken
      },
      success: function (response, status, xhr) {
          localStorage.removeItem('LoginToken');
          if (response['success']) {
              window.location.href = "http://localhost:5000/api/login/"; 
          } else {
              console.log(response);
          }
      },
      error: function (xhr, status, error) {
          window.location.href = "http://localhost:5000/api/login/";
          // Handle errors (e.g., show an error message)
          console.log("Error: " + error);
          console.log("Status: " + status);
          console.log("Response: " + xhr.responseText);
      
      // Check the response text for a specific error message
      try {
          var response = JSON.parse(xhr.responseText);
          var messageText = '';
  
          for (var key in response) {
              if (response.hasOwnProperty(key)) {
                  messageText += key + ': ' + response[key] + '\n';
              }
          }     
          $('#message').text(messageText).css('color', 'red');
          // alert(messageText)
      } catch (e) {
          $('#message').text('An error occurred, but the response could not be parsed.').css('color', 'red');
          // alert('An error occurred, but the response could not be parsed.')
      }
  }
  });
}
