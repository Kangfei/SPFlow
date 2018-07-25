'''
Created on March 29, 2018

@author: Alejandro Molina
'''
from networkx.drawing.nx_agraph import graphviz_layout


def get_networkx_obj(spn):
    import networkx as nx
    from spn.structure.Base import Sum, Product, Leaf, get_nodes_by_type
    import numpy as np

    all_nodes = get_nodes_by_type(spn)

    g = nx.Graph()

    labels = {}
    for n in all_nodes:

        if isinstance(n, Sum):
            label = "+"
        elif isinstance(n, Product):
            label = "x"
        else:
            label = "V" + str(n.scope[0])
        g.add_node(n.id)
        labels[n.id] = label

        if isinstance(n, Leaf):
            continue
        for i, c in enumerate(n.children):
            edge_label = ""
            if isinstance(n, Sum):
                edge_label = np.round(n.weights[i], 2)
            g.add_edge(c.id, n.id, weight=edge_label)

    return g, labels


def plot_spn(spn, fname="plot.pdf"):
    import networkx as nx
    from networkx.drawing.nx_pydot import graphviz_layout

    import matplotlib.pyplot as plt

    g, labels = get_networkx_obj(spn)

    pos = graphviz_layout(g, prog='dot')
    # pos = nx.drawing.layout.rescale_layout(pos, 10)
    #plt.figure(figsize=(18, 12))
    ax = plt.gca()
    #ax.invert_yaxis()

    nx.draw(g, pos, with_labels=True, arrows=False, node_color='#DDDDDD', edge_color='#DDDDDD', width=1, node_size=450,
            labels=labels, font_size=12)
    ax.collections[0].set_edgecolor("#888888")
    edge_labels = nx.draw_networkx_edge_labels(g, pos=pos, edge_labels=nx.get_edge_attributes(g, 'weight'), font_size=12,
                                               clip_on=False, alpha=0.6)
    plt.tight_layout()
    plt.savefig(fname)

def plot_spn2(spn, fname="plot.pdf"):
    import networkx as nx
    import matplotlib.pyplot as plt

    g, _ = get_networkx_obj(spn)

    pos = graphviz_layout(g, prog='dot')
    nx.draw(g, pos, with_labels=False, arrows=False)
    plt.savefig(fname)


def plot_spn_to_svg(root_node, fname="plot.svg"):
    import networkx.drawing.nx_pydot as nxpd

    g, _ = get_networkx_obj(root_node)

    pdG = nxpd.to_pydot(g)
    svg_string = pdG.create_svg()

    f = open(fname, 'wb')
    f.write(svg_string)
