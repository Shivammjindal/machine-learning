
async function S() {
    const response = await fetch('http://127.0.0.1:5000/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: 'ee',
        password: 'ees'
      })
    });
  
    const result = await response.json();
    console.log("Response:", result);
  }
  
S();