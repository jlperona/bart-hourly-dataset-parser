import argparse
import csv
import networkx as nx
import pynumparser
from datetime import datetime

station_names = {
    '12TH' : '12th St/Oakland City Center',
    '16TH' : '16th St Mission',
    '19TH' : '19th St/Oakland',
    '24TH' : '24th St Mission',
    'ANTI' : 'Antioch',
    'ASHB' : 'Ashby',
    'BALB' : 'Balboa Park',
    'BAYF' : 'Bay Fair',
    'CAST' : 'Castro Valley',
    'CIVC' : 'Civic Center/UN Plaza',
    'COLM' : 'Colma',
    'COLS' : 'Coliseum',
    'CONC' : 'Concord',
    'DALY' : 'Daly City',
    'DBRK' : 'Downtown Berkeley',
    'DELN' : 'El Cerrito del Norte',
    'DUBL' : 'Dublin/Pleasanton',
    'EMBR' : 'Embarcadero',
    'FRMT' : 'Fremont',
    'FTVL' : 'Fruitvale',
    'GLEN' : 'Glen Park',
    'HAYW' : 'Hayward',
    'LAFY' : 'Lafayette',
    'LAKE' : 'Lake Merritt',
    'MCAR' : 'MacArthur',
    'MLBR' : 'Millbrae',
    'MONT' : 'Montgomery St',
    'NBRK' : 'North Berkeley',
    'NCON' : 'North Concord/Martinez',
    'OAKL' : 'Oakland International Airport (OAK)',
    'ORIN' : 'Orinda',
    'PCTR' : 'Pittsburg Center',
    'PHIL' : 'Pleasant Hill/Contra Costa Centre',
    'PITT' : 'Pittsburg/Bay Point',
    'PLZA' : 'El Cerrito Plaza',
    'POWL' : 'Powell St',
    'RICH' : 'Richmond',
    'ROCK' : 'Rockridge',
    'SANL' : 'San Leandro',
    'SBRN' : 'San Bruno',
    'SFIA' : 'San Francisco International Airport (SFO)',
    'SHAY' : 'South Hayward',
    'SSAN' : 'South San Francisco',
    'UCTY' : 'Union City',
    'WCRK' : 'Walnut Creek',
    'WDUB' : 'West Dublin/Pleasanton',
    'WOAK' : 'West Oakland'
    'WSPR' : 'Warm Springs/South Fremont'
}

def valid_date(input):
    try:
        return datetime.strptime(input, '%Y-%m-%d')
    except ValueError:
        msg = 'Not a valid ISO 8601 date: \'{0}\'.'.format(input)
        raise argparse.ArgumentTypeError(msg)

def valid_type(input):
    filetypes = {'net', 'gexf'}

    if input.split('.')[input.count('.')].lower() not in filetypes:
        msg = 'Unrecognized file format: \'{0}\'.'.format(input)
        raise argparse.ArgumentTypeError(msg)

    return input

parser = argparse.ArgumentParser(
    description = 'Take in BART origin-destination data and a source graph. Output a weighted graph.')

# mandatory/positional arguments
parser.add_argument('inputfile', type = valid_type, metavar = 'input.[gexf,net]',
    help = 'Graph to use as the basis. Supports GEXF and Pajek NET. Format will be guessed from the file extension.')
parser.add_argument('csvfile', metavar = 'input.csv',
    help = 'BART origin-destination data to read from.')
parser.add_argument('outputfile', type = valid_type, metavar = 'output.[gexf,net]',
    help = 'Graph output file to write to. Supports GEXF and Pajek NET. Format will be guessed from the file extension.')

# optional arguments
parser.add_argument('--hours', type = pynumparser.NumberSequence(limits = (0, 23)), default = range(0, 23),
    metavar = '[0-23]', help = 'Consider only entries within 24-hour range. Example: 0-5,7,11-21.')
parser.add_argument('--weekday', type = pynumparser.NumberSequence(limits = (0, 6)), default = range(0, 6),
    metavar = '[0-6]', help = 'Consider only selected days. Monday = 0, Sunday = 6. Example: 0-3,5.')
parser.add_argument('--startdate', type = valid_date,
    help = 'First date to consider. Use ISO 8601 format, example: 2011-05-23.')
parser.add_argument('--enddate', type = valid_date,
    help = 'Last date to consider. Use ISO 8601 format, example: 2011-06-19.')
parser.add_argument('-d', '--directed', action = 'store_true',
    help = 'Create a directed graph instead of an undirected one.')
parser.add_argument('-k', '--keepweights', action = 'store_true',
    help = 'Keep original weights from inputfile. Useful if adding to an existing graph.')

args = parser.parse_args()

if args.startdate is not None and args.enddate is not None and args.startdate > args.enddate:
    parser.error('startdate must be before enddate.')

inputtype = args.inputfile.split('.')[args.inputfile.count('.')].lower()

# import graph representation using NetworkX
if inputtype == 'net':
    base_multigraph = nx.read_pajek(args.inputfile)
elif inputtype == 'gexf':
    base_multigraph = nx.read_gexf(args.inputfile)

if args.directed is True:
    base_graph = nx.DiGraph(base_multigraph)
else:
    base_graph = nx.Graph(base_multigraph)

shortest_paths = nx.shortest_path(base_graph)

# import CSV file and start reading in rows
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
            if weekday not in args.weekday:
                continue

            # skip dates not in desired subset
            if args.startdate is not None and date < args.startdate:
                continue

            if args.enddate is not None and date > args.enddate:
                continue

            # for every adjacent pair of vertices in the shortest path
            for index in range(0, len(shortest_paths[source][destination]) - 1):
                first = shortest_paths[source][destination][index]
                second = shortest_paths[source][destination][index + 1]

                # add the number of passengers to the edge weight
                base_graph[first][second]['weight'] += passengers
        except:
            print('Exception occurred at line number', linenumber, 'in', args.csvfile)
            raise

# remove original weights if specified
if args.keepweights is False:
    for source, destination in nx.edges(base_graph):
        base_graph[source][destination]['weight'] -= 1

outputtype = args.outputfile.split('.')[args.outputfile.count('.')].lower()

# write to output file
if outputtype == 'net':
    nx.write_pajek(base_graph, args.outputfile)
elif outputtype == 'gexf':
    nx.write_gexf(base_graph, args.outputfile)
