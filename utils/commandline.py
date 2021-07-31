import argparse
import datetime
import pynumparser  # type: ignore


def valid_date(input: str) -> datetime.datetime:
    """Verify the input date is a valid ISO 8601 date.
    Used for argparse in parse_arguments() below.
    """

    try:
        return datetime.datetime.strptime(input, '%Y-%m-%d')
    except ValueError:
        msg = 'Not a valid ISO 8601 date: \'{0}\'.'.format(input)
        raise argparse.ArgumentTypeError(msg)


def valid_type(input: str) -> str:
    """Verify the input and output graph file types are supported.
    Used for argparse in argument_parsing() below.
    """

    filetypes = {'net', 'gexf'}

    if input.split('.')[-1].lower() not in filetypes:
        msg = 'Unrecognized file format: \'{0}\'.'.format(input)
        raise argparse.ArgumentTypeError(msg)

    return input


def argument_parsing() -> argparse.Namespace:
    """Parse command line arguments."""

    parser = argparse.ArgumentParser(
        description='Take in BART origin-destination data and a source graph. '
                    'Output a weighted graph.'
    )

    # mandatory/positional arguments
    parser.add_argument(
        'inputfile',
        type=valid_type,
        metavar='input.[gexf,net]',
        help='Graph to use as the basis. Supports GEXF and Pajek NET. '
             'Format will be guessed from the file extension.'
    )

    parser.add_argument(
        'csvfile',
        metavar='input.csv',
        help='BART origin-destination data to read from.'
    )

    parser.add_argument(
        'outputfile',
        type=valid_type,
        metavar='output.[gexf,net]',
        help='Graph output file to write to. Supports GEXF and Pajek NET. '
             'Format will be guessed from the file extension.'
     )

    # optional arguments
    parser.add_argument(
        '--hours',
        type=pynumparser.NumberSequence(limits=(0, 23)),
        default=range(24),
        metavar='[0-23]',
        help='Consider only entries within a 24-hour range. '
             'Example: 0-5,7,11-21.'
    )

    parser.add_argument(
        '--weekday',
        type=pynumparser.NumberSequence(limits=(0, 6)),
        default=range(7),
        metavar='[0-6]',
        help='Consider only selected days. Monday = 0, Sunday = 6, and so on. '
             'Example: 0-3,5.'
    )

    parser.add_argument(
        '--startdate',
        type=valid_date,
        help='First date to consider. Use ISO 8601 format. '
             'Example: 2011-05-23.'
    )

    parser.add_argument(
        '--enddate',
        type=valid_date,
        help='Last date to consider. Use ISO 8601 format. Example: 2011-06-19.'
    )

    parser.add_argument(
        '-d',
        '--directed',
        action='store_true',
        help='Create a directed graph instead of an undirected one.'
    )

    parser.add_argument(
        '-k',
        '--keepweights',
        action='store_true',
        help='Keep original weights from inputfile. '
             'Useful if adding to an existing graph.'
    )

    args = parser.parse_args()

    if (args.startdate is not None and args.enddate is not None
            and args.startdate > args.enddate):
        parser.error('startdate must be before enddate.')

    return args
