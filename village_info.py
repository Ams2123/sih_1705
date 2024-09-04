import fiona
import geopandas as gpd 
import matplotlib.pyplot as plt

class village_info:

    def __init__(self,path,vname):
        self.gdp_path = path
        self.layers = fiona.listlayers(self.gdb_path)
        self.vname = vname
    
    def house_info(self,lname):
        self.house = gpd.read_file(self.gdb_path,layer=lname)
        self.house['area'] = self.house['geometry'].area()
        self.area = self.house['area'].sum()
        self.count = len(self.house)
        self.avg = self.area/self.count
        return self.count , self.area , self.avg
    
    def road_info(self,lname):
        self.road = gpd.read_file(self.gdb_path,layer=lname)
        self.road['length'] = self.road['geometry'].length
        return self.road['length'].sum()/1000

    def layers_available(self):
        return self.layers

    def pic_gen(self,lname):
        self.pic_layer = gpd.read_file(self.gdp_path,layer=self.lname)
        self.pic_layer.plot()
        plt.savefig(f'{self.vname}_{lname}.jpeg')
        return f'{self.vname}_{lname}.jpeg'
