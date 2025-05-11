document.addEventListener('DOMContentLoaded', function() {
    // Por enquanto, nada dinâmico no index
    console.log("Página index carregada!");
  });
  document.addEventListener('DOMContentLoaded', async () => {
  try {
    const resposta = await fetch('http://localhost:5000/usuario_logado', {
      method: 'GET',
      credentials: 'include'
    });

    const data = await resposta.json();

    if (resposta.ok && data.username) {
      document.getElementById('sessao-usuario').textContent = `Olá, ${data.username}`;
      document.getElementById('logout-btn').style.display = 'inline-block';
    } else {
      document.getElementById('sessao-usuario').textContent = 'Olá';
    }
  } catch (error) {
    console.error('Erro ao verificar sessão:', error);
  }

  document.getElementById('logout-btn').addEventListener('click', async () => {
    try {
      await fetch('http://localhost:5000/logout', {
        method: 'POST',
        credentials: 'include'
      });
      location.reload();
    } catch (error) {
      alert('Erro ao fazer logout');
    }
  });
});
