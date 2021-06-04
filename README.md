# WineQualityMLProject
What makes a wine good? Is data analytics able to predict what physical-chemical characteristics make a good wine? Our team decided to take this challenge.
A machine learning model for predicting wine quality.

# General approach to the problem
1. The dataset was cleaned and put into an SQL database ans csv files.
2. A multivariate linear regression was carried out.
3. PCA (Principal component analysis) was used to reduce the problem dimensions
4. kNN (k-Nearest Neighbor) was use to classify both the type and the quality of wine.
5. The wines were divided into two types: red and white and 3 categories for quality: 'good','average','bad'.
6. The data was deployed by using Heroku and a flask app. [Check it out!](https://winequalityml.herokuapp.com/)
----------
The model development can be found along with the exploratory analysis in the Jupyter notebook called [Exploratory Analysis](./Exploratory_analysis.ipynb), while the model testing can be found in the one called [Model_test](Model_test.ipynb). \
[Procfile](Procfile) and [Requirements](Requirements.txt) are necessary fo the deployment on Heroku as explained [here](https://stackabuse.com/deploying-a-flask-application-to-heroku). A virtual environment was created but ignored while pushing to GitHub. \
Finally, [app.py](app.py) is the code for our web app and relies on the functions reported in [wine_ML.py](wine_ML.py) and all the files in the folders [lib](lib),[static](static) and [templates](templates).

# Flask structure and web page images
```
\
```
The home page is simple and tries to explain in a few words the motivation.
![home_page](./images/ReadMe/home_page.png)
```
\analysis
```
The main take home messages and conclusions from the data analysis are reported in this page with additional information sources.
![analysis_page](./images/ReadMe/analysis.png)
```
\prediction
```
The prediction page is the fun page, the user can insert its own prediction and a plot will be generated showing where the predicted point is with respect to the model points. The plot is updated live until the user leaves the page, at that point the plot refreshes.
![prediction](./images/ReadMe/prediction.gif)
```
\about
```
![about_us](./images/ReadMe/about_us.png)

# Dataset
[Wine Quality Datasets](http://www3.dsi.uminho.pt/pcortez/wine/)

# References
1. P. Cortez, A. Cerdeira, F. Almeida, T. Matos and J. Reis. Modeling wine preferences by data mining from physicochemical properties. In Decision Support Systems, Elsevier, 47(4):547-553, 2009.
2. Scikit-learn: Machine Learning in Python, Pedregosa et al., JMLR 12, pp. 2825-2830, 2011.
