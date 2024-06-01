let form,
  loadingSpinner;

document.addEventListener('DOMContentLoaded', (event) => {
  form = document.querySelector('form')
  loadingSpinner = document.querySelector('.loadingSpinner')
  form.addEventListener('submit', handleSubmit)
});

async function handleSubmit(ev) {
  ev.preventDefault()
  const { target } = ev
  loadingSpinner.style.display = 'block'
  const res = await fetch('/api/translate', {
    method: 'POST',
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      text: target.text.value,
      target_lang: target.target_lang.value,
      correlation: target.correlation.value,
    })
  })
  .then(res => res.json())
  loadingSpinner.style.display = 'none'
  document.querySelector('.res').innerText = res.result
}