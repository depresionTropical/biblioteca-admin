const selectAutores = document.getElementById('autoresSelect');

// Hacer una solicitud a la API de FastAPI para obtener la lista de autores
fetch('http://localhost:8000/autores/')
  .then(response => response.json())
  .then(data => {
    // Iterar sobre los datos de los autores y crear opciones para el select
    data.forEach(autor => {
      const option = document.createElement('option');
      option.value = autor.id;
      option.text = `${autor.Nombre} ${autor.Apellido}`;
      selectAutores.appendChild(option);
    });
  })
  .catch(error => console.error('Error:', error));