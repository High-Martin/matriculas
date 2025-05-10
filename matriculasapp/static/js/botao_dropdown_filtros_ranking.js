document.addEventListener('DOMContentLoaded', () => {
    const btnAbrirDropdownFiltrosRanking = document.getElementById('btnAbrirDropdownFiltrosRanking');
    const dropdownFiltrosRanking = document.getElementById('dropdownFiltrosRanking');
    const dropdownFiltrosRankingItens = document.getElementById('dropdownFiltrosRankingItens');
    const btnRecarregarFiltrosRanking = document.getElementById('btnRecarregarFiltrosRanking');

    // Formulário e campos a serem preenchidos para o ranking
    const formRankingCursos = document.getElementById('formRankingCursos'); // ID do formulário de ranking
    const filtroModalidadeRankingSelect = document.getElementById('filtroModalidadeRanking');
    const filtroEstadoRankingInput = document.getElementById('filtroEstadoRanking');

    let dropdownRankingCarregado = false;

    async function carregarFiltrosRanking() {
        dropdownFiltrosRankingItens.innerHTML = '<p class="px-4 py-2 text-sm text-gray-500">Carregando filtros...</p>';

        try {
            const response = await fetch('filtro_cursos'); // URL confirmada pelo usuário
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();

            dropdownFiltrosRankingItens.innerHTML = ''; 

            // Ajustar a chave conforme o retorno da sua API, ex: data.filtros_cursos_salvos
            if (data.filtros_cursos && data.filtros_cursos.length > 0) { 
                data.filtros_cursos.forEach(filtro => {
                    const item = document.createElement('a');
                    item.href = '#';
                    item.classList.add('block', 'px-4', 'py-2', 'text-sm', 'text-gray-700', 'hover:bg-gray-100', 'hover:text-gray-900');
                    item.setAttribute('role', 'menuitem');
                    
                    // Usar filtro.nome se disponível, senão montar a string com modalidade e estado
                    let displayText = filtro.nome || '';
                    if (!displayText) {
                        const modalidadeDisplay = filtro.modalidade || 'Todas modalidades';
                        const estadoDisplay = filtro.estado || 'Todos os estados';
                        displayText = `Modalidade: ${modalidadeDisplay}<br>Estado: ${estadoDisplay}`;
                    } else {
                        displayText += `<br><small>Modalidade: ${filtro.modalidade || 'N/A'}<br>Estado: ${filtro.estado || 'N/A'}</small>`;
                    }
                    item.innerHTML = displayText;

                    item.addEventListener('click', (e) => {
                        e.preventDefault();
                        if (filtroModalidadeRankingSelect) filtroModalidadeRankingSelect.value = filtro.modalidade || '';
                        if (filtroEstadoRankingInput) filtroEstadoRankingInput.value = filtro.estado || '';
                        
                        dropdownFiltrosRanking.classList.add('hidden');
                        btnAbrirDropdownFiltrosRanking.setAttribute('aria-expanded', 'false');
                    });
                    dropdownFiltrosRankingItens.appendChild(item);
                });
            } else {
                dropdownFiltrosRankingItens.innerHTML = '<p class="px-4 py-2 text-sm text-gray-500">Nenhum filtro de ranking salvo encontrado.</p>';
            }
            dropdownRankingCarregado = true;
        } catch (error) {
            console.error('Erro ao carregar filtros de ranking:', error);
            dropdownFiltrosRankingItens.innerHTML = '<p class="px-4 py-2 text-sm text-red-500">Erro ao carregar filtros de ranking.</p>';
            dropdownRankingCarregado = false; 
        }
    }

    if (btnAbrirDropdownFiltrosRanking && dropdownFiltrosRanking) {
        btnAbrirDropdownFiltrosRanking.addEventListener('click', () => {
            const isExpanded = btnAbrirDropdownFiltrosRanking.getAttribute('aria-expanded') === 'true';
            if (isExpanded) {
                dropdownFiltrosRanking.classList.add('hidden');
                btnAbrirDropdownFiltrosRanking.setAttribute('aria-expanded', 'false');
            } else {
                dropdownFiltrosRanking.classList.remove('hidden');
                btnAbrirDropdownFiltrosRanking.setAttribute('aria-expanded', 'true');
                if (!dropdownRankingCarregado) {
                    carregarFiltrosRanking();
                }
            }
        });

        if (btnRecarregarFiltrosRanking) {
            btnRecarregarFiltrosRanking.addEventListener('click', (e) => {
                e.stopPropagation(); 
                dropdownRankingCarregado = false; 
                carregarFiltrosRanking();
            });
        }

        document.addEventListener('click', (event) => {
            if (!btnAbrirDropdownFiltrosRanking.contains(event.target) && !dropdownFiltrosRanking.contains(event.target)) {
                dropdownFiltrosRanking.classList.add('hidden');
                btnAbrirDropdownFiltrosRanking.setAttribute('aria-expanded', 'false');
            }
        });
    } else {
        console.warn('Botão de dropdown de ranking ou container do dropdown não encontrado.');
    }
});
