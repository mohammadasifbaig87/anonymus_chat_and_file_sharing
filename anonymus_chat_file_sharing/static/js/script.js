function fetchMessages() {
  fetch('/get_messages')
    .then(response => response.json())
    .then(data => {
      const chatBox = document.getElementById('chat-box');
      chatBox.innerHTML = '';
      data.forEach(entry => {
        const div = document.createElement('div');
        div.innerHTML = `<span>[${entry.time}]</span> ${entry.message}`;
        chatBox.appendChild(div);
      });
      chatBox.scrollTop = chatBox.scrollHeight;
    });
}

document.getElementById('message-form').addEventListener('submit', function(e) {
  e.preventDefault();
  const messageInput = document.getElementById('message-input');
  const formData = new FormData();
  formData.append('message', messageInput.value);

  fetch('/send_message', {
    method: 'POST',
    body: formData
  }).then(() => {
    messageInput.value = '';
    fetchMessages();
  });
});

document.getElementById('file-form').addEventListener('submit', function(e) {
  e.preventDefault();
  const fileInput = document.getElementById('file-input');
  const formData = new FormData();
  formData.append('file', fileInput.files[0]);

  fetch('/upload', {
    method: 'POST',
    body: formData
  }).then(() => {
    fileInput.value = '';
    fetchMessages();
  });
});

setInterval(fetchMessages, 1000);
fetchMessages();
