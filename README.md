1. Arquitetura do Sistema:
O simulador foi estruturado sob o paradigma de Orientação a Objetos. A classe Processo atua como um DTO (Data Transfer Object) estendido, armazenando metadados de entrada e estados mutáveis durante a simulação (como tempo_restante). A classe Escalonador centraliza a lógica de negócios, isolando as políticas de despacho.

2. Mecânica do Tempo de Troca de Contexto (TTC):
O TTC foi implementado de forma rigorosa: ele só é adicionado ao relógio global da CPU (tempo_atual) quando há uma alteração efetiva no ponteiro do processo em execução (quando ultimo_pid != p_atual.pid). Isso garante que preempções falsas ou loops contínuos no mesmo processo não sofram penalidade de overhead.

3. Métricas Calculadas:

    Tempo de Conclusão (Completion Time): Timestamp exato em que tempo_restante atinge 0.

    Turnaround (Tempo Efetivo/Vida): Calculado no fechamento através da fórmula: Turnaround=Conclusao−Chegada. Representa o tempo total observado, absorvendo implicitamente os atrasos de fila e overhead de TTC.

    Tempo de Espera (Waiting Time): Calculado rigorosamente como Espera=Turnaround−ExecucaoOriginal. Esta é a métrica mais robusta pois independe do algoritmo rastrear cada micropausa na fila.

4. Comportamento Específico dos Algoritmos:

    FCFS: Filas FIFO estritas. Ausência de starvation, mas suscetível ao Efeito Comboio.

    SJF (NP): Avaliação de jobs na fila de prontos (Ready Queue). Quando a CPU ociosa escolhe um processo, ele roda até o fim de seu Burst.

    SJF Preemptivo (SRTF): Simulação baseada em tick de CPU (avanços de 1 u.t.). A cada ciclo, avalia se a chegada de um novo processo com Burst menor do que o residual do processo atual exige a interrupção (disparando o TTC).

    Round Robin: Simulação baseada em time slice. Um timer avança até o limite do quantum ou até o fim da execução do processo, o que for menor. Inserções na fila de prontos respeitam a cronologia de chegada para evitar race conditions no escalonamento.