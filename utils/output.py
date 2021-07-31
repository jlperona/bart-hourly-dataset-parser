import argparse
import networkx as nx  # type: ignore

from typing import Union


def generate_output(args: argparse.Namespace,
                    base_graph: Union[nx.Graph, nx.DiGraph]) -> None:
    """Have NetworkX write to the output file given the parsed graph."""

    outputtype = args.outputfile.split('.')[-1].lower()

    # write to output file
    if outputtype == 'net':
        nx.write_pajek(base_graph, args.outputfile)
    elif outputtype == 'gexf':
        nx.write_gexf(base_graph, args.outputfile)
