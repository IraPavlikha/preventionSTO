document.getElementById('serviceForm').addEventListener('submit', function(event) {
  event.preventDefault();

  const formData = {
    fullName: document.getElementById('fullName').value,
    phoneNumber: document.getElementById('phoneNumber').value,
    email: document.getElementById('email').value,
    telegramUser: document.getElementById('telegramUser').value
  };

  console.log('Відправлені дані:', formData);

  fetch('http://127.0.0.1:5002/submit_form', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(formData)
  })
  .then(response => response.json())
  .then(data => {
    if (data.status === 'success') {
      alert('Форму успішно відправлено!');
    } else {
      alert('Сталася помилка при відправці форми.');
    }
  })
  .catch(error => {
    console.error('Error:', error);
    alert('Сталася помилка при відправці форми.');
  });
});
