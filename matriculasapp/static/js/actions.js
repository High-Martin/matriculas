/**
 * As ações são funções que se comunicam com a API
 * para buscar dados.
 */

/**
 * Faz uma requisição para o endpoint de contagem de alunos
 * @param {string|null} ano - Ano da matrícula
 * @param {string|null} modalidade - Modalidade do curso
 * @param {string|null} estado - Estado da instituição
 * @returns {Promise} - Promise com resultado da requisição
 */
async function fetchCountAlunos(ano = null, modalidade = null, estado = null) {
    // Construir URL com parâmetros
    const params = new URLSearchParams();
    if (ano) params.append('ano', ano);
    if (modalidade) params.append('modalidade', modalidade);
    if (estado) params.append('estado', estado);
    
    const url = `count_alunos/?${params.toString()}`;
    
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Erro na requisição: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Resposta recebida:', data);
        return data;
    } catch (error) {
        console.error('Erro ao buscar contagem de alunos:', error);
        throw error;
    }
}

/**
 * Testa a conexão com a API para validar o funcionamento
 */
async function testApiConnection() {
    try {
        const result = await fetchCountAlunos();
        console.log('Conexão com API testada com sucesso:', result);
        
        // Aqui você poderia mostrar alguma notificação na UI se desejar
        if (result.status === 'ok') {
            console.log('API retornou status OK');
        }
    } catch (error) {
        console.error('Falha ao testar conexão com a API:', error);
    }
}

/**
 * Faz uma requisição para o endpoint de ranking de cursos
 * @param {string|null} modalidade - Modalidade do curso
 * @param {string|null} estado - Estado da instituição
 * @returns {Promise} - Promise com resultado da requisição
 */
async function fetchRankingCursos(modalidade = null, estado = null) {
    // Construir URL com parâmetros
    const params = new URLSearchParams();
    if (modalidade) params.append('modalidade', modalidade);
    if (estado) params.append('estado', estado);
    
    const url = `ranking_cursos/?${params.toString()}`;
    
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Erro na requisição: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Resposta recebida:', data);
        return data;
    } catch (error) {
        console.error('Erro ao buscar ranking de cursos:', error);
        throw error;
    }
}