# The citybike Wien Importer

The application fetch data from citybike Wien, transform it into a different structure and to apply some filtering and sorting on it. <br>
Filters out any stations that have no free bikes available. <br>
Sorts stations by the number of free bikes descending. If two stations have the same number of bikes, sort by name ascending. <br>
Adds a property called “address” to each station. <br>

Follow the steps to build the application:

1. Build the docker image with the command: <br>
      **docker build -t citybike .**

2. Run the docker container with the command: <br>
      **docker run citybike**
      
The docker container runs a script and outputs the transformed data.
