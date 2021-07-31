# package imports
import networkx as nx  # type: ignore

# relative imports
import utils.commandline
import utils.input
import utils.output


def main() -> None:
    """Take in inputs, generate output graph file."""

    args = utils.commandline.argument_parsing()
    base_graph = utils.input.generate_base_graph(args)
    shortest_paths = nx.shortest_path(base_graph)
    utils.input.parse_csv(args, base_graph, shortest_paths)
    utils.output.generate_output(args, base_graph)


if __name__ == "__main__":
    main()
