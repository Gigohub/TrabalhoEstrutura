import sys
import os
def menu():
     
    # Nome da pasta
    nome_pasta = "IMAGENS"

    # Verifica se a pasta existe
    if not os.path.exists(nome_pasta):
        os.makedirs(nome_pasta)
        print(f'Pasta "{nome_pasta}" criada.')
    else:
        print(f'A pasta "{nome_pasta}" já existe.')
    print(f'A pasta "{nome_pasta}" já existe.')
    print("\nEscolha qual módulo deseja executar:")
    print("\nEstruturas:")
    print("1 - Grafo (Visualização de Consumo)")
    print("2 - Hashing")
    print("3 - Bloom Filter")
    print("4 - Skip List")
    print("5 - Segment Tree")
    print("6 - Árvore Binária (Decision Tree)")
    print("Operações Adicionais:")
    print("7 - Estatistica Descritiva")
    print("8 - Simulação com Novos Dados")
    print("9 - Filtragem e Ordenação dos dados")
    print("Bench Marks:")
    print("10 - Bench Mark Árvore Binária")
    print("11 - Bench Mark Bloom Filter")
    print("12 - Bench Mark Grafo")
    print("13 - Bench Mark Hashing")
    print("14 - Bench Mark Segment Tree")
    print("15 - Bench Mark Skip List")
    print("Optimização do Hashing (Cuckoo Hashing)")
    print("16 - Cuckoo Hashing")
    print("Restrições:")
    print("17 - Restrição Árvpre Binária")
    print("18 - Restrição Bloom Filter")
    print("19 - Restrição Grafos")
    print("20 - Restrição Hashing")
    print("21 - Restrição Segment Tree")
    print("22 - Restrição Skip Tree")
    print("Aprendizado não supervisionado (Clusterização)")
    print("23 - Clusterização")
    print("0 - Sair")
    return input("Opção: ")

if __name__ == "__main__":
    while True:
        opcao = menu()
        if opcao == "0":
            print("Saindo.")
            sys.exit(0)
        elif opcao == "1":
            import Grafo
        elif opcao == "2":
            import Hashing
        elif opcao == "3":
            import BloomFilter
        elif opcao == "4":
            import SkipList
        elif opcao == "5":
            import SegmentTree
        elif opcao == "6":
            import ArvoreBinaria
        elif opcao == "7":
            import EstatisticaDescritiva
        elif opcao == "8":
            import SimulaçãoComNovosDados
        elif opcao == "9":
            import FiltragemOrdenaçãoDeDados
        elif opcao == "10":
            from BenchMark_ArvoreBinaria import benchmark_arvore_binaria
            benchmark_arvore_binaria()
        elif opcao == "11":
            from BenchMark_BloomFilter import benchmark_bloom_filter
            benchmark_bloom_filter()
        elif opcao == "12":
            from BenchMark_Grafos import benchmark_grafo
            benchmark_grafo()
        elif opcao == "13":
            from BenchMark_Hashing import benchmark_hashing
            benchmark_hashing()
        elif opcao == "14":
            from BenchMark_SegmentTree import benchmark_segment_tree
            benchmark_segment_tree()
        elif opcao == "15":
            from BenchMark_SkipList import benchmark_skiplist
            benchmark_skiplist()
        elif opcao == "16":
            import CuckooHashing
        elif opcao == "17":
            import RestriçãoArvoreBinaria 
        elif opcao == "18":
            import RestriçãoBlomFilter
        elif opcao == "19":
            import RestriçãoGrafos
        elif opcao == "20":
            import RestriçãoHashing
        elif opcao == "21":
            import RestriçãoSegmentTree
        elif opcao == "22":
            import RestriçãoSkipList
        elif opcao == "23":
            import AprendizadoNãoSupervisionado
        else:
            print("Opção inválida.")
        