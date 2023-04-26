# Purpose

This document is a informal, very high level summary of what is required for the project. It will NOT contain any detailed requirement. Those will be tracked in a different document.

# Project Scope and Requirements

Here we define the scope of this project. This project is a *prototype* of the bigger "Music Data Visualizer" project. Specifically, it showcases a single visualization - the listening volume over time chart, and we will use it to explore what tools we want to use and the capability of those tools.

## In-Scope Requirements:

The requirements that are in scope for this project are:
* Presenting a working chart of your music listening activity over a period of time
* Make this chart interactive, able to respond to various user controls in an intuitive, user friendly way.
* Make this chart pretty and pleasing to the eye
* Makes this chart *moderately* creative: You don't have to go all out with the creativity on this one. A simple line chart will do.
* Allows this chart to take in real music data that spans at least 1 year and display the info.

## Out-of-scope requirements:

The requirement that are OUT OF SCOPE for this project are:
* Load real data in an efficient and user friendly way. 
    * The data are there just so that we can test the chart. Making a good back end isn't the purpose of this prototype.
* Host this project on a web server.
* Implement any backend code.
* Able to add new charts easily
    * That would be considered when we are making the real webpage or maybe with a different prototype. For this, don't bother with that. Just do one chart and do it right.
* Implement any additional user control, outside of the chart controls and some basic data loading stuffs.


## Detailed Requirements:

### Definition

* **Song stream**: Counted when someone listens for 30 seconds or more. Same as the definition used in Spotify and LastFM to count "scrubbles"
* **New song stream**: A song stream is **new** if there are less than 3 streams prior to the current stream. 

### 1. Chart Type:

**1.1** The chart needs to cover the *total song stream time / number* (will be called *total song stream*) per *day*, over a period of at least one year. To be more clear:    
  * **1.1.1** The x-axis must be date;
  * **1.1.2** The y-axis must be either listening time (in minutes or hours) or number of scrubbles (count)
  * **1.1.3** The date range in the x-axis must span <i>at least </i> one year.

**1.2** The chart needs to be an area chart (i.e. the area underneath the area is colored)

**1.3** The chart needs to have two datasets, represented as two lines on the chart:
* **1.3.1** The first data set represents the total stream time of **all** songs in one year

* **1.3.2** The second dataset represents the total stream time of all **new** songs in one year. (see definition of *new song stream*)

### 2. Chart Controls:
