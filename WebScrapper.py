import requests
from bs4 import BeautifulSoup
import pandas as pd
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np

def _generateRealTimeData(data,d):
    for ele in d:
        o = ele.find_all('td',{"align":'left'})
        c = ele.find('td',{"align":'right'}).find('a')
        data['Organisation Name'].append(o[1].text.strip())
        data['Tender Count'].append(int(c.text))
        data['Link'].append('https://etenders.gov.in'+c.get('href'))

def getData(url):
    r = requests.get(url)
    web_content = BeautifulSoup(r.text,'html.parser')
    web_content = web_content.find('table',{'id':"table"})
    data = defaultdict(list)
    even = web_content.find_all('tr',{'class':"even"})
    _generateRealTimeData(data,even)
    odd = web_content.find_all('tr',{'class':"odd"})
    _generateRealTimeData(data,odd)

    return dict(data)

def convertToCsv(data):
    df = pd.DataFrame(data,columns=['Organisation Name','Tender Count','Link'])
    df.to_csv("./csvFile.csv")

def _labels(x,y):
    for i in range(len(x)):
        plt.text(i,y[i],y[i],va="baseline",color="maroon")

def plotdata():
    df=pd.read_csv("./csvFile.csv")
    style.use('Solarize_Light2')
    y = df.iloc[:,2].values
    s = df.iloc[:,1].values
    x = list(range(1,len(y)+1))
    colors = np.random.randint(1,5,size=len(x))
    norm = plt.Normalize(1,4)
    cmap = plt.cm.rainbow

    fig, ax = plt.subplots()
    scatter = plt.scatter(
        x=x, 
        y=y, 
        c=colors,
        s = 100,
        cmap=cmap,
        norm=norm,  
        marker="h",
        )
    _labels(x, y)

    annot = ax.annotate(
        text="", 
        xy=(0,0), 
        xytext=(-300,-120),
        textcoords="offset points", 
        bbox= {'boxstyle':'round','fc':'w'},
    )
    annot.set_visible(False)

    def on_hover(event):
        annot_visibility = annot.get_visible()
        if(event.inaxes==ax):
            is_contained, annot_index = scatter.contains(event)
            if(is_contained):
                data_point_location = scatter.get_offsets()[annot_index['ind'][0]]
                text_label = s[int(data_point_location[0])]
                annot.set_text(text_label)
                annot.set_color('c')
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if(annot_visibility):
                    annot.set_visible(False)
                    fig.canvas.draw_idle()

    fig.canvas.mpl_connect('motion_notify_event',on_hover)

    plt.xlabel("NAMES OF ORGANIZATIONS")
    plt.ylabel("COUNT OF TENDERS")
    plt.title('TENDER COUNT VS DIFFERENT ORGANIZATIONS')
    ax.invert_xaxis()
    ax.invert_yaxis()
    ax.tick_params(axis='x', colors='maroon')
    ax.tick_params(axis='y', colors='m')
    plt.show()
    


url = ('https://etenders.gov.in/eprocure/app?page=FrontEndTendersByOrganisation&service=page')
data = getData(url)
convertToCsv(data)
plotdata()
