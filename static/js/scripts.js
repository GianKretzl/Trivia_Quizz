// Estado do jogo
let jogoAtivo = false;
let perguntaAtual = null;
let equipesSelecionadas = [];
let coresDisponiveis = [];
let respostaSelecionada = null;
let configState = {
    turma: null,
    numEquipes: null,
    cores: []
};

// Funções de seleção para os modais
function selecionarTurma(turma) {
    configState.turma = turma;
    closeModal('turma-modal');
    atualizarProgresso();
    atualizarNivel();
}

function selecionarNumEquipes(num) {
    configState.numEquipes = num;
    configState.cores = []; // Reset cores quando mudar número de equipes
    closeModal('equipes-modal');
    atualizarProgresso();
}

function confirmarCores() {
    if (configState.cores.length === configState.numEquipes) {
        closeModal('cores-modal');
        atualizarProgresso();
    } else {
        alert(`Por favor, selecione ${configState.numEquipes} cores para as equipes.`);
    }
}

// Elementos DOM
const configMenu = document.getElementById('config-menu');
const gameArea = document.getElementById('game-area');
const iniciarJogoBtn = document.getElementById('iniciar-jogo');
const girarRoletaBtn = document.getElementById('girar-roleta');
const roleta = document.getElementById('roleta');
const disciplinaResultado = document.getElementById('disciplina-resultado');
const disciplinaNome = document.getElementById('disciplina-nome');
const perguntaArea = document.getElementById('pergunta-area');
const perguntaTexto = document.getElementById('pergunta-texto');
const opcoesBtns = document.querySelectorAll('.opcao-btn');
const equipeRespostaSelect = document.getElementById('equipe-resposta');
const resultadoArea = document.getElementById('resultado-area');
const resultadoTitulo = document.getElementById('resultado-titulo');
const resultadoTexto = document.getElementById('resultado-texto');
const respostaCorretaTexto = document.getElementById('resposta-correta-texto');
const novaPerguntaBtn = document.getElementById('nova-pergunta');
const resetJogoBtn = document.getElementById('reset-jogo');
const voltarConfigBtn = document.getElementById('voltar-config');
const placar = document.getElementById('placar');

// Novos elementos do menu estilo jogo
const turmaBtn = document.getElementById('turma-btn');
const equipesBtn = document.getElementById('equipes-btn');
const coresBtn = document.getElementById('cores-btn');
const turmaModal = document.getElementById('turma-modal');
const equipesModal = document.getElementById('equipes-modal');
const coresModal = document.getElementById('cores-modal');
const coresContainer = document.getElementById('cores-container');
const confirmarCoresBtn = document.getElementById('confirmar-cores');

// Função para interação com a logo
function playEurekaSound() {
    const logo = document.querySelector('.logo-eureka');
    logo.style.animation = 'logoSpin 1s linear';
    
    // Criar efeito de "EUREKA!" 
    const eurekaText = document.createElement('div');
    eurekaText.textContent = 'EUREKA! 🎉';
    eurekaText.style.cssText = `
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 2rem;
        color: #FFD700;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        animation: eurekaPopup 2s ease-out forwards;
        pointer-events: none;
        z-index: 1000;
    `;
    
    document.body.appendChild(eurekaText);
    
    // Remover o texto após a animação
    setTimeout(() => {
        if (eurekaText.parentNode) {
            eurekaText.parentNode.removeChild(eurekaText);
        }
        logo.style.animation = 'logoFloat 3s ease-in-out infinite';
    }, 2000);
}

// Adicionar CSS para animação do popup
const style = document.createElement('style');
style.textContent = `
    @keyframes eurekaPopup {
        0% {
            opacity: 0;
            transform: translate(-50%, -50%) scale(0);
        }
        50% {
            opacity: 1;
            transform: translate(-50%, -50%) scale(1.2);
        }
        100% {
            opacity: 0;
            transform: translate(-50%, -50%) scale(1) translateY(-50px);
        }
    }
`;
document.head.appendChild(style);

// Funções do novo menu
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
}

function updateButtonState(button, text, enabled = false) {
    // A nova estrutura não usa button-subtitle, então vamos apenas atualizar o estado do botão
    if (button) {
        button.disabled = !enabled;
        
        if (enabled) {
            button.classList.add('configured');
        }
    }
}

function checkAllConfigured() {
    const allConfigured = configState.turma && 
                         configState.numEquipes && 
                         configState.cores.length === configState.numEquipes;
    
    console.log('Verificando configuração:', {
        turma: configState.turma,
        numEquipes: configState.numEquipes,
        cores: configState.cores.length,
        necessarias: configState.numEquipes,
        completo: allConfigured
    });
    
    iniciarJogoBtn.disabled = !allConfigured;
    return allConfigured;
}

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    carregarCoresDisponiveis();
    configurarEventListeners();
});

// Configurar event listeners
function configurarEventListeners() {
    // Botões do menu principal - verificar se existem
    if (turmaBtn) {
        turmaBtn.addEventListener('click', () => openModal('turma-modal'));
    }
    
    if (equipesBtn) {
        equipesBtn.addEventListener('click', () => {
            if (configState.turma) {
                openModal('equipes-modal');
            } else {
                alert('Por favor, selecione uma turma primeiro!');
            }
        });
    }
    
    if (coresBtn) {
        coresBtn.addEventListener('click', () => {
            if (configState.numEquipes && configState.numEquipes > 0) {
                setupCoresModal();
                openModal('cores-modal');
                console.log('Botão de cores clicado, abrindo modal...');
            } else {
                // Mostrar mensagem de aviso se as equipes não foram definidas
                alert('⚠️ Primeiro você precisa definir o número de equipes!');
            }
        });
    }
    
    // Botões de fechar modal
    document.querySelectorAll('.close-modal').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const modalId = e.target.getAttribute('data-modal');
            closeModal(modalId);
        });
    });
    
    // Fechar modal clicando fora
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeModal(modal.id);
            }
        });
    });
    
    // Event listeners para seleção de turma (usando onclick no HTML)
    
    // Event listeners para seleção de equipes (usando onclick no HTML)
    
    // Configuração do jogo
    iniciarJogoBtn.addEventListener('click', iniciarJogo);
    
    // Confirmar cores
    if (confirmarCoresBtn) {
        confirmarCoresBtn.addEventListener('click', () => {
            confirmarCores();
            checkAllConfigured();
        });
    }
    
    // Jogo
    girarRoletaBtn.addEventListener('click', girarRoleta);
    opcoesBtns.forEach(btn => {
        btn.addEventListener('click', selecionarResposta);
    });
}

// Configurar modal de cores
function setupCoresModal() {
    console.log('Configurando modal de cores...');
    console.log('Cores disponíveis:', coresDisponiveis);
    console.log('Número de equipes:', configState.numEquipes);
    
    // Se não há número de equipes definido, usar um padrão para teste
    if (!configState.numEquipes) {
        console.warn('Número de equipes não definido, usando padrão de 3 equipes');
        configState.numEquipes = 3;
    }
    
    if (!coresDisponiveis || coresDisponiveis.length === 0) {
        console.error('Cores não carregadas ainda, carregando agora...');
        // Carregar cores diretamente aqui se necessário
        coresDisponiveis = [
            { nome: 'VERDE', hex: '#00FF00' },
            { nome: 'AMARELO', hex: '#FFFF00' },
            { nome: 'VERMELHO', hex: '#FF0000' },
            { nome: 'AZUL', hex: '#0066FF' },
            { nome: 'LARANJA', hex: '#FFA500' },
            { nome: 'ROXO', hex: '#8A2BE2' },
            { nome: 'AZUL CLARO', hex: '#87CEEB' },
            { nome: 'PRETO', hex: '#000000' },
            { nome: 'BRANCO', hex: '#FFFFFF' },
            { nome: 'ROSA BEBÊ', hex: '#FFB6C1' }
        ];
    }
    
    // Resetar estado das cores
    configState.cores = [];
    confirmarCoresBtn.disabled = true;
    
    // Atualizar instruções iniciais
    atualizarInstrucoesCores();
    
    // Limpar container
    coresContainer.innerHTML = '';
    
    console.log('Criando elementos de cores...');
    
    // Mostrar todas as cores disponíveis
    coresDisponiveis.forEach((cor, index) => {
        console.log(`Criando elemento para cor: ${cor.nome} (${cor.hex})`);
        
        const corDiv = document.createElement('div');
        corDiv.className = 'cor-option';
        corDiv.dataset.corIndex = index;
        corDiv.innerHTML = `
            <div class="cor-circle" style="background-color: ${cor.hex}">
                <div class="check-mark" style="display: none;">✓</div>
            </div>
            <span>${cor.nome}</span>
        `;
        corDiv.addEventListener('click', () => selecionarCor(corDiv, cor, index));
        coresContainer.appendChild(corDiv);
    });
    
    console.log('Modal de cores configurado com sucesso. Elementos criados:', coresContainer.children.length);
}

