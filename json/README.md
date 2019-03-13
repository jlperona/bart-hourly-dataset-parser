# GeoJSON files

These files are GIS data meant for mapping the BART system.

## The files themselves

### `bart.kml`

This file was obtained from [the BART website](https://www.bart.gov/schedules/developers/geo) on 2019-03-10.
You can obtain the latest version of this file on their website.

### `stations.geojson`

The station data was originally exported to GeoJSON from KML via ArcGIS.
However, I've made significant edits to remove extraneous data provided by ArcGIS.
I also corrected the station names to match the [system map](https://www.bart.gov/system-map), and provided the abbreviations separately.

Normally, I'm a fan of reproducible analysis, and being able to reproduce this file from the original KML via a script would be nice.
However, I made significant changes to what was provided in the original KML, so I don't see a way to make a script to reproduce this.
Thankfully, adding future stations will be fairly easy.

### `tracks.geojson`

The problem with the KML data above is that the tracks are listed via route, so there's one polyline for an entire route.
In order to work with a mapping software such as `mapview` in R, we need separate pieces of track between stations.
This GeoJSON file has one polyline from station to station.
I was unable to find this data anywhere else, so I made it myself.

To create this file, I imported the track data from the KML file above into ArcGIS.
I then split the polylines for the routes by the stations into separate segments.
Due to the way it was split, I had to merge some pieces back together, and remove some duplicates.
Finally, I exported the data to GeoJSON via ArcGIS.
I also removed some extraneous data provided by ArcGIS, and renamed track segments to be more descriptive.

Again, while I'm a fan of reproducible analysis, I don't see a way to reproduce what I did in ArcGIS via a script.

## Using the files

My intended use case for this was to map the hourly data as a heat map.
I'm currently working on this, and will post the results to GitHub when I am finished.
