#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# In[2]:


retail = pd.read_csv('OnlineRetail.csv')


# In[3]:


retail.columns


# In[4]:


retail.head()


# In[5]:


retail.tail()


# In[6]:


retail.describe()


# In[7]:


retail.info()


# In[8]:


retail.isnull().sum()


# In[9]:


retail = retail[pd.notnull(retail['CustomerID'])]
len(retail)


# In[10]:


retail = retail[retail['Quantity'] > 0]
retail = retail[retail['UnitPrice'] > 0]

len(retail)


# In[11]:


retail.info()


# In[12]:


retail['CustomerID'] = retail['CustomerID'].astype(np.int32)
retail.info()


# In[13]:


retail['CheckoutPrice'] = retail['UnitPrice'] * retail['Quantity']
retail.head()


# In[14]:


import numpy as np
import pandas as pd
# seaborn
import seaborn as sns
COLORS = sns.color_palette()

get_ipython().run_line_magic('matplotlib', 'inline')


# In[15]:


dtypes = {
    'UnitPrice': np.float32,
    'CustomerID': np.int32,
    'Quantity': np.int32
}
retail.head()


# In[16]:


retail['InvoiceDate'] = pd.to_datetime(retail['InvoiceDate'], infer_datetime_format=True)
retail.info()


# In[17]:


total_revenue = retail['CheckoutPrice'].sum()
total_revenue


# In[18]:


rev_by_countries = retail.groupby('Country').sum()['CheckoutPrice'].sort_values()
rev_by_countries


# In[19]:


plot = rev_by_countries.plot(kind='bar', color=COLORS[-1], figsize=(20, 10))
plot.set_xlabel('Country', fontsize=11)
plot.set_ylabel('Revenue', fontsize=11)
plot.set_title('Revenue by Country', fontsize=13)
plot.set_xticklabels(labels=rev_by_countries.index, rotation=45)


# In[20]:


rev_by_countries / total_revenue


# In[21]:


def plot_bar(df, xlabel, ylabel, title, color=COLORS[0], figsize=(20, 10), rotation=45):
    plot = df.plot(kind='bar', color=color, figsize=figsize)
    plot.set_xlabel(xlabel, fontsize=11)
    plot.set_ylabel(ylabel, fontsize=11)
    plot.set_title(title, fontsize=13)
    plot.set_xticklabels(labels=df.index, rotation=rotation)
                   
plot_bar(rev_by_countries, 'Country', 'Revenue', 'Revenue by Country')


# In[22]:


retail['InvoiceDate'].sort_values(ascending=False)


# In[23]:


def extract_month(date):
    month = str(date.month)
    if date.month < 10:
        month = '0' + month
    return str(date.year) + month 


# In[24]:


rev_by_month = retail.set_index('InvoiceDate').groupby(extract_month).sum()['CheckoutPrice']
rev_by_month

plot_bar(rev_by_month, 'Month', 'Revenue', 'Revenue by Month')


# In[25]:


rev_by_dow = retail.set_index('InvoiceDate').groupby(lambda date:date.dayofweek).sum()['CheckoutPrice']
rev_by_dow


# In[26]:


DAY_OF_WEEK = np.array(['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun'])
rev_by_dow.index = DAY_OF_WEEK[rev_by_dow.index]
plot_bar(rev_by_dow, 'DOW', 'Revenue', 'Revenue by DOW')


# In[27]:


rev_by_hour = retail.set_index('InvoiceDate').groupby(lambda date:date.hour).sum()['CheckoutPrice']
plot_bar(rev_by_hour, 'hour', 'revenue', 'revenue by hour')


# In[28]:


top_selling = retail.groupby('StockCode').sum()['Quantity'].sort_values(ascending=False)[:3]
top_selling


# In[29]:


top_revenue = retail.groupby('StockCode').sum()['CheckoutPrice'].sort_values(ascending=False)[:10]
top_revenue


# In[30]:


monthly_top3 = retail.set_index('InvoiceDate').groupby(['StockCode', extract_month]).sum()[['Quantity', 'CheckoutPrice']].loc[top_selling.index]


# In[31]:


plot_bar(monthly_top3['CheckoutPrice'], 'Product/Month', 'Revenue', 'Revenue of top 3 items')


# In[32]:


from datetime import datetime
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

get_ipython().run_line_magic('matplotlib', 'inline')


# In[33]:


dtypes = {
    'UnitPrice': np.float32,
    'CustomerID': np.int32,
    'Quantity': np.int32
}
retail = pd.read_csv('./OnlineRetailClean.csv', dtype=dtypes)
retail['InvoiceDate'] = pd.to_datetime(retail['InvoiceDate'], infer_datetime_format=True)
retail.head()


# In[34]:


retail.groupby('CustomerID').count()['Quantity'].sort_values(ascending=False)


# In[35]:


retail.groupby('CustomerID').sum()['CheckoutPrice'].sort_values(ascending=False)


# In[36]:


def get_month_as_datetime(date):
    return datetime(date.year, date.month, 1)

retail['Month'] = retail['InvoiceDate'].apply(get_month_as_datetime)

retail.head()


# In[37]:


month_group = retail.groupby('CustomerID')['Month']
retail['MonthStarted'] = month_group.transform(np.min)

retail.tail()


# In[38]:


retail['MonthPassed'] = (retail['Month'].dt.year - retail['MonthStarted'].dt.year) * 12 +     (retail['Month'].dt.month - retail['MonthStarted'].dt.month)


# In[39]:


retail.tail()


# In[40]:


def get_unique_no(x):
    return len(np.unique(x))

cohort_group = retail.groupby(['MonthStarted', 'MonthPassed'])
cohort_df = cohort_group['CustomerID'].apply(get_unique_no).reset_index()
cohort_df.head()


# In[41]:


cohort_df = cohort_df.pivot(index='MonthStarted', columns='MonthPassed')
cohort_df.head()


# In[42]:


customer_cohort = cohort_df.div(cohort_df.iloc[:, 0], axis=0) * 100
customer_cohort = customer_cohort.round(decimals=2)

customer_cohort


# In[43]:


xticks = np.arange(0, 13)
yticks = ['2010/12', '2011/01', '2011/02', '2011/03', '2011/04', '2011/05', '2011/06', '2011/07', '2011/08', '2011/09', '2011/10', '2011/11', '2011/12']

plt.figure(figsize = (15, 8))
sns.heatmap(customer_cohort, 
            annot=True, 
            xticklabels=xticks,
            yticklabels=yticks, 
            fmt='.1f')


# In[44]:


import numpy as np
import pandas as pd
# seaborn
import seaborn as sns
COLORS = sns.color_palette()

get_ipython().run_line_magic('matplotlib', 'inline')


# In[45]:


def plot_bar(df, xlabel, ylabel, title, figsize=(20, 10), color=COLORS[-1], rotation=45):
    plot = df.plot(kind='bar', color=color, figsize=figsize)
    plot.set_xlabel(xlabel, fontsize=10)
    plot.set_ylabel(ylabel, fontsize=10)
    plot.set_title(title, fontsize=12)
    plot.set_xticklabels(labels=df.index, rotation=rotation)


# In[46]:


dtypes = {
    'UnitPrice': np.float32,
    'CustomerID': np.int32,
    'Quantity': np.int32
}
retail = pd.read_csv('./OnlineRetailClean.csv', dtype=dtypes)
retail['InvoiceDate'] = pd.to_datetime(retail['InvoiceDate'], infer_datetime_format=True)
retail.head()


# In[47]:


order_by_hour = retail.set_index('InvoiceDate').groupby(lambda date: date.hour).count()['CustomerID']
order_by_hour


# In[48]:


plot_bar(order_by_hour, 'hour', '# orders', 'Order by hour')


# In[49]:


def half_an_hour(date):
    minute = ':00'
    if date.minute > 30:
        minute = ':30'
    hour = str(date.hour)
    if date.hour < 10:
        hour = '0' + hour
    
    return hour + minute


# In[50]:


order_by_hour_half = retail.set_index('InvoiceDate').groupby(half_an_hour).count()['CustomerID']
order_by_hour_half


# In[51]:


order_by_hour_half / order_by_hour_half.sum()


# In[52]:


plot_bar(order_by_hour_half, 'half an hour', '# orders', 'order by half an hour')


# In[53]:


order_count_by_hour = retail.set_index('InvoiceDate').groupby(['CustomerID', lambda date: date.hour]).count()['StockCode']
order_count_by_hour


# In[54]:


idx = order_count_by_hour.groupby('CustomerID').idxmax()


# In[55]:


result = order_count_by_hour.loc[idx]
result


# In[56]:


result.reset_index().groupby('level_1').groups


# In[58]:


import pandas as pd
import numpy as np


# In[ ]:




