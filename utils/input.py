import argparse
import csv
import networkx as nx  # type: ignore

from datetime import datetime
from typing import Union

station_names = {
    '12TH': '12th St/Oakland City Center',
    '16TH': '16th St Mission',
    '19TH': '19th St/Oakland',
    '24TH': '24th St Mission',
    'ANTC': 'Antioch',
    'ASHB': 'Ashby',
    'BALB': 'Balboa Park',
    'BAYF': 'Bay Fair',
    'BERY': 'Berryessa',
    'CAST': 'Castro Valley',
    'CIVC': 'Civic Center/UN Plaza',
    'COLM': 'Colma',
    'COLS': 'Coliseum',
    'CONC': 'Concord',
    'DALY': 'Daly City',
    'DBRK': 'Downtown Berkeley',
    'DELN': 'El Cerrito del Norte',
    'DUBL': 'Dublin/Pleasanton',
    'EMBR': 'Embarcadero',
    'FRMT': 'Fremont',
    'FTVL': 'Fruitvale',
    'GLEN': 'Glen Park',
    'HAYW': 'Hayward',
    'LAFY': 'Lafayette',
    'LAKE': 'Lake Merritt',
    'MCAR': 'MacArthur',
    'MLBR': 'Millbrae',
    'MLPT': 'Milpitas',
    'MONT': 'Montgomery St',
    'NBRK': 'North Berkeley',
    'NCON': 'North Concord/Martinez',
    'OAKL': 'Oakland International Airport (OAK)',
    'ORIN': 'Orinda',
    'PCTR': 'Pittsburg Center',
    'PHIL': 'Pleasant Hill/Contra Costa Centre',
    'PITT': 'Pittsburg/Bay Point',
    'PLZA': 'El Cerrito Plaza',
    'POWL': 'Powell St',
    'RICH': 'Richmond',
    'ROCK': 'Rockridge',
    'SANL': 'San Leandro',
    'SBRN': 'San Bruno',
    'SFIA': 'San Francisco International Airport (SFO)',
    'SHAY': 'South Hayward',
    'SSAN': 'South San Francisco',
    'UCTY': 'Union City',
    'WARM': 'Warm Springs/South Fremont',
    'WCRK': 'Walnut Creek',
    'WDUB': 'West Dublin/Pleasanton',
    'WOAK': 'West Oakland'
}


def generate_base_graph(args: argparse.Namespace) -> Union[nx.Graph,
                                                           nx.DiGraph]:
    """Create the base graph used for the remainder of the calculations.
    Import from inputfile, then convert to directed or undirected as desired.
    """

    inputtype = args.inputfile.split('.')[args.inputfile.count('.')].lower()

    # import graph representation using NetworkX
    if inputtype == 'net':
        base_multigraph = nx.read_pajek(args.inputfile)
    elif inputtype == 'gexf':
        base_multigraph = nx.read_gexf(args.inputfile)

    if args.directed is True:
        return nx.DiGraph(base_multigraph)
    else:
        return nx.Graph(base_multigraph)


def parse_csv(args: argparse.Namespace,
              base_graph: Union[nx.Graph, nx.DiGraph],
              shortest_paths: dict) -> None:
    """Import the CSV file and start reading in rows.
    Write weights to the base graph.
    """

    with open(args.csvfile) as csvfile:
        csvreader = csv.reader(csvfile)

        # parse out relevant information in row
        for row in csvreader:
            linenumber = csvreader.line_num

            try:
                date = datetime.strptime(row[0], '%Y-%m-%d')
                weekday = date.weekday()
                hour = int(row[1])
                source = station_names[row[2]]
                destination = station_names[row[3]]
                passengers = int(row[4])

                # skip hours not in desired subset
                if hour not in args.hours:
                    continue
                # skip weekdays not in desired subset
                elif weekday not in args.weekday:
                    continue
                # skip dates not in desired subset
                elif args.startdate is not None and date < args.startdate:
                    continue
                elif args.enddate is not None and date > args.enddate:
                    continue

                # for every adjacent pair of vertices in the shortest path
                for index in range(len(shortest_paths[source][destination])
                                   - 1):
                    first = shortest_paths[source][destination][index]
                    second = shortest_paths[source][destination][index + 1]

                    # add the number of passengers to the edge weight
                    base_graph[first][second]['weight'] += passengers
            except Exception:
                print('Exception occurred at line number ',
                      linenumber, ' in ', args.csvfile, '.', sep='')
                raise

    # remove original weights if specified
    if args.keepweights is False:
        for source, destination in nx.edges(base_graph):
            base_graph[source][destination]['weight'] -= 1