function selecionarCor(elemento, cor, index) {
    console.log('Selecionando cor:', cor);
    
    // Remover seleção anterior se existir
    const jasSelecionado = elemento.classList.contains('selected');
    const checkMark = elemento.querySelector('.check-mark');
    
    if (jasSelecionado) {
        // Desselecionar
        elemento.classList.remove('selected');
        if (checkMark) checkMark.style.display = 'none';
        configState.cores = configState.cores.filter(c => c.nome !== cor.nome);
        console.log('Cor desselecionada. Cores atuais:', configState.cores);
    } else {
        // Verificar se já temos o número máximo de cores
        if (configState.cores.length >= configState.numEquipes) {
            console.log('Já temos o número máximo de cores');
            alert(`Você já selecionou ${configState.numEquipes} cores. Desselecione uma cor primeiro se quiser trocar.`);
            return; // Não permitir mais seleções
        }
        
        // Selecionar
        elemento.classList.add('selected');
        if (checkMark) checkMark.style.display = 'flex';
        configState.cores.push(cor);
        console.log('Cor selecionada. Cores atuais:', configState.cores);
    }
    
    // Atualizar o texto das instruções
    atualizarInstrucoesCores();
    
    // Verificar se todas as cores necessárias foram selecionadas
    if (configState.cores.length === configState.numEquipes) {
        confirmarCoresBtn.disabled = false;
        console.log('Todas as cores selecionadas!');
    } else {
        confirmarCoresBtn.disabled = true;
        console.log(`Ainda faltam ${configState.numEquipes - configState.cores.length} cores`);
    }
}

function atualizarInstrucoesCores() {
    const coresNeeded = document.getElementById('cores-needed');
    const instruction = document.getElementById('cores-instructions');
    
    console.log('Atualizando instruções de cores:', {
        coresNeeded: coresNeeded,
        instruction: instruction,
        numEquipes: configState.numEquipes,
        coresSelecionadas: configState.cores.length
    });
    
    if (coresNeeded && instruction) {
        const selecionadas = configState.cores.length;
        const necessarias = configState.numEquipes;
        
        if (selecionadas === 0) {
            instruction.innerHTML = `Selecione <span id="cores-needed">${necessarias}</span> cores para as equipes (clique para selecionar/desselecionar):`;
        } else if (selecionadas < necessarias) {
            instruction.innerHTML = `Selecionadas: ${selecionadas}/${necessarias} - Selecione mais <span id="cores-needed">${necessarias - selecionadas}</span> cores:`;
        } else {
            instruction.innerHTML = `✅ Todas as <span id="cores-needed">${necessarias}</span> cores selecionadas!`;
        }
    } else {
        console.error('Elementos não encontrados:', { coresNeeded, instruction });
    }
}

// Carregar cores disponíveis
async function carregarCoresDisponiveis() {
    try {
        console.log('Carregando cores disponíveis...');
        
        // Definir cores específicas solicitadas
        coresDisponiveis = [
            { nome: 'VERDE', hex: '#00FF00' },
            { nome: 'AMARELO', hex: '#FFFF00' },
            { nome: 'VERMELHO', hex: '#FF0000' },
            { nome: 'AZUL', hex: '#0066FF' },
            { nome: 'LARANJA', hex: '#FFA500' },
            { nome: 'ROXO', hex: '#8A2BE2' },
            { nome: 'AZUL CLARO', hex: '#87CEEB' },
            { nome: 'PRETO', hex: '#000000' },
            { nome: 'BRANCO', hex: '#FFFFFF' },
            { nome: 'ROSA BEBÊ', hex: '#FFB6C1' }
        ];
        
        console.log('Cores definidas com sucesso:', coresDisponiveis);
        
        // Tentar carregar cores da API se disponível
        try {
            const response = await fetch('/api/cores_disponiveis');
            if (response.ok) {
                const data = await response.json();
                if (data.cores && Array.isArray(data.cores) && data.cores.length > 0) {
                    console.log('Cores da API também carregadas:', data.cores);
                    // Manter as cores definidas acima como prioritárias
                }
            }
        } catch (apiError) {
            console.log('API de cores não disponível, usando cores predefinidas');
        }
        
    } catch (error) {
        console.error('Erro ao carregar cores:', error);
        // Garantir que sempre temos as cores mesmo em caso de erro
        coresDisponiveis = [
            { nome: 'VERDE', hex: '#00FF00' },
            { nome: 'AMARELO', hex: '#FFFF00' },
            { nome: 'VERMELHO', hex: '#FF0000' },
            { nome: 'AZUL', hex: '#0066FF' },
            { nome: 'LARANJA', hex: '#FFA500' },
            { nome: 'ROXO', hex: '#8A2BE2' },
            { nome: 'AZUL CLARO', hex: '#87CEEB' },
            { nome: 'PRETO', hex: '#000000' },
            { nome: 'BRANCO', hex: '#FFFFFF' },
            { nome: 'ROSA BEBÊ', hex: '#FFB6C1' }
        ];
        console.log('Usando cores padrão devido ao erro:', coresDisponiveis);
    }
}

