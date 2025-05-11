// Atualiza a saudação na barra superior
function atualizarSaudacao() {
  const nomeUsuario = localStorage.getItem('username');
  document.getElementById('saudacaoUsuario').textContent = `Olá, ${nomeUsuario || 'Usuário'}`;
}

// Logout
async function fazerLogout() {
  if (confirm('Deseja realmente sair da sessão?')) {
    try {
      await fetch('http://localhost:5000/logout', {
        method: 'POST',
        credentials: 'include' // garante que cookies de sessão sejam enviados
      });

      // Limpa o nome do usuário do localStorage e redireciona
      localStorage.removeItem('username');
      window.location.href = 'login.html';
    } catch (error) {
      alert('Erro ao sair da sessão!');
    }
  }
}

// Adiciona eventos nos botões de logout
function adicionarEventosDeLogout() {
  document.getElementById('btnLogout').addEventListener('click', fazerLogout);
}

// Chama a função para atualizar a saudação e adicionar eventos de logout
document.addEventListener('DOMContentLoaded', function() {
  atualizarSaudacao();
  adicionarEventosDeLogout();
});
