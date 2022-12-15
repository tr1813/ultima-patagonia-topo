from dataclasses import dataclass, field
import matplotlib.pyplot as plt
from salem import GoogleVisibleMap, Map, transform_geopandas
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, MultiPoint

from helpers.geo import coordinatePairUTM
from helpers.cadaster import CaveCadaster,Cave, Expedition

@dataclass
class SatelliteMapPlot:
      # Configure image aspect
    size_x : int
    size_y : int
    dpi : int
    scale : float = 0.013988764
    points : list[coordinatePairUTM] = field(init = False) 
    point_names : list[str] = field(init=False)
    new_x : float = field(init = False) 
    new_y : float = field(init=False)

    def add_points(self, cadaster : CaveCadaster) -> None:
        self.points = [cave.coordinates for cave in cadaster.caves]
        self.point_names = [cave.name for cave in cadaster.caves]

    def add_point_to_plot(self, x: float, y: float) -> None:
        self.new_x = x
        self.new_y = y

    def plot_map(self):
        # Get the Google Static image
        g = GoogleVisibleMap(y=[self.new_y-0.64*self.scale, self.new_y+0.64*self.scale], x=[self.new_x-1.5*self.scale, self.new_x+1.5*self.scale],
                     scale=2,  # scale is for more details
                     maptype='satellite',
                     size_x=self.size_x, size_y=self.size_y
                    )

        # the google static image is a standard rgb image
        ggl_img = g.get_vardata()

        sm = Map(g.grid, nx=self.size_x, factor=1)

        sm.set_rgb(ggl_img)  # add the background rgb image

        # prepare the figure
        fig, ax  = plt.subplots(figsize=(self.size_x/self.dpi,self.size_y/self.dpi), dpi=self.dpi)

        # plot 1
        x, y = sm.grid.transform([self.new_x],[self.new_y])
        xi, yi = sm.grid.transform([p._orig_long for p in self.points],[p._orig_lat for p in self.points])
        ax.scatter(x, y, zorder= 100, s=5,color="blue", marker = "d") # type:ignore
        ax.scatter(xi, yi, zorder= 100, s=3,color="red", marker = "d") # type:ignore
        for name,x,y in zip(self.point_names,xi,yi):
            ax.text(x+.0001,y+.0001,name,fontsize=5,color = "red")

        sm.plot(ax=ax)
        fig.patch.set_facecolor('black') # type:ignore
        return fig,ax




