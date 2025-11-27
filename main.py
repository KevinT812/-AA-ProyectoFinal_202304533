"""
Programa principal del proyecto de Análisis de Algoritmos.

Este módulo implementa un menú interactivo para ejecutar los algoritmos
de Prim, Kruskal, Dijkstra y Huffman.
"""

import sys
from src.prim import ejecutar_prim
from src.kruskal import ejecutar_kruskal
from src.dijkstra import ejecutar_dijkstra
from src.huffman import ejecutar_huffman


def mostrar_menu():
    """
    Muestra el menú principal del programa.
    
    Returns:
        None
    
    Complejidad: O(1)
    """
    print("\n" + "="*60)
    print(" " * 10 + "PROYECTO FINAL - ANÁLISIS DE ALGORITMOS")
    print("="*60)
    print("\nMenú Principal:")
    print("  1. Algoritmo de Prim (Árbol de Expansión Mínima)")
    print("  2. Algoritmo de Kruskal (Árbol de Expansión Mínima)")
    print("  3. Algoritmo de Dijkstra (Caminos más cortos)")
    print("  4. Algoritmo de Huffman (Codificación óptima)")
    print("  5. Ejecutar todos los algoritmos")
    print("  6. Salir")
    print("="*60)


def ejecutar_todos():
    """
    Ejecuta todos los algoritmos en secuencia.
    
    Returns:
        None
    
    Complejidad: Suma de complejidades de cada algoritmo.
    """
    print("\n" + "="*60)
    print("EJECUTANDO TODOS LOS ALGORITMOS")
    print("="*60 + "\n")
    
    try:
        ejecutar_prim()
        ejecutar_kruskal()
        ejecutar_dijkstra(nodo_origen='A')  # Usar nodo por defecto
        ejecutar_huffman()
        
        print("\n" + "="*60)
        print("✓ TODOS LOS ALGORITMOS EJECUTADOS EXITOSAMENTE")
        print("="*60 + "\n")
    except Exception as e:
        print(f"\n✗ Error durante la ejecución: {e}")


def main():
    """
    Función principal que maneja el flujo del programa.
    
    Presenta un menú interactivo y ejecuta los algoritmos seleccionados
    por el usuario.
    
    Returns:
        None
    
    Complejidad: O(1) para el manejo del menú, más la complejidad
                 del algoritmo seleccionado.
    """
    while True:
        mostrar_menu()
        
        try:
            opcion = input("\nSeleccione una opción (1-6): ").strip()
            
            if opcion == '1':
                ejecutar_prim()
            
            elif opcion == '2':
                ejecutar_kruskal()
            
            elif opcion == '3':
                ejecutar_dijkstra()
            
            elif opcion == '4':
                ejecutar_huffman()
            
            elif opcion == '5':
                ejecutar_todos()
            
            elif opcion == '6':
                print("\n" + "="*60)
                print("Saliendo del programa...")
                print("¡Hasta pronto!")
                print("="*60 + "\n")
                sys.exit(0)
            
            else:
                print("\n✗ Opción no válida. Por favor, seleccione 1-6.")
        
        except KeyboardInterrupt:
            print("\n\n" + "="*60)
            print("Programa interrumpido por el usuario.")
            print("="*60 + "\n")
            sys.exit(0)
        
        except Exception as e:
            print(f"\n✗ Error inesperado: {e}")
            print("Por favor, intente nuevamente.\n")


if __name__ == "__main__":
    main()