class Processo:
    def __init__(self, pid, chegada, execucao):
        self.pid = pid
        self.chegada = chegada
        self.execucao = execucao
        self.tempo_restante = execucao
        self.tempo_espera = 0
        self.tempo_conclusao = 0
        self.tempo_turnaround = 0 # Tempo efetivo observado (Conclusão - Chegada)

class Escalonador:
    def __init__(self, processos, ttc=0, quantum=0):
        self.processos = processos
        self.ttc = ttc
        self.quantum = quantum

    def _imprimir_resultados(self, ordem_execucao):
        print("\n--- Resultados da Simulação ---")
        print(f"Ordem de Execução: {' -> '.join(ordem_execucao)}")
        
        tempo_total_espera = 0
        print("\nPID\tChegada\tExecução\tConclusão\tTurnaround\tEspera")
        for p in sorted(self.processos, key=lambda x: x.pid):
            p.tempo_turnaround = p.tempo_conclusao - p.chegada
            p.tempo_espera = p.tempo_turnaround - p.execucao
            tempo_total_espera += p.tempo_espera
            print(f"{p.pid}\t{p.chegada}\t{p.execucao}\t\t{p.tempo_conclusao}\t\t{p.tempo_turnaround}\t\t{p.tempo_espera}")
        
        tempo_medio_espera = tempo_total_espera / len(self.processos)
        print(f"\nTempo Médio de Espera: {tempo_medio_espera:.2f}")

    def simular_fcfs(self):
        print("\nIniciando FCFS...")
        fila = sorted(self.processos, key=lambda p: p.chegada)
        tempo_atual = 0
        ordem_execucao = []

        for p in fila:
            if tempo_atual < p.chegada:
                tempo_atual = p.chegada
            if ordem_execucao: # Aplica TTC se não for o primeiro
                tempo_atual += self.ttc
            
            ordem_execucao.append(f"P{p.pid}")
            tempo_atual += p.execucao
            p.tempo_conclusao = tempo_atual

        self._imprimir_resultados(ordem_execucao)

    def simular_sjf_nao_preemptivo(self):
        print("\nIniciando SJF (Não Preemptivo)...")
        processos_restantes = sorted(self.processos, key=lambda p: p.chegada)
        tempo_atual = 0
        ordem_execucao = []
        concluidos = []

        while processos_restantes:
            # Filtra processos que já chegaram
            prontos = [p for p in processos_restantes if p.chegada <= tempo_atual]
            
            if not prontos:
                tempo_atual = processos_restantes[0].chegada
                continue
            
            # Escolhe o de menor tempo de execução
            p_atual = min(prontos, key=lambda p: p.execucao)
            processos_restantes.remove(p_atual)

            if ordem_execucao:
                tempo_atual += self.ttc

            ordem_execucao.append(f"P{p_atual.pid}")
            tempo_atual += p_atual.execucao
            p_atual.tempo_conclusao = tempo_atual
            concluidos.append(p_atual)

        self.processos = concluidos
        self._imprimir_resultados(ordem_execucao)

    def simular_sjf_preemptivo(self):
        print("\nIniciando SJF (Preemptivo / SRTF)...")
        tempo_atual = 0
        completados = 0
        n = len(self.processos)
        ordem_execucao = []
        ultimo_pid = None

        while completados < n:
            prontos = [p for p in self.processos if p.chegada <= tempo_atual and p.tempo_restante > 0]
            
            if not prontos:
                tempo_atual += 1
                continue

            p_atual = min(prontos, key=lambda p: p.tempo_restante)

            if ultimo_pid is not None and ultimo_pid != p_atual.pid:
                tempo_atual += self.ttc
            
            if ultimo_pid != p_atual.pid:
                ordem_execucao.append(f"P{p_atual.pid}")
                ultimo_pid = p_atual.pid

            p_atual.tempo_restante -= 1
            tempo_atual += 1

            if p_atual.tempo_restante == 0:
                completados += 1
                p_atual.tempo_conclusao = tempo_atual

        self._imprimir_resultados(ordem_execucao)

    def simular_round_robin(self):
        print(f"\nIniciando Round Robin (Quantum = {self.quantum})...")
        tempo_atual = 0
        fila_prontos = []
        processos_ordenados = sorted(self.processos, key=lambda p: p.chegada)
        ordem_execucao = []
        indice_chegada = 0
        n = len(self.processos)
        ultimo_pid = None

        while processos_ordenados and indice_chegada < n and processos_ordenados[indice_chegada].chegada <= tempo_atual:
            fila_prontos.append(processos_ordenados[indice_chegada])
            indice_chegada += 1

        if not fila_prontos and indice_chegada < n:
            tempo_atual = processos_ordenados[indice_chegada].chegada
            fila_prontos.append(processos_ordenados[indice_chegada])
            indice_chegada += 1

        while fila_prontos:
            p_atual = fila_prontos.pop(0)

            if ultimo_pid is not None and ultimo_pid != p_atual.pid:
                tempo_atual += self.ttc

            if ultimo_pid != p_atual.pid:
                ordem_execucao.append(f"P{p_atual.pid}")
                ultimo_pid = p_atual.pid

            tempo_executado = min(p_atual.tempo_restante, self.quantum)
            p_atual.tempo_restante -= tempo_executado
            tempo_atual += tempo_executado

            # Verifica novos processos que chegaram durante a execução
            while indice_chegada < n and processos_ordenados[indice_chegada].chegada <= tempo_atual:
                fila_prontos.append(processos_ordenados[indice_chegada])
                indice_chegada += 1

            if p_atual.tempo_restante > 0:
                fila_prontos.append(p_atual)
            else:
                p_atual.tempo_conclusao = tempo_atual

            # Se a fila esvaziou mas ainda há processos a chegar
            if not fila_prontos and indice_chegada < n:
                tempo_atual = processos_ordenados[indice_chegada].chegada
                fila_prontos.append(processos_ordenados[indice_chegada])
                indice_chegada += 1

        self._imprimir_resultados(ordem_execucao)


