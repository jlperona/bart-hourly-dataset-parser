# Network files

In order to generate an output network file, the script needs a source network file.
This allows the script to calculate the shortest paths from station to station.

## `bart.net`

This file contains the BART network layout in the [Pajek NET format](https://gephi.org/users/supported-graph-formats/pajek-net-format/).
It's good for use with programs like Gephi.
There are some multi-edges in the graph, which I added so that edges in sequence follow one of the BART routes.
After importing into NetworkX as a regular graph, these multi-edges will disappear.
