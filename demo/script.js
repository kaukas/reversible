fetch('http://127.0.0.1:8000/images').then(async (resp) => {
  const { images } = await resp.json();
  images.forEach((image) => {
    const container = document.createElement('li');
    container.innerHTML = `
<span class="filename"></span> <span class="valid"></span> <span class="reversible"></span>
    `;
    container.querySelector('.filename').innerText = image.filename;
    container.querySelector('.valid').innerText =
      image.valid_image === null ? 'Not yet validated.' : image.valid_image ? 'Valid.' : 'Invalid.';
    container.querySelector('.reversible').innerText =
      image.reversible === null ? 'Reversibility check pending.' :
      image.reversible ? 'Reversible' : 'Irreversible';
    document.getElementById('images').appendChild(container);
  })
});

document.querySelector('form').addEventListener('submit', (e) => {
  const form = e.target;
  fetch(form.getAttribute('action'), { body: new FormData(form), method: form.getAttribute('method') }).
    then((resp) => {
      if (resp.status === 200) {
        window.location.reload();
      }
    });
  e.preventDefault();
})
