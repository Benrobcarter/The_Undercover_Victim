
fetch('consolidated_master.json')
  .then(response => response.json())
  .then(data => {
    const output = document.getElementById('output');
    output.innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
  })
  .catch(error => {
    document.getElementById('output').innerText = 'Failed to load data: ' + error;
  });
