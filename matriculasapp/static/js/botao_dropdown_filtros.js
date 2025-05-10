document.addEventListener('DOMContentLoaded', () => {
    const btnAbrirDropdownFiltros = document.getElementById('btnAbrirDropdownFiltros');
    const dropdownFiltrosAlunos = document.getElementById('dropdownFiltrosAlunos');
    const dropdownFiltrosAlunosItens = document.getElementById('dropdownFiltrosAlunosItens');
    const btnRecarregarFiltros = document.getElementById('btnRecarregarFiltros'); // Novo botão

    // Formulário e campos a serem preenchidos
    const formCalculadoraAlunos = document.getElementById('formCalculadoraAlunos');
    const filtroAnoSelect = document.getElementById('filtroAno');
    const filtroModalidadeSelect = document.getElementById('filtroModalidade');
    const filtroEstadoInput = document.getElementById('filtroEstado');

    let dropdownCarregado = false;

    async function carregarFiltros() {
        dropdownFiltrosAlunosItens.innerHTML = '<p class="px-4 py-2 text-sm text-gray-500">Carregando filtros...</p>';

        try {
            // Certifique-se de que esta URL está correta e configurada no seu Django urls.py
            const response = await fetch('filtro_alunos/');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();

            dropdownFiltrosAlunosItens.innerHTML = ''; // Limpa o placeholder "Carregando..."

            if (data.filtros_alunos && data.filtros_alunos.length > 0) {
                data.filtros_alunos.forEach(filtro => {
                    const item = document.createElement('a');
                    item.href = '#';
                    item.classList.add('block', 'px-4', 'py-2', 'text-sm', 'text-gray-700', 'hover:bg-gray-100', 'hover:text-gray-900');
                    item.setAttribute('role', 'menuitem');
                    // Modificado para usar innerHTML e adicionar quebras de linha
                    item.innerHTML = `Ano: ${filtro.ano}<br>Modalidade: ${filtro.modalidade || 'Todas modalidades'}<br>Estado: ${filtro.estado || 'Todos'}`;

                    item.addEventListener('click', (e) => {
                        e.preventDefault();
                        if (filtroAnoSelect) filtroAnoSelect.value = filtro.ano;
                        if (filtroModalidadeSelect) filtroModalidadeSelect.value = filtro.modalidade;
                        if (filtroEstadoInput) filtroEstadoInput.value = filtro.estado || '';

                        // Opcional: Submeter o formulário ou disparar um evento
                        // formCalculadoraAlunos.dispatchEvent(new Event('submit', { cancelable: true }));
                        
                        dropdownFiltrosAlunos.classList.add('hidden');
                        btnAbrirDropdownFiltros.setAttribute('aria-expanded', 'false');
                    });
                    dropdownFiltrosAlunosItens.appendChild(item);
                });
            } else {
                dropdownFiltrosAlunosItens.innerHTML = '<p class="px-4 py-2 text-sm text-gray-500">Nenhum filtro salvo encontrado.</p>';
            }
            dropdownCarregado = true;
        } catch (error) {
            console.error('Erro ao carregar filtros:', error);
            dropdownFiltrosAlunosItens.innerHTML = '<p class="px-4 py-2 text-sm text-red-500">Erro ao carregar filtros.</p>';
            dropdownCarregado = false; // Garante que tentará carregar novamente em caso de erro
        }
    }

    if (btnAbrirDropdownFiltros && dropdownFiltrosAlunos) {
        btnAbrirDropdownFiltros.addEventListener('click', () => {
            const isExpanded = btnAbrirDropdownFiltros.getAttribute('aria-expanded') === 'true';
            if (isExpanded) {
                dropdownFiltrosAlunos.classList.add('hidden');
                btnAbrirDropdownFiltros.setAttribute('aria-expanded', 'false');
            } else {
                dropdownFiltrosAlunos.classList.remove('hidden');
                btnAbrirDropdownFiltros.setAttribute('aria-expanded', 'true');
                if (!dropdownCarregado) { // Só carrega automaticamente ao abrir se não tiver sido carregado antes
                    carregarFiltros();
                }
            }
        });

        // Event listener para o botão de recarregar
        if (btnRecarregarFiltros) {
            btnRecarregarFiltros.addEventListener('click', (e) => {
                e.stopPropagation(); // Impede que o evento de clique feche o dropdown
                dropdownCarregado = false; // Força o recarregamento
                carregarFiltros();
            });
        }

        // Fechar ao clicar fora
        document.addEventListener('click', (event) => {
            if (!btnAbrirDropdownFiltros.contains(event.target) && !dropdownFiltrosAlunos.contains(event.target)) {
                dropdownFiltrosAlunos.classList.add('hidden');
                btnAbrirDropdownFiltros.setAttribute('aria-expanded', 'false');
            }
        });
    } else {
        console.warn('Botão de dropdown ou container do dropdown não encontrado.');
    }
});
