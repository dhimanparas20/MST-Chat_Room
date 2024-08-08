const csrftoken = getCookie('csrftoken');
const token = localStorage.getItem('LoginToken'); 
let username = null;
var socket = null; // Initialize WebSocket variable
var baseUrl = window.location.protocol + "//" + window.location.host;


$(document).ready(function() {
    $('#status').text("Disconnected");
    $('#status').css("color","red");
    console.log(WEBSOCKET_URL)
    console.log(`Token: ${token}`)
    username = $('#username').text()
    console.log("Current User: "+username)
  
    // Function to join a chat room
    $('#joinChatBtn').click(function() {
      const roomId = $('#roomIdInput').val().trim();
      console.log(`roomid: ${roomId}`);
      
      if (roomId !== '') {
        // Redirect to the chat room using WebSocket
        socket = new WebSocket(`${WEBSOCKET_URL}/chat/${roomId}/?token=${token}`);
      }
  
      socket.onopen = function() {
        console.log('WebSocket connection opened');
        $('#status').text(`Connected to ${roomId}`);
        $('#status').css("color","green");
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

    //generate random chat
    $('#genrandom').click(function() {
      // Define the characters to include in the random string
      const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
      let randomString = '';
  
      // Generate a random string of a specified length
      for (let i = 0; i < 6; i++) {  // 12 is an example length, you can change it
          const randomIndex = Math.floor(Math.random() * chars.length);
          randomString += chars[randomIndex];
      }
  
      // Set the generated string to the input field
      $('#roomIdInput').val(randomString);
    });

    //Leave a chat  
    $('#leaveChatBtn').click(function() {
      console.log("Leaving chat")
      $('#chatMessages').empty();
      $('#status').text("Disconnected");
      $('#status').css("color","red");
      socket.close();
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
      if (user===username){
        user = "You"
      }

      const messageClass = isSender ? 'my-message' : 'other-message';
      const messageHtml = `<div class="${messageClass}"><strong>${user}:</strong> ${message}</div>`;
      $('#chatMessages').append(messageHtml);

      // Apply color based on message content after appending to the DOM
      if (message.includes('left chat')) {
          $('#chatMessages .'+messageClass+':last').css("color", "red");
      } else if (message.includes('joined the chat')) {
          $('#chatMessages .'+messageClass+':last').css("color", "green");
      }

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
      url: `${baseUrl}/api/logout/`,
      method: "POST",
      headers: {
          'Authorization': `Bearer ${token}`,
          'X-CSRFToken': csrftoken
      },
      success: function (response, status, xhr) {
          localStorage.removeItem('LoginToken');
          if (response['success']) {
              window.location.href = `${baseUrl}/api/login/`; 
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
