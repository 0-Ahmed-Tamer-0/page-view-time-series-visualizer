import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df=pd.read_csv("fcc-forum-pageviews.csv")
df['date']=pd.to_datetime(df['date'])
df['YEAR']=df['date'].agg(lambda x:x.year)
df['MONTH']=df['date'].agg(lambda x:x.month)
df.sort_values(by=['value'],inplace=True)
# Clean data

clean_df=df
clean_df.drop((clean_df['value'].head((df['value'].size *2.5/100).__ceil__()).index),inplace=True)
clean_df.drop((clean_df['value'].tail(1+(df['value'].size *2.5/100).__ceil__()).index),inplace=True)

df.sort_values(by=['date'],inplace=True)

def draw_line_plot():
    # Draw line plot
    fig=plt.figure(figsize=(20,6))
    plt.plot(df['date'],df['value'],'r')
    plt.ylabel('Page Views')
    plt.xlabel('Date')
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    bar_df=clean_df

    bar_df['YEAR']=clean_df['date'].agg(lambda x:x.year)
    bar_df['MONTH']=clean_df['date'].agg(lambda x:x.month)
    bar_df['MONTH_NAME']=clean_df['date'].agg(lambda x:x.month_name())

    # Draw bar plot
    fig=plt.figure(figsize=(8,8))
    hue_o=pd.Series(data=bar_df["MONTH_NAME"].unique(),index=bar_df['MONTH'].unique()).sort_index()
    sns.barplot(data=bar_df,x='YEAR',y='value',hue='MONTH_NAME',hue_order=hue_o,ci=False,palette='bright',width=0.5)
    plt.xlabel('Years')
    plt.ylabel("Average Page Views")
    plt.legend(title='Months')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    bar_df=df
    bar_df['YEAR']=df['date'].agg(lambda x:x.year)
    bar_df['MONTH']=df['date'].agg(lambda x:x.month)
    bar_df['MONTH_NAME']=df['date'].agg(lambda x:x.month_name())
    
    # Draw box plots (using Seaborn)
    fig ,axes=plt.subplots(1,2,figsize=(30,9))
    sns.boxplot(data=bar_df,x='YEAR',y='value',hue='YEAR',palette='bright',legend=False,ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    hue_o=pd.Series(data=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],index=np.arange(1,13))
    sns.boxplot(data=bar_df, x='MONTH', y='value', hue='MONTH', palette='bright', legend=False, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")
    axes[1].set_xticks(hue_o.index)
    axes[1].set_xticklabels(hue_o.values)


    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
