from flask import Flask , request ,make_response ,send_file
from flask_cors import CORS
import matplotlib.pyplot as plt
import pandas as pd
from pandas import Categorical
from plotnine import *
import sys, base64
app = Flask(__name__);
CORS(app);

@app.route("/",methods = ["POST"])
def dataProcess():
    tgiData = request.json['data'];
    colorSet = request.json['colorSet'];
    groupSet = request.json['groupSet'];

    df = pd.DataFrame(columns=["group","time","tumorSize"]);
    for k,v in tgiData.items():
        tumorSize = map(lambda x : x[1] ,v["data"])
        day = map(lambda x : x[0] ,v["data"])
        df = pd.concat([df,pd.DataFrame({
            "group":k,
            "time":day,
            "tumorSize":tumorSize,
        })],axis=0)
    df = df.astype({"group":"category","time":"int64"});
    df['group'].cat.reorder_categories(groupSet,inplace=True);
    p = ggplot(df, aes(x="time", y="tumorSize",color="group",group="group")) + geom_smooth(method="lowess") + ylab("Tumor Size(mm^3)") + xlab("Days after inoculation") + facet_wrap('~group')  +  scale_color_manual(values =  colorSet) + theme(figure_size=(12, 7));
    ## data visulization plot 
    ggplot.save(p,filename="./cache/standard.png",dpi=300,path=".",limitsize=True) 
    with open("./cache/Standard.png","rb") as standardImg:
        encodedImg = base64.b64encode(standardImg.read())
        return encodedImg;
    
if __name__ == "__main__":
    app.run( host="172.25.113.131" , port = 5500)
