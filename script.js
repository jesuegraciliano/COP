document.addEventListener('DOMContentLoaded', () => {
    const fluidoSelect = document.getElementById('fluido');
    const tempEvaporacaoInput = document.getElementById('tempEvaporacao');
    const tempCondensacaoInput = document.getElementById('tempCondensacao');
    const calcularBtn = document.getElementById('calcularBtn');
    const copSistemaSpan = document.getElementById('copSistema');
    const copCarnotSpan = document.getElementById('copCarnot');
    const eficienciaSpan = document.getElementById('eficiencia');

    // Dados de entalpia baseados na imagem para as temperaturas fixas de -10°C e 45°C
    const dadosFluido = {
        "R134a": {
            Te_menos10: { hl: 186, hv: 392, h2: 0 }, // Para Tevap = -10°C
            Tc_45:    { hl: 264, hv: 422, h2: 430 }  // Para Tcond = 45°C
        },
        "R410A": {
            Te_menos10: { hl: 43, hv: 276, h2: 0 },   // Para Tevap = -10°C
            Tc_45:    { hl: 133, hv: 281, h2: 320 }  // Para Tcond = 45°C
        }
    };

    calcularBtn.addEventListener('click', () => {
        const fluidoSelecionado = fluidoSelect.value;
        const tempEvaporacao = parseFloat(tempEvaporacaoInput.value);
        const tempCondensacao = parseFloat(tempCondensacaoInput.value);

        // Validação simples
        if (isNaN(tempEvaporacao) || isNaN(tempCondensacao)) {
            alert("Por favor, insira valores numéricos válidos para as temperaturas.");
            return;
        }
        if (tempEvaporacao >= tempCondensacao) {
            alert("A temperatura de evaporação deve ser menor que a temperatura de condensação.");
            return;
        }

        // Seleciona os dados relevantes com base no fluido.
        // NOTA: Esta é uma simulação simples. Para valores variáveis,
        // você precisaria de uma lógica de interpolação ou uma tabela
        // de dados mais completa. Aqui, estamos usando os valores da imagem
        // que parecem corresponder a Tevap -10 e Tcond 45.
        const dadosEvap = dadosFluido[fluidoSelecionado].Te_menos10;
        const dadosCond = dadosFluido[fluidoSelecionado].Tc_45;

        // Assumindo que a entalpia de saída do evaporador (h1) é hv na temperatura de evaporação
        // e a entalpia de saída do condensador (h3) é hl na temperatura de condensação.
        const h1 = dadosEvap.hv;
        const h3 = dadosCond.hl;
        const h2 = dadosCond.h2; // Entalpia h2 dada na tabela

        // Cálculos
        // COP do Sistema: (E4-D5)/(G5-E4) da imagem
        // E4 = hv (Te), D5 = hl (Te)
        // G5 = h2 (Tc), E4 = hv (Te)
        const copSistema = (h1 - h3) / (h2 - h1);

        // COP de Carnot: (I4+273)/(J4-I4) da imagem
        // I4 = Tevap, J4 = Tcond
        const copCarnot = (tempEvaporacao + 273) / (tempCondensacao - tempEvaporacao);

        // Eficiência: 100*(C7/C11) da imagem
        // C7 = COP Sistema, C11 = COP Carnot
        const eficiencia = (copSistema / copCarnot) * 100;

        // Exibir resultados
        copSistemaSpan.textContent = copSistema.toFixed(2);
        copCarnotSpan.textContent = copCarnot.toFixed(2);
        eficienciaSpan.textContent = eficiencia.toFixed(2);
    });

    // Simular um clique inicial para mostrar os valores padrão
    calcularBtn.click();
});
