// RELATÓRIO - FUNCIONALIDADES INTERATIVAS

// Dados globais
let dadosOriginais = [];
let dadosFiltrados = [];

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    inicializarRelatorio();
    carregarDadosTabela();
    popularFiltros();
    configurarEventListeners();
});

// Inicializar relatório
function inicializarRelatorio() {
    console.log('📊 Relatório iniciado - Eureka do Padre');
}

// Carregar dados da tabela para manipulação
function carregarDadosTabela() {
    const tabela = document.getElementById('tabelaRelatorio');
    const linhas = tabela.querySelectorAll('tbody tr');
    
    dadosOriginais = Array.from(linhas).map(linha => {
        const celulas = linha.querySelectorAll('td');
        const perguntaCompleta = linha.querySelector('.pergunta-expandida');
        const perguntaTexto = perguntaCompleta ? perguntaCompleta.textContent : '';
        
        // Verificar se alguma equipe acertou
        const equipesResultados = linha.querySelectorAll('.equipe-resultado');
        const temAcerto = Array.from(equipesResultados).some(eq => 
            eq.querySelector('.resultado-texto').textContent.includes('Acertou')
        );
        
        return {
            elemento: linha,
            rodada: parseInt(celulas[0].textContent.trim()),
            turma: celulas[1].textContent.trim(),
            tema: celulas[2].textContent.trim(),
            pergunta: perguntaTexto,
            acertou: temAcerto
        };
    });
    
    dadosFiltrados = [...dadosOriginais];
}

// Popular dropdowns dos filtros
function popularFiltros() {
    const turmas = [...new Set(dadosOriginais.map(d => d.turma))].sort();
    const temas = [...new Set(dadosOriginais.map(d => d.tema))].sort();
    
    popularSelect('filtroTurma', turmas);
    popularSelect('filtroTema', temas);
}

// Popular select com opções
function popularSelect(id, opcoes) {
    const select = document.getElementById(id);
    opcoes.forEach(opcao => {
        const option = document.createElement('option');
        option.value = opcao;
        option.textContent = opcao;
        select.appendChild(option);
    });
}

// Aplicar filtros
function aplicarFiltros() {
    const filtroTurma = document.getElementById('filtroTurma').value;
    const filtroTema = document.getElementById('filtroTema').value;
    const filtroAcerto = document.getElementById('filtroAcerto').value;
    
    dadosFiltrados = dadosOriginais.filter(item => {
        return (!filtroTurma || item.turma === filtroTurma) &&
               (!filtroTema || item.tema === filtroTema) &&
               (!filtroAcerto || item.acertou.toString() === filtroAcerto);
    });
    
    atualizarTabela();
    atualizarEstatisticas();
    
    // Feedback visual
    const btnFiltrar = document.querySelector('.btn-filtrar');
    const textoOriginal = btnFiltrar.textContent;
    btnFiltrar.textContent = '✅ Aplicado!';
    btnFiltrar.style.background = 'linear-gradient(135deg, #48bb78, #38a169)';
    
    setTimeout(() => {
        btnFiltrar.textContent = textoOriginal;
        btnFiltrar.style.background = '';
    }, 1500);
}

// Limpar filtros
function limparFiltros() {
    document.getElementById('filtroTurma').value = '';
    document.getElementById('filtroTema').value = '';
    document.getElementById('filtroAcerto').value = '';
    
    dadosFiltrados = [...dadosOriginais];
    atualizarTabela();
    atualizarEstatisticas();
    
    // Feedback visual
    const btnLimpar = document.querySelector('.btn-limpar');
    const textoOriginal = btnLimpar.textContent;
    btnLimpar.textContent = '🗑️ Limpo!';
    
    setTimeout(() => {
        btnLimpar.textContent = textoOriginal;
    }, 1500);
}

// Atualizar tabela com dados filtrados
function atualizarTabela() {
    const corpoTabela = document.getElementById('corpoTabela');
    
    // Esconder todas as linhas
    dadosOriginais.forEach(item => {
        item.elemento.style.display = 'none';
    });
    
    // Mostrar apenas as filtradas
    dadosFiltrados.forEach(item => {
        item.elemento.style.display = '';
    });
    
    // Atualizar contador
    const contador = document.getElementById('contadorResultados');
    contador.textContent = `Mostrando ${dadosFiltrados.length} de ${dadosOriginais.length} rodadas`;
}

// Atualizar estatísticas
function atualizarEstatisticas() {
    const totalRodadas = dadosFiltrados.length;
    
    // Calcular total de participações e acertos baseado nas equipes
    let totalParticipacoes = 0;
    let totalAcertos = 0;
    
    dadosFiltrados.forEach(rodada => {
        const equipesResultados = rodada.elemento.querySelectorAll('.equipe-resultado');
        totalParticipacoes += equipesResultados.length;
        
        equipesResultados.forEach(equipeEl => {
            const resultado = equipeEl.querySelector('.resultado-texto').textContent.trim();
            if (resultado.includes('Acertou')) {
                totalAcertos++;
            }
        });
    });
    
    const totalErros = totalParticipacoes - totalAcertos;
    const taxa = totalParticipacoes > 0 ? ((totalAcertos / totalParticipacoes) * 100).toFixed(1) : 0;
    
    document.getElementById('totalRodadas').textContent = totalRodadas;
    document.getElementById('totalAcertos').textContent = totalAcertos;
    document.getElementById('totalErros').textContent = totalErros;
    document.getElementById('taxaAcerto').textContent = taxa + '%';
}

// Ordenação da tabela
let ordemCrescente = {};

function ordenarTabela(coluna) {
    const propriedades = ['rodada', 'turma', 'tema', 'pergunta', 'acertou'];
    const prop = propriedades[coluna];
    
    if (!ordemCrescente.hasOwnProperty(coluna)) {
        ordemCrescente[coluna] = true;
    } else {
        ordemCrescente[coluna] = !ordemCrescente[coluna];
    }
    
    dadosFiltrados.sort((a, b) => {
        let valA = a[prop];
        let valB = b[prop];
        
        // Tratamento especial para números
        if (prop === 'rodada') {
            return ordemCrescente[coluna] ? valA - valB : valB - valA;
        }
        
        // Tratamento especial para booleanos
        if (prop === 'acertou') {
            return ordemCrescente[coluna] ? valA - valB : valB - valA;
        }
        
        // Strings
        if (typeof valA === 'string') {
            valA = valA.toLowerCase();
            valB = valB.toLowerCase();
        }
        
        if (ordemCrescente[coluna]) {
            return valA < valB ? -1 : valA > valB ? 1 : 0;
        } else {
            return valA > valB ? -1 : valA < valB ? 1 : 0;
        }
    });
    
    atualizarTabela();
    
    // Atualizar indicador visual na header
    atualizarIndicadorOrdenacao(coluna);
}

// Atualizar indicador de ordenação
function atualizarIndicadorOrdenacao(colunaAtiva) {
    const headers = document.querySelectorAll('#tabelaRelatorio th');
    
    headers.forEach((header, index) => {
        const texto = header.textContent.replace(/\s*↕️|↑|↓/g, '');
        
        if (index === colunaAtiva) {
            const simbolo = ordemCrescente[colunaAtiva] ? ' ↑' : ' ↓';
            header.textContent = texto + simbolo;
        } else {
            header.textContent = texto + ' ↕️';
        }
    });
}

// Exportar para PDF
function exportarPDF() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF('l', 'mm', 'a4'); // landscape
    
    // Título
    doc.setFontSize(20);
    doc.setFont(undefined, 'bold');
    doc.text('📊 Relatório - Eureka do Padre', 20, 20);
    
    // Subtítulo
    doc.setFontSize(12);
    doc.setFont(undefined, 'normal');
    doc.text(`Gerado em: ${new Date().toLocaleString('pt-BR')}`, 20, 30);
    doc.text(`Total de registros: ${dadosFiltrados.length}`, 20, 37);
    
    // Preparar dados da tabela - versão completa para PDF
    const cabecalhos = ['Rodada', 'Turma', 'Tema', 'Equipe', 'Pergunta', 'Resposta', 'Resultado'];
    const dados = [];
    
    dadosFiltrados.forEach(item => {
        // Extrair pergunta e resposta do texto completo
        const perguntaTexto = item.pergunta.replace(/Pergunta:\s*/, '').replace(/\s*Resposta:.*/, '').trim();
        const respostaTexto = item.pergunta.replace(/.*Resposta:\s*/, '').trim();
        
        // Buscar resultados de todas as equipes para esta rodada
        const equipesResultados = item.elemento.querySelectorAll('.equipe-resultado');
        
        if (equipesResultados.length > 0) {
            equipesResultados.forEach(equipeEl => {
                const nomeEquipe = equipeEl.querySelector('.equipe-nome').textContent.trim();
                const resultado = equipeEl.querySelector('.resultado-texto').textContent.trim();
                
                dados.push([
                    item.rodada,
                    item.turma,
                    item.tema,
                    nomeEquipe,
                    perguntaTexto,
                    respostaTexto,
                    resultado
                ]);
            });
        } else {
            // Fallback caso não encontre equipes
            dados.push([
                item.rodada,
                item.turma,
                item.tema,
                'N/A',
                perguntaTexto,
                respostaTexto,
                item.acertou ? 'Acerto' : 'Erro'
            ]);
        }
    });
    
    // Gerar tabela
    doc.autoTable({
        head: [cabecalhos],
        body: dados,
        startY: 45,
        styles: {
            fontSize: 8,
            cellPadding: 3
        },
        headStyles: {
            fillColor: [66, 153, 225],
            textColor: 255,
            fontStyle: 'bold'
        },
        alternateRowStyles: {
            fillColor: [247, 250, 252]
        },
        columnStyles: {
            0: { halign: 'center', cellWidth: 20 },
            1: { cellWidth: 30 },
            2: { cellWidth: 35 },
            3: { cellWidth: 25 },
            4: { cellWidth: 30 },
            5: { cellWidth: 80 },
            6: { halign: 'center', cellWidth: 25 }
        }
    });
    
    // Salvar arquivo
    const nomeArquivo = `relatorio_eureka_${new Date().toISOString().split('T')[0]}.pdf`;
    doc.save(nomeArquivo);
    
    // Feedback
    mostrarFeedbackExport('PDF exportado com sucesso!', 'success');
}

// Exportar para Excel
function exportarExcel() {
    // Preparar dados - versão completa para Excel
    const dados = [];
    
    dadosFiltrados.forEach(item => {
        // Extrair pergunta e resposta do texto completo
        const perguntaTexto = item.pergunta.replace(/Pergunta:\s*/, '').replace(/\s*Resposta:.*/, '').trim();
        const respostaTexto = item.pergunta.replace(/.*Resposta:\s*/, '').trim();
        
        // Buscar resultados de todas as equipes para esta rodada
        const equipesResultados = item.elemento.querySelectorAll('.equipe-resultado');
        
        if (equipesResultados.length > 0) {
            equipesResultados.forEach(equipeEl => {
                const nomeEquipe = equipeEl.querySelector('.equipe-nome').textContent.trim();
                const resultado = equipeEl.querySelector('.resultado-texto').textContent.trim();
                
                dados.push({
                    'Rodada': item.rodada,
                    'Turma': item.turma,
                    'Tema': item.tema,
                    'Equipe': nomeEquipe,
                    'Pergunta': perguntaTexto,
                    'Resposta': respostaTexto,
                    'Resultado': resultado
                });
            });
        } else {
            // Fallback caso não encontre equipes
            dados.push({
                'Rodada': item.rodada,
                'Turma': item.turma,
                'Tema': item.tema,
                'Equipe': 'N/A',
                'Pergunta': perguntaTexto,
                'Resposta': respostaTexto,
                'Resultado': item.acertou ? 'Acerto' : 'Erro'
            });
        }
    });
    
    // Criar workbook
    const wb = XLSX.utils.book_new();
    const ws = XLSX.utils.json_to_sheet(dados);
    
    // Ajustar largura das colunas
    const colWidths = [
        { wch: 10 }, // Rodada
        { wch: 15 }, // Turma
        { wch: 20 }, // Tema
        { wch: 20 }, // Equipe
        { wch: 50 }, // Pergunta
        { wch: 30 }, // Resposta
        { wch: 12 }  // Resultado
    ];
    ws['!cols'] = colWidths;
    
    // Adicionar planilha ao workbook
    XLSX.utils.book_append_sheet(wb, ws, 'Relatório');
    
    // Salvar arquivo
    const nomeArquivo = `relatorio_eureka_${new Date().toISOString().split('T')[0]}.xlsx`;
    XLSX.writeFile(wb, nomeArquivo);
    
    // Feedback
    mostrarFeedbackExport('Planilha exportada com sucesso!', 'success');
}

