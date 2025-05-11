let objetivoSalvo = false;

// Salvar objetivo no localStorage
function salvarObjetivo() {
  const como = document.getElementById('como').value.trim();
  const quando = document.getElementById('quando').value.trim();
  const resultados = document.getElementById('resultados').value.trim();
  const ajudas = document.getElementById('ajudas').value.trim();

  if (!como && !quando && !resultados && !ajudas) {
    alert('Por favor, preencha pelo menos um campo.');
    return;
  }

  const novoObjetivo = { como, quando, resultados, ajudas };
  const objetivos = JSON.parse(localStorage.getItem('objetivos') || '[]');
  objetivos.push(novoObjetivo);
  localStorage.setItem('objetivos', JSON.stringify(objetivos));

  alert('Objetivo salvo com sucesso!');
  objetivoSalvo = true;
  listarObjetivos();
}

// Listar os objetivos do localStorage
function listarObjetivos() {
  const lista = document.getElementById('lista-tarefas');
  lista.innerHTML = '';

  const objetivos = JSON.parse(localStorage.getItem('objetivos') || '[]');
  objetivos.forEach((obj, index) => {
    const div = document.createElement('div');
    div.className = 'tarefa';
    div.innerHTML = `
      <p><strong>O que:</strong> ${obj.como}</p>
      <p><strong>Quando:</strong> ${obj.quando}</p>
      <p><strong>Resultados:</strong> ${obj.resultados}</p>
      <p><strong>Ajudas:</strong> ${obj.ajudas}</p>
      <button class="botao-excluir" onclick="excluirObjetivo(${index})">🗑️</button>
    `;
    lista.appendChild(div);
  });
}

// Excluir objetivo
function excluirObjetivo(index) {
  if (!confirm('Deseja realmente excluir este objetivo?')) return;
  const objetivos = JSON.parse(localStorage.getItem('objetivos') || '[]');
  objetivos.splice(index, 1);
  localStorage.setItem('objetivos', JSON.stringify(objetivos));
  listarObjetivos();
}

// Preencher data da assinatura
function preencherDataAssinatura() {
  const data = new Date();
  document.getElementById('data-assinatura').textContent = `📅 Assinado em: ${data.toLocaleDateString('pt-BR')}`;
}

// Alerta ao sair sem salvar
window.addEventListener('beforeunload', function (e) {
  if (!objetivoSalvo) {
    e.preventDefault();
    e.returnValue = 'Você tem alterações não salvas. Deseja mesmo sair?';
  }
});

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('salvarObjetivo').addEventListener('click', salvarObjetivo);
  document.getElementById('voltar').addEventListener('click', () => {
    window.location.href = 'index.html';
  });

  preencherDataAssinatura();
  listarObjetivos();
});
