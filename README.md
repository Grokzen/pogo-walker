# Installation

Install pypy on your system or you will not have enough performance to run this code.

Install google earth on your system.



# Run the code

Fetch a raw query from a rocketmap instance and put it in the file raw.json

Then run the following commands

```
# Transform the data from the raw rocketmap query to data this code can more easily work with
pypy transform_raw.py

# Run the main code logic that tests all paths and builds the shortest path from each point
time pypy main2.py

# The winning ID must be manually dumped in order to get a file that can be used to build a .kml file that can be used for google maps
time pypy dump.py 465f9e6f07d
```

The dumped csv file should be uploaded to this page https://www.earthpoint.us/ExcelToKml.aspx then you click on `View on google earth`. It will download a .kml file that will open in google earth and it will show you the paths that you should walk.
