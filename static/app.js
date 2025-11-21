async function roll(expression) {
  const resultContainer = document.getElementById('result');
  resultContainer.textContent = 'Rolando...';

  try {
    const response = await fetch('/api/roll', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ expression })
    });

    const data = await response.json();

    if (!response.ok) {
      resultContainer.textContent = data.error || 'Erro ao processar a expressão.';
      return;
    }

    const rollsList = data.rolls.map((value, index) => `<li>Dado ${index + 1}: <strong>${value}</strong></li>`).join('');
    const keptList = data.kept.map((value, index) => `<li>Mantido ${index + 1}: <strong>${value}</strong></li>`).join('');

    resultContainer.innerHTML = `
      <div class="content">
        <h3>Expressão: <code>${data.expression}</code></h3>
        <p>Total: <strong>${data.total}</strong>${data.modifier ? ` (modificador ${data.modifier >= 0 ? '+' : ''}${data.modifier})` : ''}</p>
        <div class="lists">
          <p>Rolagens:</p>
          <ul>${rollsList}</ul>
          <p>Dados mantidos:</p>
          <ul>${keptList}</ul>
        </div>
      </div>
    `;
  } catch (error) {
    resultContainer.textContent = 'Não foi possível conectar à API.';
  }
}

function setupButtons() {
  document.querySelectorAll('button[data-expression]').forEach((button) => {
    button.addEventListener('click', () => roll(button.dataset.expression));
  });
}

function setupForm() {
  const form = document.getElementById('custom-form');
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const input = document.getElementById('expression');
    roll(input.value.trim());
  });
}

window.addEventListener('DOMContentLoaded', () => {
  setupButtons();
  setupForm();
});
