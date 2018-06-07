# bart-hourly-dataset-parser

Parses San Francisco BART hourly origin-destination data into graph files.

## Background

### Reasoning

This script is designed to parse BART hourly origin-destination files, and output graph files.
Parsing these into graph files is useful for visualizing the BART network, due to the differing edge weights.
The origin-destination data is provided on [their website](https://www.bart.gov/about/reports/ridership), available starting from 2011-01-01.

### Script

The script does the following:

* Parses an input graph to set up the network topology.
* Reads in the hourly data line by line.
* For each origin-destination pair, calculate the shortest path between the two stations.
    * Due to the current topology of the network, there will only ever be one shortest path.
* Add the number of passengers to each edge on the shortest path.
* Output the graph file, in the desired format.

## Python

### Version

This is a Python 3 script.

### Dependencies

The script uses the following packages that aren't provided in base Python:

* `networkx` for parsing the input graph.
* `pynumparser` for range parsing the hour and weekday arguments.

Both of these can be found on `pip`.
Feel free to install them in any way you wish.

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
If both flags are not provided, the script will parse all data in the input `csv`.
The script expects ISO 8601-style dates.
Therefore, 25 January 2016 corresponds to 2016-01-25.

#### Graph Options

`-d` and `--directed` allow you to specify that a directed graph should be output.
By default, the script defaults to an undirected graph.

`-k` and `--keepweights` allow you to keep the original weights from the input graph file.
The script will then add on the weight from the input `csv`.
This is useful if you are, say, trying to grab data from multiple years, and don't want to combine the data files for each year by hand.
This flag shouldn't be used for the first run, when initially generating data from the basic topological graph.
The edge weights will be slightly wrong in that case.

### Positional Arguments

#### input.graph

The representation of the BART network that serves as the basis to calculate shortest paths.
An example file has already been provided, in `data/bart.gexf`.
Note that this file will need to be modified to keep up with expansions in the BART network.
See the **Dataset Caveats** section below.

#### bartdata.csv

The `csv` files provided by BART on [their website](https://www.bart.gov/about/reports/ridership).
The script does a decent job in offering options to subset the data.
If you need more detailed subsetting options, I recommend doing so with another program.

#### output.graph

The output graph file.
Currently, the following file formats are supported:

* GEXF
* Pajek NET

NetworkX supports many other graph file formats.
Adding these would be fairly simple.

## Dataset Caveats

The following sections were written and are true as of 2018-06-05.
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
I have not found the four-letter code for this station.
When I do, I will update the dictionary to make the translation.

#### Warm Springs / South Fremont

The *Warm Springs / South Fremont* station opened for revenue service on 2017-03-25.
Dates before this will have no traffic to this node, as this is a terminal station.
This may pose a problem for certain programs, such as Gephi.
I have not found the four-letter code for this station.
When I do, I will update the dictionary to make the translation.

### Future Network Changes

There are also changes that have been made or planned since the last day available in the dataset.

#### eBART

The eBART extension to *Pittsburg Center* and *Antioch* opened for revenue service on 2018-05-26.
Currently, no data is available past 2017.
Once data is available, the stations and their four-letter codes can be added.

#### BART to Silicon Valley

The Silicon Valley BART extension in planned in two phases.
The following stations are (currently) planned to open in fall 2018:

* *Milpitas*
* *Berryessa*

The following stations are currently planned to open in 2025 - 2026:

* *Alum Rock*
* *Downtown San Jose*
* *Diridon / Arena*
* *Santa Clara*

I will add these stations as these extensions open, and data becomes available for them.

### Network Changes by Time

The BART network changes at certain hours of the day.
The changes that are made are the following:

#### Warm Springs / South Fremont

The following lines run to *Warm Springs / South Fremont*:

* Richmond - Warm Springs / South Fremont
* Warm Springs / South Fremont - Daly City

These lines run to Warm Springs at mutually exclusive times.
This is due to a shortage of trains.
As the Fleet of the Future continues to arrive, this time change should eventually disappear.

No changes need to be made to graph files to account for this.
The lines run between the same stations, so there is only one shortest path to take.

#### Millbrae and San Francisco International Airport (SFO)

The following lines run to *Millbrae* and *San Francisco International Airport (SFO)*:

* Antioch - SFO / Millbrae
* Richmond - Daly City / Millbrae

During weekdays before 21:00, the Richmond - Daly City / Millbrae continues on from Daly City to Millbrae, skipping SFO.
After 21:00 on weekdays, and on weekends, that line terminates at Daly City.
Instead, the Antioch - SFO / Millbrae line is extended from SFO to Millbrae.

In order to be completely correct, the script should take this into account.
Traffic that has Millbrae as one of its starting or ending points should be checked to see what day and time it occurs in.
If the traffic occurs before 21:00 on a weekday, only the San Bruno - Millbrae edge should have weight added to it.
At the other times, both the San Bruno - SFO and SFO - Millbrae edges should have weight added to them.

This is not a significant change, but I have not added it to the script.
Thus, results involving those stations are slightly incorrect.
In the future, I will consider adding this.

# Future

I have a couple of changes in mind for the future:

* Add new and recent BART expansions to the script
* Update the script logic to account for the Millbrae and SFO edge change, described above
* Add the ability to read and write the rest of the graph file formats that NetworkX supports
