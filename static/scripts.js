document.getElementById('registerForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const cpf = document.getElementById('registerCpf').value;
    const password = document.getElementById('registerPassword').value;
    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ cpf, password })
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.error('Error:', error));
});

document.getElementById('loginForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const cpf = document.getElementById('loginCpf').value;
    const password = document.getElementById('loginPassword').value;
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ cpf, password })
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.error('Error:', error));
});

document.getElementById('transactionForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const cpf = document.getElementById('transactionCpf').value;
    const app_name = document.getElementById('transactionAppName').value;
    const valor = document.getElementById('transactionValor').value;
    fetch('/transactions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ cpf, app_name, valor })
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.error('Error:', error));
});

document.getElementById('consultForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const cpf = document.getElementById('consultCpf').value;
    fetch(`/transactions/${cpf}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        const resultsDiv = document.getElementById('results');
        resultsDiv.innerHTML = JSON.stringify(data, null, 2);
    })
    .catch(error => console.error('Error:', error));
});