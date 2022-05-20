# PropertyAnalysisIP

Progress Report:

1) Our first weeks were mainly focused on reading research papers. Two of which we found useful are attached below. The papers were based on properties in Valencia, Spain and Greater London.

2) Next, we created two scraper classes from scratch using selenium in python. These were used to scrape property samples from magicbricks.com and 99acres.com. We searched for properties in New Delhi, and scraped all the relevant features of each properties. We currently have around 1000+ samples. We also did some preprocessing like removing null values, feature generation, outlier removal, etc.

3) The properties which we scraped didn’t have one necessary feature and that is the location rating, which is how good the neighborhood is and for that we had to manually create this feature. This was done using geocoding and nearby place search by TomTom API. We used the address extracted from the website and used geocoding to get the latitudes and longitudes. After that we found nearest Points of interests like schools, malls, police stations, etc. If there was a higher density of such points, we gave it a higher location rating.

4) Then we trained some basic regression models on this dataset. We achieved a MSE of 7702 and R-score of  around 0.3. For a dataset of this size, this seems to be a pretty decent score. We tried a simple DL model as well, but a simple linear regression model performed better. 

5) Finally we made some basic graphs to understand the feature importance. We passed a random samples and changed just a single feature keeping other features constant in the sample and predicted the prices. Some of these graphs are attached below.

Our next step is to try to increase the score, either by collecting more data or trying to improve the location rating feature.
