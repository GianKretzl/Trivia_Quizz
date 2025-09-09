// RELATÓRIO - FUNCIONALIDADES INTERATIVAS

// Dados globais
let dadosOriginais = [];
let dadosFiltrados = [];

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    inicializarRelatorio();
    carregarDadosTabela();
    popularFiltros();
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
        return {
            elemento: linha,
            rodada: parseInt(celulas[0].textContent.trim()),
            turma: celulas[1].textContent.trim(),
            equipe: celulas[2].textContent.trim(),
            cor: celulas[3].querySelector('.cor-nome').textContent.trim(),
            tema: celulas[4].textContent.trim(),
            pergunta: celulas[5].textContent.trim(),
            resposta: celulas[6].textContent.trim(),
            acertou: celulas[7].textContent.includes('Acerto')
        };
    });
    
    dadosFiltrados = [...dadosOriginais];
}

// Popular dropdowns dos filtros
function popularFiltros() {
    const turmas = [...new Set(dadosOriginais.map(d => d.turma))].sort();
    const equipes = [...new Set(dadosOriginais.map(d => d.equipe))].sort();
    const temas = [...new Set(dadosOriginais.map(d => d.tema))].sort();
    
    popularSelect('filtroTurma', turmas);
    popularSelect('filtroEquipe', equipes);
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
    const filtroEquipe = document.getElementById('filtroEquipe').value;
    const filtroTema = document.getElementById('filtroTema').value;
    const filtroAcerto = document.getElementById('filtroAcerto').value;
    
    dadosFiltrados = dadosOriginais.filter(item => {
        return (!filtroTurma || item.turma === filtroTurma) &&
               (!filtroEquipe || item.equipe === filtroEquipe) &&
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
    document.getElementById('filtroEquipe').value = '';
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
    const total = dadosFiltrados.length;
    const acertos = dadosFiltrados.filter(d => d.acertou).length;
    const erros = total - acertos;
    const taxa = total > 0 ? ((acertos / total) * 100).toFixed(1) : 0;
    
    document.getElementById('totalRodadas').textContent = total;
    document.getElementById('totalAcertos').textContent = acertos;
    document.getElementById('totalErros').textContent = erros;
    document.getElementById('taxaAcerto').textContent = taxa + '%';
}

// Ordenação da tabela
let ordemCrescente = {};

function ordenarTabela(coluna) {
    const propriedades = ['rodada', 'turma', 'equipe', 'cor', 'tema', 'pergunta', 'resposta', 'acertou'];
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
    
    // Preparar dados da tabela
    const cabecalhos = ['Rodada', 'Turma', 'Equipe', 'Cor', 'Tema', 'Resposta', 'Resultado'];
    const dados = dadosFiltrados.map(item => [
        item.rodada,
        item.turma,
        item.equipe,
        item.cor,
        item.tema,
        item.resposta,
        item.acertou ? 'Acerto' : 'Erro'
    ]);
    
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
    // Preparar dados
    const dados = dadosFiltrados.map(item => ({
        'Rodada': item.rodada,
        'Turma': item.turma,
        'Equipe': item.equipe,
        'Cor': item.cor,
        'Tema': item.tema,
        'Pergunta': item.pergunta,
        'Resposta': item.resposta,
        'Resultado': item.acertou ? 'Acerto' : 'Erro'
    }));
    
    // Criar workbook
    const wb = XLSX.utils.book_new();
    const ws = XLSX.utils.json_to_sheet(dados);
    
    // Ajustar largura das colunas
    const colWidths = [
        { wch: 10 }, // Rodada
        { wch: 15 }, // Turma
        { wch: 20 }, // Equipe
        { wch: 15 }, // Cor
        { wch: 20 }, // Tema
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
        item.equipe.toLowerCase().includes(termo) ||
        item.tema.toLowerCase().includes(termo) ||
        item.pergunta.toLowerCase().includes(termo) ||
        item.resposta.toLowerCase().includes(termo)
    );
    
    atualizarTabela();
    atualizarEstatisticas();
}
