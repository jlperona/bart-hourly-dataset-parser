# bart-hourly-dataset-parser

Parses San Francisco BART hourly origin-destination data into graph files.
For a Shiny application that is heavily based on this, see [`bart-passenger-heatmap`](https://github.com/jlperona/bart-passenger-heatmap).

## Background

### Reasoning

This script is designed to parse BART hourly origin-destination files and output weighted graph files.
Parsing these into graph files is useful for visualizing the BART network, due to the differing edge weights.
The origin-destination data is provided on [their website](https://www.bart.gov/about/reports/ridership), available starting from 2011-01-01.

### Script

The script does the following:

1. Parses an input graph to set up the network topology.
2. Reads in the hourly data line by line.
3. For each origin-destination pair, calculate the shortest path between the two stations.
    * Due to the current topology of the network, there will only ever be one shortest path.
4. Add the number of passengers to each edge on the shortest path.
5. Output the graph file, in the desired format.

## Python

### Version

This is a Python 3 script.

### Dependencies

The script uses the following packages that aren't provided in base Python:

* `networkx` for parsing the input graph.
* `pynumparser` for range parsing the hour and weekday arguments.

Both of these can be found on `pip`.
If you'd like to set up a virtual environment, the typical code to do so is below:

```
python3 -m venv env
source env/bin/activate
python3 -m pip install -r requirements.txt
```

## Usage

    python3 bart-hourly-dataset-parser.py [-h] [--flags] input.graph bartdata.csv output.graph

### Flags

The following flags are available.
For more information, use the `-h` flag when running the script.

#### Subsetting by Hour

`--hour` allows you to subset the input data and choose hours that you want to keep.
This uses 24 hour format, to match the input data style.
Multiple ranges are allowed.
Here is an example of a valid subset: 0-12,15,19-21,23.

#### Subsetting by Weekday

`--weekday` allows you to subset the input data and choose only the weekdays that you want to keep.
The numbering matches the system used in Python's `datetime` package.
Monday corresponds to 0, and Sunday corresponds to 6.
Multiple ranges are allowed.
Here is an example of a valid subset: 0-2,4,6.

#### Subsetting by Date

`--startdate` and `--enddate` allow you to subset the input data and choose a range of dates that you want to keep.
If both flags are not provided, the script will parse all data in the input CSV.
The script expects ISO 8601-style dates.
Therefore, 25 January 2016 corresponds to 2016-01-25.

#### Graph Options

`-d` and `--directed` allow you to specify that a directed graph should be output.
By default, the script defaults to an undirected graph.

`-k` and `--keepweights` allow you to keep the original weights from the input graph file.
The script will then add on the weight from the input CSV.
This is useful if you are, say, trying to grab data from multiple years, and don't want to combine the data files for each year by hand.
This flag shouldn't be used for the first run, when initially generating data from the basic topological graph.
The edge weights will be slightly wrong in that case.

### Positional Arguments

#### `input.graph`

The representation of the BART network that serves as the basis to calculate shortest paths.
An example file has already been provided at `data/bart.net`.
Note that this file will need to be modified to keep up with expansions in the BART network.
See the **Dataset Caveats** section below.

#### `bartdata.csv`

The CSV files provided by BART on [their website](https://www.bart.gov/about/reports/ridership).
The script does a decent job in offering options to subset the data.
If you need more detailed subsetting options, I recommend doing so with another program.

#### `output.graph`

The output graph file.
Currently, the following file formats are supported:

* GEXF
* Pajek NET

NetworkX supports many other graph file formats.
Adding these would be fairly simple.

## Dataset Caveats

The following sections were written and are true as of 2021-07-31.
Changes to the BART network will change the validity of the following sections.

### Network Changes

BART has been changing since the start of their data set collection.
In particular, the following changes have been made since 2011-01-01, the first day available in the dataset:

#### West Dublin / Pleasanton

The *West Dublin / Pleasanton* station opened for revenue service on 2011-02-19.
Dates before this (of which there are not that many) will have traffic identical on both sides of the station, as this is an infill station.

#### Oakland International Airport (OAK)

The *Oakland International Airport (OAK)* station opened for revenue service on 2014-11-22.
Dates before this will have no traffic to this node, as this is a terminal station.
This may pose a problem for certain programs, such as Gephi.

#### Warm Springs / South Fremont

The *Warm Springs / South Fremont* station opened for revenue service on 2017-03-25.
Dates before this will have no traffic to this node, as this is a terminal station.
This may pose a problem for certain programs, such as Gephi.

#### eBART

The eBART extension to *Pittsburg Center* and *Antioch* opened for revenue service on 2018-05-26.
Dates before this will have no traffic to either of these stations, as these nodes extend past a terminal station.
This may pose a problem for certain programs, such as Gephi.


#### Milpitas and Berryessa

The *Milpitas* and *Berryessa* stations opened for revenue service on 2020-06-13.
Dates before this will have no traffic to these nodes, as Berryessa is a terminal station.
This may pose a problem for certain programs, such as Gephi.

### Future Network Changes

There are also changes that have been made or planned since the last day available in the dataset.

#### BART to Silicon Valley

The Silicon Valley BART extension to the following stations are currently planned to open in 2030:

* *Alum Rock*
* *Downtown San Jose*
* *Diridon / Arena*
* *Santa Clara*

The input network file and `station_names` dictionary in `utils/input.py` will need to be modified to support these stations when they open.

### Network Changes by Time

The BART network changes at certain hours of the day.
The following lines run to *Millbrae* and *San Francisco International Airport (SFO)*:

* Antioch - SFO / Millbrae
* Richmond - Daly City / Millbrae

During weekdays before 21:00, the Richmond - Daly City / Millbrae continues on from Daly City to Millbrae, skipping SFO.
After 21:00 on weekdays, and on weekends, that line terminates at Daly City.
Instead, a separate line (the SFO-Millbrae Shuttle) runs instead.

In order to be completely correct, the script should take this into account.
Traffic that has Millbrae as one of its starting or ending points should be checked to see what day and time it occurs in.
If the traffic occurs before 21:00 on a weekday, only the San Bruno - Millbrae edge should have weight added to it.
At the other times, both the San Bruno - SFO and SFO - Millbrae edges should have weight added to them.

This is not a significant change, but I have not added it to the script.
Thus, results involving those stations are slightly incorrect.

## Future

I have a couple of changes in mind for the future:

* Add new BART expansions to the script
* Update the script logic to account for the Millbrae and SFO edge change, described above
* Add the ability to read and write the rest of the graph file formats that NetworkX supports