// Mostrar seleção de cores das equipes
function mostrarSelecaoCores() {
    const numEquipes = parseInt(numEquipesSelect.value);
    
    if (numEquipes) {
        coresSection.style.display = 'block';
        coresContainer.innerHTML = '';
        
        coresDisponiveis.forEach(cor => {
            const corOption = document.createElement('div');
            corOption.className = 'cor-option';
            corOption.dataset.cor = cor;
            
            const corCircle = document.createElement('div');
            corCircle.className = 'cor-circle';
            corCircle.style.backgroundColor = getCssColor(cor);
            
            const corLabel = document.createElement('span');
            corLabel.textContent = cor;
            
            corOption.appendChild(corCircle);
            corOption.appendChild(corLabel);
            
            corOption.addEventListener('click', () => selecionarCor(corOption, cor));
            
            coresContainer.appendChild(corOption);
        });
        
        validarConfiguracao();
    } else {
        coresSection.style.display = 'none';
    }
}

// Validar configuração do jogo
function validarConfiguracao() {
    const turma = turmaSelect.value;
    const numEquipes = parseInt(numEquipesSelect.value);
    const coresSelecionadas = document.querySelectorAll('.cor-option.selected');
    
    const configuracaoValida = turma && numEquipes && coresSelecionadas.length === numEquipes;
    
    iniciarJogoBtn.disabled = !configuracaoValida;
}

// Iniciar jogo
async function iniciarJogo() {
    const turma = configState.turma;
    const numEquipes = configState.numEquipes;
    const coresSelecionadas = configState.cores.map(cor => cor.nome);
    
    try {
        const response = await fetch('/api/configurar_jogo', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                turma: turma,
                num_equipes: numEquipes,
                cores_equipes: coresSelecionadas
            })
        });
        
        const data = await response.json();
        
        if (data.sucesso) {
            // Redireciona para a rota da roleta
            window.location.href = '/roleta';
        } else {
            alert('Erro ao configurar o jogo: ' + data.erro);
        }
    } catch (error) {
        console.error('Erro ao iniciar jogo:', error);
        alert('Erro ao iniciar o jogo');
    }
}

// Mostrar área do jogo
function mostrarAreaJogo() {
    configMenu.style.display = 'none';
    gameArea.style.display = 'block';
}

// Girar roleta
async function girarRoleta() {
    if (!jogoAtivo) return;
    
    // Gerar rotação aleatória (entre 1800 e 3600 graus para múltiplas voltas)
    const rotacaoBase = 1800;
    const rotacaoExtra = Math.random() * 1800;
    const rotacaoTotal = rotacaoBase + rotacaoExtra;
    
    // Calcular qual disciplina será sorteada baseada na rotação final
    const anguloFinal = (rotacaoTotal % 360);
    const disciplinaSorteada = determinarDisciplinaPorAngulo(anguloFinal);
    
    // Animação da roleta
    roleta.style.transform = `rotate(${rotacaoTotal}deg)`;
    girarRoletaBtn.disabled = true;
    
    try {
        // Fazer requisição para o backend
        const response = await fetch('/api/sortear_disciplina');
        const data = await response.json();
        
        if (data.erro) {
            alert('Erro: ' + data.erro);
            resetRoleta();
            return;
        }
        
        perguntaAtual = data;
        
        // Aguardar animação (3 segundos)
        setTimeout(() => {
            mostrarDisciplinaSorteada(data.disciplina);
            mostrarPergunta(data);
            girarRoletaBtn.disabled = false;
        }, 3000);
        
    } catch (error) {
        console.error('Erro ao sortear disciplina:', error);
        resetRoleta();
    }
}

