import pandas as pd
import anigmas
import draw_gauge
import plotly
from graph_manager import Gauge_Graph_type, Spider_Graph_type                     

class SchoolInfo:
  def __init__(self,df):
    self.df = df
    self.ici=anigmas.ici_result(df)
    self.risc=anigmas.risc_result(df)   
    self.future_negetive_past=anigmas.future_negetive_past_result(df)
    self.future_positive_past=anigmas.future_positive_past_result(df)
    self.future_fatalic_present=anigmas.future_fatalic_present_result(df)
    self.future_hedonistic_present=anigmas.future_hedonistic_present_result(df)
    self.future_future=anigmas.future_future_result(df)
    
  
#   def __ici_result_mean(self):
#       return float(anigmas.ici_result(self.df))
#   def __risc_result_mean(self):
#       return float(anigmas.risc_result(self.df))
#   def __future_negetive_past_result_mean(self):
#       return float(anigmas.future_negetive_past_result(self.df))
#   def __future_positive_past_result_mean(self):
#         return float(anigmas.future_positive_past_result(self.df))
#   def __future_fatalic_present_result_mean(self):
#         return float(anigmas.future_fatalic_present_result(self.df))
#   def __future_hedonistic_present_result_mean(self):
#         return float(anigmas.future_hedonistic_present_result(self.df))
#   def __future_future_result_mean(self):
#         return float(anigmas.future_future_result(self.df))
  
  def return_anigmas_result_as_dict(self):
        result= {
            "ici":self.ici,
            "risc":self.risc,
            "future_negetive_past":self.future_negetive_past,
            "future_positive_past":self.future_positive_past,
            "future_fatalic_present":self.future_fatalic_present,
            "future_hedonistic_present":self.future_hedonistic_present,
            "future_future":self.future_future
        }
        # result= {
        #     "ici":self.__ici_result_mean(),
        #     "risc":self.__risc_result_mean(),
        #     "future_negetive_past":self.__future_negetive_past_result_mean(),
        #     "future_positive_past":self.__future_positive_past_result_mean(),
        #     "future_fatalic_present":self.__future_fatalic_present_result_mean(),
        #     "future_hedonistic_present":self.__future_hedonistic_present_result_mean(),
        #     "future_future":self.__future_future_result_mean()
        # }
        return result

    
  
  def get_fig_ici(self,name):
      graph=Gauge_Graph_type("ici",name,self.ici)
      fig=graph.get_fig()
      return fig

      
  def get_fig_risc(self,name):
      graph=Gauge_Graph_type("risc",name,self.risc)
      fig=graph.get_fig()
      return fig
  
  def get_fig_spider(self):
      graph=Spider_Graph_type("spider",self.return_anigmas_result_as_dict())
      fig=graph.get_fig()
      return fig
  
    
    
    