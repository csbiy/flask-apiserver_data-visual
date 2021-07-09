from flask import Flask , request ,make_response ,send_file
from flask_cors import CORS
import matplotlib.pyplot as plt
import pandas as pd
from plotnine import *
import sys, base64
app = Flask(__name__);
CORS(app);

@app.route("/",methods=["GET"])
def testRouter():
    print("request")
    return "hello";
@app.route("/",methods = ["POST"])
def dataProcess():
    tgiData = request.json;
    df = pd.DataFrame(columns=["group","time","tumorSize"]);
    for k,v in tgiData.items():
        tumorSize = map(lambda x : x[1] ,v["data"])
        day = map(lambda x : x[0] ,v["data"])
        df = pd.concat([df,pd.DataFrame({
            "group":k,
            "time":day,
            "tumorSize":tumorSize,
        })],axis=0)
    df = df.astype({"group":"string","time":"int64"});
    p = ggplot(df, aes(x="time", y="tumorSize",color="group")) + geom_smooth() + ylab("Tumor Size(mm^3)") + xlab("Days after inoculation") + ggtitle("Standard Growth Curve") + facet_wrap('~group') 
    ggplot.save(p,filename="standard.png",path=".")
    with open("standard.png","rb") as standardImg:
        encodedImg = base64.b64encode(standardImg.read())
        return encodedImg;c

if __name__ == "__main__":
    print("server executed!!"); 
    app.run( host="172.25.113.131" , port = 5500 ,debug=True )
