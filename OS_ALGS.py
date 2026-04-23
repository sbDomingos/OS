def criar_processos():
    """
    Função auxiliar para sempre gerar processos 'fresquinhos' (zerados) 
    toda vez que uma nova simulação for escolhida.
    """
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
        print("2. SJF (Não Preemptivo)")
        print("3. SJF (Preemptivo)")
        print("4. Round Robin")
        print("0. Sair do Programa")
        print("="*40)
        
        escolha = input("Escolha qual algoritmo deseja simular (0-4): ")
        
        if escolha == '0':
            print("Encerrando o simulador... Até logo!")
            break
            
        if escolha not in ['1', '2', '3', '4']:
            print("Opção inválida. Tente novamente.")
            continue
            
        # Pega o TTC (Tempo de Troca de Contexto) que vale para todos
        try:
            ttc_input = input("Informe o TTC (Tempo de Troca de Contexto) [Pressione Enter para 0]: ")
            ttc = int(ttc_input) if ttc_input.strip() != "" else 0
        except ValueError:
            print("Valor de TTC inválido. Usando TTC = 0.")
            ttc = 0

        # Cria uma lista nova e limpa de processos
        processos = criar_processos_padrao()
        
        # Instancia o escalonador
        simulador = Escalonador(processos, ttc=ttc)

        # Executa o algoritmo escolhido
        if escolha == '1':
            # simulador.simular_fcfs() # (Você implementará este depois)
            print("\n[Aviso: Algoritmo FCFS ainda não implementado.]")
            
        elif escolha == '2':
            simulador.simular_sjf_nao_preemptivo()
            
        elif escolha == '3':
            # simulador.simular_sjf_preemptivo() # (Você implementará este depois)
            print("\n[Aviso: Algoritmo SJF Preemptivo ainda não implementado.]")
            
        elif escolha == '4':
            # O Round Robin é o único que exige a pergunta extra do Quantum
            try:
                quantum = int(input("Informe o valor do Quantum para o Round Robin: "))
                simulador.quantum = quantum
                # simulador.simular_round_robin() # (Você implementará este depois)
                print("\n[Aviso: Algoritmo Round Robin ainda não implementado.]")
            except ValueError:
                print("Valor de Quantum inválido. Abortando simulação.")

        # Pausa antes de limpar e mostrar o menu de novo
        input("\nPressione [ENTER] para voltar ao menu principal...")

# Ponto de entrada do programa
if __name__ == "__main__":
    menu_principal()
