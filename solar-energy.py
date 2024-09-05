import geopandas as gpd
import pvlib
import pandas as pd
import fiona

class SolarEnergyCalculator:
    def __init__(self, path, vname):
        self.gdb_path = path
        self.vname = vname
        self.layers = fiona.listlayers(self.gdb_path)

    def _get_location(self):
        if 'gujarat' in self.vname.lower():
            return pvlib.location.Location(latitude=22.2587, longitude=71.1924)  # Gujarat
        elif 'gautam' in self.vname.lower() or 'buddh' in self.vname.lower():
            return pvlib.location.Location(latitude=28.4595, longitude=77.0266)  # Gautam Buddh Nagar, UP
        elif 'chhattisgarh' in self.vname.lower():
            return pvlib.location.Location(latitude=21.2787, longitude=81.8661)  # Chhattisgarh
        else:
            raise ValueError("Unknown location. Please provide a file name that includes 'gujarat', 'gautam', or 'chhattisgarh'.")

    def calculate_solar_energy(self, tilt_angle=30, surface_azimuth=180, panel_efficiency=0.18):
        # Load .gdb file to access built-up area polygons
        buildings_layer = "Built_Up_Area_type"  # Replace with the correct layer name from the list
        buildings = gpd.read_file(self.gdb_path, layer=buildings_layer)
        buildings['area_sqm'] = buildings['geometry'].area

        # Get the location based on the file name
        location = self._get_location()

        # Get solar position data
        times = pd.date_range('2024-01-01', '2024-12-31', freq='h', tz=location.tz)  # 1 year of hourly data
        solar_position = location.get_solarposition(times)

        # Calculate solar irradiance on a tilted surface
        irradiance = pvlib.irradiance.get_total_irradiance(
            surface_tilt=tilt_angle,
            surface_azimuth=surface_azimuth,
            dni=solar_position['apparent_zenith'],  # Direct normal irradiance
            ghi=solar_position['apparent_elevation'],  # Global horizontal irradiance
            dhi=solar_position['apparent_zenith'],  # Diffuse horizontal irradiance
            solar_zenith=solar_position['apparent_zenith'],
            solar_azimuth=solar_position['azimuth']
        )

        buildings['solar_energy_kwh'] = buildings['area_sqm'] * irradiance['poa_global'].mean() * panel_efficiency

        total_energy = buildings['solar_energy_kwh'].sum()
        print(f"Total solar energy potential (kWh): {total_energy}")
        print(buildings[['area_sqm', 'solar_energy_kwh']].head())

        # Save the results to a new GeoJSON file
        output_path = "solar_energy_potential.geojson"
        buildings.to_file(output_path, driver='GeoJSON')