// Mostrar feedback de exportação
function mostrarFeedbackExport(mensagem, tipo) {
    // Criar elemento de feedback
    const feedback = document.createElement('div');
    feedback.className = `feedback-export ${tipo}`;
    feedback.innerHTML = `
        <div class="feedback-content">
            <span class="feedback-icon">${tipo === 'success' ? '✅' : '❌'}</span>
            <span class="feedback-texto">${mensagem}</span>
        </div>
    `;
    
    // Adicionar estilos
    feedback.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${tipo === 'success' ? '#48bb78' : '#f56565'};
        color: white;
        padding: 15px 25px;
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        z-index: 1000;
        transform: translateX(100%);
        transition: transform 0.3s ease;
    `;
    
    // Adicionar ao DOM
    document.body.appendChild(feedback);
    
    // Animar entrada
    setTimeout(() => {
        feedback.style.transform = 'translateX(0)';
    }, 100);
    
    // Remover após 3 segundos
    setTimeout(() => {
        feedback.style.transform = 'translateX(100%)';
        setTimeout(() => {
            document.body.removeChild(feedback);
        }, 300);
    }, 3000);
}

// Utilitário para busca rápida
function buscarRapida(termo) {
    if (!termo) {
        dadosFiltrados = [...dadosOriginais];
        atualizarTabela();
        return;
    }
    
    termo = termo.toLowerCase();
    dadosFiltrados = dadosOriginais.filter(item =>
        item.turma.toLowerCase().includes(termo) ||
        item.tema.toLowerCase().includes(termo) ||
        item.pergunta.toLowerCase().includes(termo)
    );
    
    atualizarTabela();
    atualizarEstatisticas();
}

// Configurar event listeners
function configurarEventListeners() {
    // Event listeners para botões de expansão
    document.addEventListener('click', function(e) {
        if (e.target.closest('.btn-expandir-pergunta')) {
            const botao = e.target.closest('.btn-expandir-pergunta');
            const indice = botao.dataset.rodada;
            togglePergunta(indice);
        }
        
        if (e.target.closest('.btn-expandir-resultado')) {
            const botao = e.target.closest('.btn-expandir-resultado');
            const indice = botao.dataset.rodada;
            toggleResultado(indice);
        }
    });
}

// Função para expandir/contrair pergunta
function togglePergunta(indice) {
    const perguntaCompleta = document.getElementById(`pergunta-${indice}`);
    const botao = document.querySelector(`[data-rodada="${indice}"][data-tipo="pergunta"]`);
    const seta = botao.querySelector('.seta-down');
    
    if (perguntaCompleta.style.display === 'none') {
        perguntaCompleta.style.display = 'block';
        seta.classList.add('rotated');
        botao.title = 'Ocultar pergunta';
    } else {
        perguntaCompleta.style.display = 'none';
        seta.classList.remove('rotated');
        botao.title = 'Ver pergunta completa';
    }
}

// Função para expandir/contrair resultado
function toggleResultado(indice) {
    const resultadoCompleto = document.getElementById(`resultado-${indice}`);
    const botao = document.querySelector(`[data-rodada="${indice}"][data-tipo="resultado"]`);
    const seta = botao.querySelector('.seta-down');
    
    if (resultadoCompleto.style.display === 'none') {
        resultadoCompleto.style.display = 'block';
        seta.classList.add('rotated');
        botao.title = 'Ocultar resultado';
    } else {
        resultadoCompleto.style.display = 'none';
        seta.classList.remove('rotated');
        botao.title = 'Ver resultado';
    }
}
