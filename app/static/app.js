let form;

document.addEventListener('DOMContentLoaded', (event) => {
  form = document.querySelector('form')
  form.addEventListener('submit', handleSubmit)
});

async function handleSubmit(ev) {
  ev.preventDefault()
  const { target } = ev
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
  document.querySelector('.res').innerText = res.result
}