# dash_heroku_deployment

# Description
This is a dash application allowing the user to examine and dig down on chrnoic conditions within the synthetic Synpuf data set. A live deployment can be found [here](https://telbert6-cs6440-miniproject2.herokuapp.com/).

# Prerequisites
1. Python 3
2. Jupyter notebooks (optional)
2. requirements.txt (pip install -r requirements.txt)

# To run
1. Clone this repo or make sure all the files are in the same directory
2. (**OPTIONAL**) If you wish to generate the clean data, run the Synpuf-cleaning.ipynb. It will re-generate a cleaned and aggregated version of the Synpuf data as *agg.csv* and re-pull the shape file as *counties.json*
3. run *python .\app.py* to launch the server. Click the url in the first line of output from this command to view the dashboard.
