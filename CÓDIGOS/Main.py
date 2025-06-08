import sys

def menu():
    print("\nEscolha qual módulo deseja executar:")
    print("1 - Estatística Descritiva")
    print("2 - Grafo (Visualização de Consumo)")
    print("3 - Hashing")
    print("4 - Bloom Filter")
    print("5 - Skip List")
    print("6 - Segment Tree")
    print("7 - Árvore Binária (Decision Tree)")
    print("0 - Sair")
    return input("Opção: ")

if __name__ == "__main__":
    while True:
        opcao = menu()
        if opcao == "0":
            print("Saindo.")
            sys.exit(0)
        elif opcao == "1":
            import EstatisticaDescritiva
        elif opcao == "2":
            import Grafo
        elif opcao == "3":
            import Hashing
        elif opcao == "4":
            import CÓDIGOS.BloomFilter as BloomFilter
        elif opcao == "5":
            import SkipList
        elif opcao == "6":
            import SegmentTree
        elif opcao == "7":
            import ArvoreBinaria
        else:
            print("Opção inválida.")

        