// Determinar disciplina baseada no ângulo final da roleta
function determinarDisciplinaPorAngulo(angulo) {
    // Ajustar ângulo para que 0° seja o topo (onde está o ponteiro)
    const anguloAjustado = (angulo + 180) % 360;
    
    // Definir os setores da roleta (cada setor tem aproximadamente 51.43°)
    const setores = [
        { inicio: 0, fim: 51.4, disciplina: 'educacao_fisica' },
        { inicio: 51.4, fim: 102.8, disciplina: 'historia' },
        { inicio: 102.8, fim: 154.2, disciplina: 'matematica' },
        { inicio: 154.2, fim: 205.6, disciplina: 'ciencias' },
        { inicio: 205.6, fim: 257, disciplina: 'geografia' },
        { inicio: 257, fim: 308.4, disciplina: 'portugues' },
        { inicio: 308.4, fim: 360, disciplina: 'lingua_inglesa' }
    ];
    
    // Encontrar em qual setor o ângulo se encontra
    for (const setor of setores) {
        if (anguloAjustado >= setor.inicio && anguloAjustado < setor.fim) {
            return setor.disciplina;
        }
    }
    
    // Fallback para educação física
    return 'educacao_fisica';
}

// Reset da roleta
function resetRoleta() {
    roleta.style.transform = 'rotate(0deg)';
    girarRoletaBtn.disabled = false;
}

// Mostrar disciplina sorteada
function mostrarDisciplinaSorteada(disciplina) {
    disciplinaNome.textContent = `🎯 ${disciplina}`;
    disciplinaResultado.style.display = 'block';
}

// Mostrar pergunta
function mostrarPergunta(dados) {
    perguntaTexto.textContent = dados.pergunta;
    
    // Preencher opções
    opcoesBtns.forEach((btn, index) => {
        if (index < dados.opcoes.length) {
            btn.textContent = `${String.fromCharCode(65 + index)}) ${dados.opcoes[index]}`;
            btn.style.display = 'block';
            btn.className = 'opcao-btn'; // Reset classes
        } else {
            btn.style.display = 'none';
        }
    });
    
    // Reset seleção
    respostaSelecionada = null;
    equipeRespostaSelect.value = '';
    
    // Mostrar área da pergunta
    perguntaArea.style.display = 'block';
    resultadoArea.style.display = 'none';
}

// Selecionar resposta
function selecionarResposta(event) {
    const opcao = parseInt(event.target.dataset.opcao);
    respostaSelecionada = opcao;
    
    // Visual feedback
    opcoesBtns.forEach(btn => btn.classList.remove('selecionada'));
    event.target.classList.add('selecionada');
    
    // Verificar se pode enviar resposta
    const equipeId = equipeRespostaSelect.value;
    if (equipeId) {
        enviarResposta(equipeId, opcao);
    }
}

// Evento de mudança na seleção de equipe
equipeRespostaSelect.addEventListener('change', function() {
    if (respostaSelecionada !== null && this.value) {
        enviarResposta(this.value, respostaSelecionada);
    }
});

// Enviar resposta
async function enviarResposta(equipeId, resposta) {
    try {
        const response = await fetch('/api/responder', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                equipe_id: equipeId,
                resposta: resposta
            })
        });
        
        const data = await response.json();
        
        if (data.erro) {
            alert('Erro: ' + data.erro);
            return;
        }
        
        mostrarResultado(data);
        atualizarPlacar();
        
    } catch (error) {
        console.error('Erro ao enviar resposta:', error);
    }
}

