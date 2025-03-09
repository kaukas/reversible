const validityLabels = {
  null: 'Validity check pending',
  true: 'Valid',
  false: 'Invalid'
}
const reversibilityLabels = {
  null: 'Reversibility check pending',
  true: 'Reversible',
  false: 'Irreversible'
}

const badgeClasses = {
  null: 'badge-light',
  true: 'badge-success',
  false: 'badge-danger'
}

fetch('http://127.0.0.1:8000/images').then(async (resp) => {
  const { images } = await resp.json();
  images.forEach((image) => {
    const container = document.createElement('li');
    document.getElementById('images').appendChild(container);
    container.classList.add('list-group-item');
    container.innerHTML = `
<span class="filename"></span> <span class="valid badge"></span> <span class="reversible badge"></span>
    `;
    container.querySelector('.filename').innerText = image.filename;

    const validText = container.querySelector('.valid');
    validText.innerText = validityLabels[image.valid_image];
    validText.classList.add(badgeClasses[image.valid_image]);

    const reversibleText = container.querySelector('.reversible');
    reversibleText.innerText = reversibilityLabels[image.reversible];
    reversibleText.classList.add(badgeClasses[image.reversible]);
  })
});

document.querySelector('form').addEventListener('submit', (e) => {
  e.preventDefault();
  const form = e.target;
  fetch(form.getAttribute('action'), { body: new FormData(form), method: form.getAttribute('method') }).
    then((resp) => {
      if (resp.status === 200) {
        window.location.reload();
      }
    });
})
