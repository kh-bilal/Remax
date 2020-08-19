#!/usr/bin/env python
# coding: utf-8

# #### In Data Analysis We will Analyze To Find out the below stuff
# 1. Missing Values
# 2. All The Numerical Variables
# 3. Distribution of the Numerical Variables
# 4. Categorical Variables
# 5. Cardinality of Categorical Variables
# 6. Outliers
# 7. Relationship between independent and dependent feature(SalePrice)

# In[186]:


#lecture data 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
## Display all the columns of the dataframe

pd.pandas.set_option('display.max_columns',None)

dataset = pd.read_csv("centris_montreal_complete.csv")
dataset.head()


# In[187]:


dataset.info()


# In[188]:


## Here we will check the type of each feature

for feature in dataset.columns: 
    print(feature, ", type:",dataset[feature].dtypes)


# ### 1) Missing Values

# In[189]:


## Here we will check the percentage of nan values present in each feature
## 1 -step make the list of features which has missing values
features_with_nan= [feature for feature in dataset.columns if dataset[feature].isnull().sum()>1]

## 2- step print the feature name and the percentage of missing values
for feature in features_with_nan:
    print(feature, np.round((dataset[feature].isnull().mean()),2)*100,"% of missing values")


# #### Since they are many missing values, we need to find the relationship between missing values and Price
# > Let's plot some diagram for this relationship
# 

# In[190]:


# converte price object to float
dataset["price"]= dataset["price"].str.replace("$","")
dataset["price"]= dataset["price"].str.replace(",","")
dataset["price"]= dataset["price"].astype(float)


# In[192]:


for feature in features_with_nan:
    data = dataset.copy()
    
    # let's make a variable that indicates 1 if the observation was missing or zero otherwise
    data[feature] = np.where(data[feature].isnull(), 1, 0)
    
    # let's calculate the mean price where the information is missing or present
    data.groupby(feature)['price'].mean().plot.bar()
    plt.title(feature)
    plt.show()


# Here With the relation between the missing values and the dependent variable is clearly visible. So We need to replace these nan values with something meaningful or drop it.

# ### 2) Numerical Variables

# In[193]:


# converte objects features to float (Net area, Gross area, Lot area, Year built)

#Net area, Gross area, Lot area
feature_area = ["Net area","Gross area","Lot area"]
for feature in feature_area:
    data[feature]= data[feature].str.replace("sqft","")
    data[feature]= data[feature].str.replace(",","")
    data[feature]= data[feature].astype(float)   

#Year built
data["Year built"]= data["Year built"].str.replace("To be built, New","2021")
data["Year built"]= data["Year built"].str.replace("Under construction, New","2021")
data["Year built"]= data["Year built"].str.replace(", Century","")
data["Year built"]= data["Year built"].str.replace(", New","")
data["Year built"]= data["Year built"].str.replace(", Historic","")
data["Year built"]= data["Year built"].str.replace(", Being converted","")
data["Year built"]= data["Year built"].str.replace("Unknown age","2021")
# data["Year built"]= data["Year built"].astype(float)


# In[194]:


numerical_features = [feature for feature in dataset.columns if dataset[feature].dtypes != 'O']

print('Number of numerical variables: ', len(numerical_features))

# visualise the numerical variables
dataset[numerical_features].head()


# In[195]:


## Lets analyze the Datetime Variables
## We will check whether there is a relation between year the house is sold and the sales price

data.groupby('Year built')['price'].mean().plot()
plt.xlabel('Year')
plt.ylabel('Mean House Price')
plt.title("House Price vs Year")


# In[200]:


## Numerical variables are usually of 2 type
## 1. Continous variable and Discrete Variables

discrete_feature=[feature for feature in numerical_features if len(dataset[feature].unique())<25 and feature not in ['Unnamed: 0','Year built']]
print("Discrete Variables Count: {}".format(len(discrete_feature)))


# In[201]:


discrete_feature


# In[202]:


dataset[discrete_feature].head()


# In[204]:


## Lets Find the realtionship between them and Sale PRice

for feature in discrete_feature:
    data=dataset.copy()
    data.groupby(feature)['price'].mean().plot.bar()
    plt.xlabel(feature)
    plt.ylabel('price')
    plt.title(feature)
    plt.show()


# ### 2) Continuous Variables

# In[206]:


continuous_feature=[feature for feature in numerical_features if feature not in discrete_feature+['Unnamed: 0','Year built']]
print("Continuous feature Count {}".format(len(continuous_feature)))


# In[207]:


## Lets analyse the continuous values by creating histograms to understand the distribution

for feature in continuous_feature:
    data=dataset.copy()
    data[feature].hist(bins=25)
    plt.xlabel(feature)
    plt.ylabel("Count")
    plt.title(feature)
    plt.show()


# In[ ]:




