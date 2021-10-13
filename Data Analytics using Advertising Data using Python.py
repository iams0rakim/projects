#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


imp=10000
clk=100
conv=10
cost=100000


# In[3]:


# ctr (click through rate)
ctr = clk/imp*100


# In[4]:


ctr


# In[5]:


# cpm
cpm = cost/imp*1000


# In[6]:


cpm


# In[7]:


# cpc
cpc = cost/clk


# In[8]:


cpc


# In[9]:


# cpa
cpa = cost/conv


# In[10]:


cpa


# In[12]:


import matplotlib.pyplot as plt


# In[13]:


from pandas import DataFrame
from pandas import Series


# In[14]:


import matplotlib
from matplotlib import font_manager, rc
import platform


# In[15]:


try : 
    if platform.system() == 'Windows':
    # 윈도우인 경우
        font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
        rc('font', family=font_name)
    else:    
    # Mac 인 경우
        rc('font', family='AppleGothic')
except : 
    pass
matplotlib.rcParams['axes.unicode_minus'] = False   


# In[17]:


dict_data = {'철수': [1,2,3,4], '영희': [2,3,4,5], '민수': [3,4,5,6], '수진': [4,5,6,7]}
df=DataFrame(dict_data)


# In[18]:


df


# In[19]:


# 선그래프
df.plot()
plt.show()


# In[20]:


# 막대그래프
df.plot.bar()
plt.show()


# In[21]:


# 가로막대그래프
df.plot.barh()
plt.show()


# In[22]:


# 히스토그램
df.plot.hist()
plt.show()


# In[23]:


df.plot.hist(bins=range(1,9,1))
plt.show()


# In[25]:


df.plot.bar(figsize=[10,6])
plt.show()


# In[26]:


df.plot.bar(figsize=[10,6])
plt.title('예제')
plt.show()


# In[27]:


df.plot.bar(figsize=[10,6])
plt.title('예제', fontsize=18)
plt.show()


# In[28]:


df.plot.bar(figsize=[10,6])
plt.title('예제', fontsize=18)
plt.xlabel('xlabel', fontsize=16)
plt.ylabel('ylabel', fontsize=16)
plt.xticks([0,1,2],['첫째', '둘째', '셋째'],fontsize=10, rotation=0)
plt.yticks([1,3,5,7], ['첫째', '셋째', '다섯째', '일곱번째'])
plt.show()


# In[29]:


df=pd.read_excel('네이버보고서.xls')


# In[30]:


df.head()


# In[31]:


df=pd.read_excel('네이버보고서.xls', skiprows=[0])


# In[32]:


df.head()


# In[33]:


df.isnull()


# In[34]:


df.isnull().sum()


# In[37]:


clk=round(df['클릭수'],0)


# In[38]:


clk


# In[39]:


clk.astype(int)


# In[40]:


df['클릭수']=clk.astype(int) # 기존 칼럼데이터 대체


# In[41]:


df.head()


# In[44]:


df['클릭률(%)']=df['클릭수']/df['노출수']*100


# In[45]:


df.head()


# In[46]:


cpc=round(df['평균클릭비용(VAT포함,원)'],0)
df['평균클릭비용(VAT포함,원)']=cpc.astype(int)


# In[47]:


df.head()


# In[48]:


df.head(10)


# In[49]:


df.shape


# In[50]:


df.describe()


# In[51]:


pd.set_option('display.float_format', '{:2f}'.format)


# In[52]:


df.describe()


# In[54]:


df.columns


# In[56]:


len(df['광고그룹'].unique())


# In[57]:


type(df['노출수'])


# In[58]:


df['노출수'].plot()
plt.show()


# In[61]:


imp_sort=df['노출수'].sort_values()


# In[62]:


imp_sort


# In[63]:


imp_sort=imp_sort.reset_index()


# In[64]:


imp_sort


# In[65]:


imp_sort.drop('index', axis=1)


# In[66]:


imp_sort.drop('index', axis=1, inplace=True)


# In[67]:


imp_sort


# In[75]:


((df['클릭수'].sort_values()).reset_index()).drop('index',axis=1)


# In[73]:


(((df['클릭수'].sort_values()).reset_index()).drop('index',axis=1)).plot()
plt.show()


# In[76]:


(((df['총비용(VAT포함,원)'].sort_values()).reset_index()).drop('index',axis=1)).plot()
plt.show()


# In[77]:


imp=df['노출수']


# In[78]:


imp.quantile(0.95)


# In[79]:


imp=imp[imp>=imp.quantile(0.95)]


# In[80]:


imp


# In[81]:


df_index=df.set_index('키워드')


# In[82]:


df_index


# In[83]:


imp=df_index['노출수']


# In[84]:


imp=imp[imp>imp.quantile(0.95)]


# In[85]:


imp #노출수 상위 5% 키워드


# In[86]:


clk=df_index['클릭수']
clk=clk[clk>=clk.quantile(0.95)]


# In[87]:


clk #클릭수 상위 5% 키워드


# In[88]:


#df_index에서 imp,clk 변수 생성
imp=df_index['노출수']
clk=df_index['클릭수']


# In[91]:


#노출수와 클릭수 모두 상위5% 추출
result=df_index[(imp>=imp.quantile(0.95))&(clk>=clk.quantile(0.95))]


# In[92]:


result


# In[93]:


result.index


# #저효율키워드 선별

# In[94]:


cost=df_index['총비용(VAT포함,원)']


# In[97]:


result=df_index[(imp<imp.quantile(0.95))&(clk<clk.quantile(0.95))&(cost>=cost.quantile(0.85))&(cost<cost.quantile(0.95))]


# In[98]:


result.index


# In[99]:


grouped=df.groupby('광고그룹')


# In[100]:


grouped


# In[101]:


grouped.count()


# In[102]:


grouped.mean()


# In[103]:


grouped.std()


# In[104]:


grouped.var()


# In[105]:


grouped.sum()


# In[106]:


df_group=grouped.sum()


# In[107]:


df_group


# In[108]:


df_group['클릭률(%)']=df_group['클릭수']/df_group['노출수']


# In[110]:


df_group['평균클릭비용(VAT포함,원)']=df_group['총비용(VAT포함,원)']/df_group['클릭수']


# In[111]:


df_group[df_group['클릭수']==0]


# In[112]:


#fillna 함수 이용- 전달된 값으로 결측값 대체
df_group['평균클릭비용(VAT포함,원)']=df_group['평균클릭비용(VAT포함,원)'].fillna(0)


# In[113]:


#round함수를 통해서 반올림처리, 소수점 제거(astype-int)
df_group['평균클릭비용(VAT포함,원)']=round(df_group['평균클릭비용(VAT포함,원)'],0)
df_group['평균클릭비용(VAT포함,원)']=df_group['평균클릭비용(VAT포함,원)'].astype(int)


# In[114]:


df_group.head()


# In[115]:


#노출수 칼럼 선그래프
df_group['노출수'].plot()
plt.show()


# In[118]:


#노출수 칼럼 선그래프
#sort_values(),reset_index(),drop('index',axis=1),plot - 한줄 코딩(괄호사용)
(((df_group['노출수'].sort_values()).reset_index()).drop('광고그룹',axis=1)).plot()
plt.show()


# In[119]:


#클릭수 칼럼 선그래프
(((df_group['클릭수'].sort_values()).reset_index()).drop('광고그룹',axis=1)).plot()
plt.show()


# In[120]:


imp=df_group['노출수']
clk=df_group['클릭수']


# In[121]:


result=df_group[(imp>=imp.quantile(0.8))&(clk>=clk.quantile(0.9))]


# In[122]:


result.index


# In[123]:


cost=df_group['총비용(VAT포함,원)']


# In[124]:


#조건이 여러개일 경우 
#데이터프레임[(조건문)&(조건문)]
result=df_group[(imp<imp.quantile(0.8))&(clk<clk.quantile(0.9))&(cost>=cost.quantile(0.6))&(cost<cost.quantile(0.9))]


# In[125]:


result.index


# In[ ]:




