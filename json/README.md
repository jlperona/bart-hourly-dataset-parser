# GeoJSON files

These files are GIS data meant for mapping the BART system.

## The files themselves

### `bart.kml`

This file was obtained from [the BART website](https://www.bart.gov/schedules/developers/geo) on 2019-03-10.
You can obtain the latest version of this file on their website.

### `stations.geojson`

The station data was exported to GeoJSON from KML via ArcGIS.
I removed some extraneous data, but otherwise the data is straight from the KML.

### `tracks.geojson`

The problem with the KML data above is that the tracks are listed via route, so there's one polyline for an entire route.
In order to work with a mapping software such as `mapview` in R, we need separate pieces of track between stations.
This GeoJSON file has one polyline from station to station.
I was unable to find this data anywhere else, so I made it myself.

To create this file, I imported the track data from the KML file above into ArcGIS.
I then split the polylines for the routes by the stations into separate segments.
Due to the way it was split, I had to merge some pieces back together, and remove some duplicates.
I also removed some extraneous data that wasn't needed, and renamed track segments to be more descriptive.
Finally, I exported the data to GeoJSON via ArcGIS.

## Using the files

My intended use case for this was to map the hourly data as a heat map.
I'm currently working on this, and will post the results to GitHub when I am finished.