// Mostrar resultado
function mostrarResultado(dados) {
    const resultadoCard = document.querySelector('.resultado-card');
    
    if (dados.acertou) {
        resultadoTitulo.textContent = '🎉 Parabéns! Resposta Correta!';
        resultadoTexto.textContent = 'A equipe ganhou 10 pontos!';
        resultadoCard.className = 'resultado-card acertou';
    } else {
        resultadoTitulo.textContent = '❌ Resposta Incorreta';
        resultadoTexto.textContent = 'Não foi dessa vez...';
        resultadoCard.className = 'resultado-card errou';
    }
    
    respostaCorretaTexto.textContent = `Resposta correta: ${dados.opcao_correta}`;
    
    // Destacar resposta correta
    opcoesBtns.forEach((btn, index) => {
        btn.classList.remove('selecionada');
        if (index === dados.resposta_correta) {
            btn.classList.add('correta');
        } else if (index === respostaSelecionada && !dados.acertou) {
            btn.classList.add('incorreta');
        }
    });
    
    perguntaArea.style.display = 'none';
    resultadoArea.style.display = 'block';
}

// Atualizar placar
function atualizarPlacar() {
    placar.innerHTML = '';
    
    equipesSelecionadas.forEach(equipe => {
        const equipeDiv = document.createElement('div');
        equipeDiv.className = `equipe-placar cor-${equipe.cor.toLowerCase()}`;
        
        const nome = document.createElement('span');
        nome.className = 'equipe-nome';
        nome.textContent = equipe.nome;
        
        const pontos = document.createElement('span');
        pontos.className = 'equipe-pontos';
        pontos.textContent = equipe.pontos;
        
        equipeDiv.appendChild(nome);
        equipeDiv.appendChild(pontos);
        
        placar.appendChild(equipeDiv);
    });
}

// Preencher select de equipes
function preencherSelectEquipes() {
    equipeRespostaSelect.innerHTML = '<option value="">Selecione a equipe...</option>';
    
    equipesSelecionadas.forEach(equipe => {
        const option = document.createElement('option');
        option.value = equipe.id;
        option.textContent = equipe.nome;
        equipeRespostaSelect.appendChild(option);
    });
}

// Próxima pergunta
function proximaPergunta() {
    disciplinaResultado.style.display = 'none';
    perguntaArea.style.display = 'none';
    resultadoArea.style.display = 'none';
    perguntaAtual = null;
    
    // Reset visual das opções
    opcoesBtns.forEach(btn => {
        btn.className = 'opcao-btn';
    });
    
    // Reset da roleta para posição inicial
    resetRoleta();
}

// Reset da roleta
function resetRoleta() {
    roleta.style.transform = 'rotate(0deg)';
    girarRoletaBtn.disabled = false;
}

// Encerrar jogo
async function encerrarJogo() {
    if (confirm('Tem certeza que deseja encerrar o jogo?')) {
        try {
            await fetch('/api/reset_jogo', { method: 'POST' });
            voltarParaConfiguracao();
        } catch (error) {
            console.error('Erro ao resetar jogo:', error);
        }
    }
}

// Voltar para configuração
function voltarParaConfiguracao() {
    jogoAtivo = false;
    perguntaAtual = null;
    equipesSelecionadas = [];
    
    // Reset interface
    gameArea.style.display = 'none';
    configMenu.style.display = 'block';
    
    // Reset formulário
    turmaSelect.value = '';
    numEquipesSelect.value = '';
    coresSection.style.display = 'none';
    iniciarJogoBtn.disabled = true;
    
    // Reset áreas do jogo
    disciplinaResultado.style.display = 'none';
    perguntaArea.style.display = 'none';
    resultadoArea.style.display = 'none';
    
    // Reset da roleta
    resetRoleta();
}

// Função auxiliar para obter cor CSS
function getCssColor(corNome) {
    const cores = {
        'Azul': '#007bff',
        'Vermelho': '#dc3545',
        'Verde': '#28a745',
        'Amarelo': '#ffc107',
        'Roxo': '#6f42c1',
        'Laranja': '#fd7e14',
        'Rosa': '#e83e8c',
        'Marrom': '#795548',
        'Preto': '#343a40',
        'Branco': '#f8f9fa',
        'Cinza': '#6c757d',
        'Turquesa': '#20c997'
    };
    
    return cores[corNome] || '#333';
}

// ===== FUNÇÕES PARA A INTERFACE APRIMORADA =====

// Atualizar indicadores de progresso
function atualizarProgresso() {
    const steps = document.querySelectorAll('.step');
    const progressBar = document.getElementById('setup-progress');
    let completedSteps = 0;
    
    // Reset todos os steps
    steps.forEach(step => {
        step.classList.remove('active', 'completed');
    });
    
    // Verificar e atualizar cada step
    if (configState.turma) {
        steps[0].classList.add('completed');
        completedSteps++;
        
        if (configState.numEquipes) {
            steps[1].classList.add('completed');
            completedSteps++;
            
            if (configState.cores.length > 0) {
                steps[2].classList.add('completed');
                completedSteps++;
            } else {
                steps[2].classList.add('active');
            }
        } else {
            steps[1].classList.add('active');
        }
    } else {
        steps[0].classList.add('active');
    }
    
    // Atualizar barra de progresso
    const progressPercent = (completedSteps / 3) * 100;
    if (progressBar) {
        progressBar.style.width = progressPercent + '%';
    }
    
    // Atualizar texto de progresso no header
    const progressText = document.getElementById('progress-text');
    if (progressText) {
        progressText.textContent = Math.round(progressPercent) + '% Completo';
    }
    
    // Atualizar cards
    atualizarStatusCards();
}

// Atualizar status dos cards
function atualizarStatusCards() {
    // Card Turma
    const turmaCard = document.getElementById('turma-card');
    const turmaStatus = document.getElementById('turma-status');
    const turmaSelection = document.getElementById('turma-selection');
    
    if (configState.turma) {
        turmaCard.classList.remove('disabled');
        turmaStatus.innerHTML = '<span class="status-dot"></span><span class="status-text">Concluído</span>';
        turmaSelection.textContent = formatarNomeTurma(configState.turma);
        turmaStatus.querySelector('.status-dot').style.background = '#4CAF50';
    }
    
    // Card Equipes
    const equipesCard = document.getElementById('equipes-card');
    const equipesStatus = document.getElementById('equipes-status');
    const equipesSelection = document.getElementById('equipes-selection');
    
    if (configState.turma) {
        equipesCard.classList.remove('disabled');
        document.getElementById('equipes-btn').disabled = false;
        
        if (configState.numEquipes) {
            equipesStatus.innerHTML = '<span class="status-dot"></span><span class="status-text">Concluído</span>';
            equipesSelection.textContent = `${configState.numEquipes} equipes`;
            equipesStatus.querySelector('.status-dot').style.background = '#4CAF50';
        } else {
            equipesStatus.innerHTML = '<span class="status-dot"></span><span class="status-text">Pendente</span>';
        }
    }
    
    // Card Cores
    const coresCard = document.getElementById('cores-card');
    const coresStatus = document.getElementById('cores-status');
    const coresSelection = document.getElementById('cores-selection');
    
    if (configState.numEquipes) {
        coresCard.classList.remove('disabled');
        document.getElementById('cores-btn').disabled = false;
        
        if (configState.cores.length > 0) {
            coresStatus.innerHTML = '<span class="status-dot"></span><span class="status-text">Concluído</span>';
            coresSelection.textContent = `${configState.cores.length} cores selecionadas`;
            coresStatus.querySelector('.status-dot').style.background = '#4CAF50';
        } else {
            coresStatus.innerHTML = '<span class="status-dot"></span><span class="status-text">Pendente</span>';
        }
    }
}

// Formatar nome da turma para exibição
function formatarNomeTurma(turma) {
    const nomes = {
        '6_ano': '6º Ano',
        '7_ano': '7º Ano', 
        '8_ano': '8º Ano',
        '9_ano': '9º Ano',
        'ensino_medio': 'Ensino Médio'
    };
    return nomes[turma] || turma;
}

// Atualizar nível baseado na turma
function atualizarNivel() {
    const levelElement = document.getElementById('current-level');
    if (!levelElement) return;
    
    const niveis = {
        '6_ano': 'Explorador',
        '7_ano': 'Aventureiro', 
        '8_ano': 'Conhecedor',
        '9_ano': 'Especialista',
        'ensino_medio': 'Mestre'
    };
    
    levelElement.textContent = niveis[configState.turma] || 'Iniciante';
}

// Garantir que as funções estejam disponíveis globalmente
window.selecionarTurma = selecionarTurma;
window.selecionarNumEquipes = selecionarNumEquipes;
window.confirmarCores = confirmarCores;

// Inicializar interface aprimorada
document.addEventListener('DOMContentLoaded', function() {
    // Aguardar um pouco para garantir que outras inicializações ocorreram
    setTimeout(() => {
        atualizarProgresso();
        atualizarNivel();
    }, 100);
});
