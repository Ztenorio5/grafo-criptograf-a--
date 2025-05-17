import networkx as nx
import matplotlib.pyplot as plt
import random
from networkx import density

def generar_grafo_expansor(num_nodos=5, grado=2):
    """Genera un grafo dirigido aleatorio k-out (mejor expansor que el anterior)."""
    grado = min(grado, num_nodos - 1)  # evita errores si grado >= num_nodos
    G = nx.random_k_out_graph(num_nodos, grado, alpha=0.8, self_loops=False)
    G = nx.DiGraph(G)  # Convierte a grafo dirigido explícitamente

    # Etiquetas aleatorias '0' o '1'
    for u, v in G.edges():
        G[u][v]['label'] = random.choice(['0', '1'])

    # Renombrar nodos como N0, N1, ...
    mapping = {n: f"{n}" for n in G.nodes()}
    G = nx.relabel_nodes(G, mapping)
    return G

def generar_clave_desde_grafo(G, longitud):
    nodos = list(G.nodes)
    actual = random.choice(nodos)
    clave = []
    visitados = set()

    while len(clave) < longitud:
        sucesores = list(G.successors(actual))
        if not sucesores:
            actual = random.choice(nodos)
            continue
        siguiente = random.choice(sucesores)
        etiqueta = G[actual][siguiente]['label']
        clave.append(int(etiqueta))
        visitados.add(actual)
        actual = siguiente

    if len(visitados) < len(G.nodes) // 2:
        print("⚠️ Advertencia: el recorrido visitó pocos nodos. El grafo podría no expandir bien.")
    return clave

def dibujar_grafo(G, mensaje):
    pos = nx.circular_layout(G)
    labels = nx.get_edge_attributes(G, 'label')

    plt.figure(figsize=(12, 12))
    nx.draw_networkx_nodes(G, pos, node_color='#FFA500', edgecolors='black', node_size=1150, linewidths=1.7)
    nx.draw_networkx_labels(G, pos, font_size=18, font_color='white', font_family='serif')
    nx.draw_networkx_edges(G, pos, arrows=True, arrowstyle='-|>', connectionstyle='arc3,rad=0.8',
                           edge_color='#800080', width=2)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color='darkred',
                                 font_size=12, font_family='serif', label_pos=0.6)
    plt.title(f"Grafo expansor generado para: “{mensaje}”", fontsize=18,
              fontweight='bold', fontfamily='serif', color='#333333')
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def texto_a_bits(texto):
    return [int(b) for c in texto for b in format(ord(c), '08b')]

def bits_a_texto(bits):
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) == 8:
            chars.append(chr(int("".join(map(str, byte)), 2)))
    return ''.join(chars)

def xor_bits(mensaje, clave):
    return [(m ^ k) for m, k in zip(mensaje, clave)]

def cifrar_con_grafo(mensaje, G):
    print(f"\n📨 Texto original: {mensaje}")
    bits = texto_a_bits(mensaje)
    print(f"🔢 Bits del mensaje: {''.join(map(str, bits))}")

    clave = generar_clave_desde_grafo(G, len(bits))
    print(f"🔑 Clave generada desde el grafo: {''.join(map(str, clave))}")

    cifrado = xor_bits(bits, clave)
    print(f"🔒 Bits cifrados: {''.join(map(str, cifrado))}")

    descifrado = xor_bits(cifrado, clave)
    texto_descifrado = bits_a_texto(descifrado)
    print(f"📬 Texto descifrado: {texto_descifrado}")

def main():
    mensaje = input("Escribe tu mensaje: ")
    num_nodos = max(6, len(mensaje) // 2)
    grado = 3

    if grado >= num_nodos:
        grado = max(1, num_nodos - 1)

    G = generar_grafo_expansor(num_nodos=num_nodos, grado=grado)

    print(f"\n📊 Densidad del grafo: {density(G):.2f}")
    cifrar_con_grafo(mensaje, G)
    dibujar_grafo(G, mensaje)

if __name__ == "__main__":
    main()
