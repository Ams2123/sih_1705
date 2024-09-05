import fiona
import geopandas as gpd 
import matplotlib.pyplot as plt

class village_info:

    def __init__(self,path,vname):
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

    def pic_gen(self,lname):
        self.pic_layer = gpd.read_file(self.gdp_path,layer=lname)
        self.pic_layer.plot()
        plt.savefig(f'{self.vname}_{lname}.jpeg')
        return f'{self.vname}_{lname}.jpeg'

    def pic_gen_multiple(self, layer_names):
        fig, ax = plt.subplots(figsize=(12, 12)) 
        
        for lname in layer_names:
            layer = gpd.read_file(self.gdp_path, layer=lname)
            layer.plot(ax=ax, label=lname,figsize=(12,12))
        
        ax.legend()
        combined_filename = f'{self.vname}_combined_layers.jpeg'
        plt.savefig(combined_filename)
        plt.close() 
        
        return combined_filename

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