def criar_processos_padrao():
    return [
        Processo(1, 0, 5),
        Processo(2, 1, 3),
        Processo(3, 2, 8),
        Processo(4, 3, 6)
    ]

def menu_principal():
    while True:
        print("\n" + "="*40)
        print("SIMULADOR DE ESCALONAMENTO DE CPU")
        print("="*40)
        print("1. FCFS (First-Come, First-Served)")
        print("2. SJF (Nao Preemptivo)")
        print("3. SJF (Preemptivo)")
        print("4. Round Robin")
        print("0. Sair do Programa")
        print("="*40)
        
        escolha = input("Escolha qual algoritmo deseja simular (0-4): ")
        
        if escolha == '0':
            print("Encerrando o simulador...")
            break
        if escolha not in ['1', '2', '3', '4']:
            print("Opcao invalida.")
            continue
            
        try:
            ttc_input = input("Informe o TTC (Tempo de Troca de Contexto) [Enter para 0]: ")
            ttc = int(ttc_input) if ttc_input.strip() != "" else 0
        except ValueError:
            ttc = 0

        processos = criar_processos_padrao()
        simulador = Escalonador(processos, ttc=ttc)

        if escolha == '1':
            simulador.simular_fcfs()
        elif escolha == '2':
            simulador.simular_sjf_nao_preemptivo()
        elif escolha == '3':
            simulador.simular_sjf_preemptivo()
        elif escolha == '4':
            try:
                quantum = int(input("Informe o valor do Quantum para o Round Robin: "))
                simulador.quantum = quantum
                simulador.simular_round_robin()
            except ValueError:
                print("Valor de Quantum invalido.")

if __name__ == "__main__":
    menu_principal()