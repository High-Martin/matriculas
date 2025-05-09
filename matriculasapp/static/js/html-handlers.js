
/**
 * Inicializa os listeners de eventos quando o DOM está pronto
 */
document.addEventListener('DOMContentLoaded', () => {
    // Botão de filtro no dashboard
    const filterButton = document.querySelector('button[type="submit"]');
    if (filterButton) {
        filterButton.addEventListener('click', handleFiltroClick);
    }
});


/**
 * Manipula o clique no botão de filtro
 * @param {Event} event - Evento de clique
 */
function handleFiltroClick(event) {
    event.preventDefault();

    document.getElementById('contadorAlunos').innerText = '...';
    
    // Capturar valores dos filtros
    const ano = document.getElementById('filtroAno').value;
    const modalidade = document.getElementById('filtroModalidade').value;
    const estado = document.getElementById('filtroEstado').value;
    
    // Executar a busca com os filtros
    fetchCountAlunos(ano, modalidade, estado)
        .then(data => {
            count = data.count;
            //add '.' at every 3 digits
            count = count.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
            document.getElementById('contadorAlunos').innerText = count;
            // Aqui você atualizaria a UI com os dados recebidos
        })
        .catch(error => {
            console.error('Erro ao aplicar filtros:', error);
        });
}
