/**
 * Inicializa os listeners de eventos quando o DOM está pronto
 */
document.addEventListener('DOMContentLoaded', () => {
    // Formulário da Calculadora de Alunos
    const formCalculadoraAlunos = document.getElementById('formCalculadoraAlunos');
    if (formCalculadoraAlunos) {
        formCalculadoraAlunos.addEventListener('submit', handleCalculaAlunosFiltros);
    }

    // Formulário do Ranking de Cursos
    const formRankingCursos = document.getElementById('formRankingCursos');
    if (formRankingCursos) {
        formRankingCursos.addEventListener('submit', handleListaRankingCursos);
    }
});


/**
 * Manipula o submit do formulário de filtros da calculadora de alunos
 * @param {Event} event - Evento de submit
 */
function handleCalculaAlunosFiltros(event) {
    event.preventDefault();

    document.getElementById('contadorAlunos').innerText = 'Carregando...';
    
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

/**
 * Manipula o submit do formulário de filtros do ranking de cursos
 * @param {Event} event - Evento de submit
 */
async function handleListaRankingCursos(event) {
    event.preventDefault();

    const tbody = document.getElementById('rankingCursosTbody');
    if (!tbody) {
        console.error('Elemento tbody para o ranking de cursos não encontrado.');
        return;
    }

    // Mostrar indicador de carregamento (opcional)
    tbody.innerHTML = '<tr><td colspan="6" class="text-center py-4">Carregando ranking...</td></tr>';

    // Capturar valores dos filtros do ranking
    const modalidade = document.getElementById('filtroModalidadeRanking').value;
    const estado = document.getElementById('filtroEstadoRanking').value;

    try {
        const data = await fetchRankingCursos(modalidade, estado);
        
        if (data.status === 'ok' && data.cursos) {
            if (data.cursos.length > 0) {
                tbody.innerHTML = ''; // Limpar conteúdo anterior
                data.cursos.forEach(curso => {
                    const row = tbody.insertRow();
                    row.innerHTML = `
                        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${curso.nome_curso || ''}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${curso.nome_detalhado_curso || ''}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${curso.modalidade || ''}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${curso.grau || ''}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${curso.estado || ''}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${curso.matriculas || 0}</td>
                    `;
                });
            } else {
                tbody.innerHTML = '<tr><td colspan="6" class="text-center py-4">Nenhum curso encontrado para os filtros aplicados.</td></tr>';
            }
        } else {
            console.error('Erro ao buscar ranking de cursos:', data);
            tbody.innerHTML = '<tr><td colspan="6" class="text-center py-4">Erro ao carregar o ranking. Tente novamente.</td></tr>';
        }
    } catch (error) {
        console.error('Erro ao buscar ranking de cursos:', error);
        tbody.innerHTML = '<tr><td colspan="6" class="text-center py-4">Erro ao carregar o ranking. Verifique o console para mais detalhes.</td></tr>';
    }
}
