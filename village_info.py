import fiona
import geopandas as gpd 
import plotly.graph_objects as go
import matplotlib.pyplot as plt

class village_map_gen:

    def __init__(self,path,vname="State"):
        self.gdp_path = path
        self.layers = fiona.listlayers(self.gdp_path)
        self.vname = vname
    
    def house_info(self,lname):
        self.house = gpd.read_file(self.gdp_path,layer=lname)
        self.house['area'] = self.house['geometry'].area
        self.area = self.house['area'].sum()
        self.count = len(self.house)
        self.avg = self.area/self.count
        return self.count , self.area , self.avg
    
    def road_info(self,lname):
        self.road = gpd.read_file(self.gdp_path,layer=lname)
        self.road['length'] = self.road['geometry'].length
        return self.road['length'].sum()/1000

    def layers_available(self):
        return self.layers

    def graph_gen(self,lname):
        traces = self.trace_gen(lname)
        fig = go.Figure(data=traces,)
        fig.update_layout(title="Map",xaxis_title = "Longitude",yaxis_title = "Latitude",width = 600,height = 600)
        return fig

    def graph_gen_multiple(self, layer_names):
        traces = []
        for i in layer_names:
            print(i)
            traces += self.trace_gen(i)
        fig = go.Figure(data=traces,)
        fig.update_layout(title="Map",xaxis_title = "Longitude",yaxis_title = "Latitude",width = 600,height = 600)
        return fig
    
    def color(self,lname):
        self.colour_code = {"area":"rgba(206,114,60,100)","road":"rgba(255,255,255,80)","water":"rgba(124,220,254,100)",\
                       "railway":"rgba(255, 215,0,100)","other":"rgba(78,201,176,100)"}
        lname=lname.split("_")
        for i in lname : 
            try:
                return self.colour_code[i.lower()]
            except KeyError:
                continue
        return self.colour_code["other"]
    
    def trace_gen(self,lname):
        self.layer = gpd.read_file(self.gdp_path,layer=lname)
        polygons = self.layer["geometry"] 
        traces = []
        for geom in polygons:
            if geom.is_empty:
                continue
            if geom.geom_type == "Polygon":
                x,y = geom.exterior.xy
                x,y = list(x)[-1],list(y)[-1]
                traces.append(go.Scatter(x=x,y=y,mode="lines+fill",fill="toself",\
                                         line=dict(width=0.1),fillcolor=self.color(lname),
                                         showlegend=False))
            else :
                for polygon in geom.geoms:
                    x,y = polygon.exterior.xy
                    x,y = list(x),list(y)
                    traces.append(go.Scatter(x=x,y=y,mode="lines",fill="toself",\
                                         line=dict(width=0.1),fillcolor=self.color(lname),\
                                         showlegend = False))
        return traces
        
class property_tax:
    
    def __init__(self,tax_rate_per_sqm=None,capital_value_rate=None,rental_value_rate=None):
        self.tax_rate_per_sqm = tax_rate_per_sqm
        self.capital_value_rate = capital_value_rate
        self.rental_value_rate = rental_value_rate
    
    def uav_system(self, area):
        return area * self.tax_rate_per_sqm
    
    def cvs_system(self, capital_value):
        return capital_value * self.capital_value_rate
    
    def arv_system(self, rental_value):
        return rental_value * self.rental_value_rate

