import pandas as pd
import anigmas
import draw_gauge
import plotly
from graph_manager import Gauge_Graph_type, Spider_Graph_type   
import streamlit as st                  

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
    
    
    # self.ici_delta_from_global=self.get_precentage_diffrent_from_global_anigmas("ici")
    # self.risc_delta_from_global=self.get_precentage_diffrent_from_global_anigmas("risc")
    # self.future_negetive_past_delta_from_global=self.get_precentage_diffrent_from_global_anigmas("future_negetive_past")
    # self.future_positive_past_delta_from_global=self.get_precentage_diffrent_from_global_anigmas("future_positive_past")
    # self.future_fatalic_present_delta_from_global=self.get_precentage_diffrent_from_global_anigmas("future_fatalic_present")
    # self.future_hedonistic_present_delta_from_global=self.get_precentage_diffrent_from_global_anigmas("future_hedonistic_present")
    # self.future_future_delta_from_global=self.get_precentage_diffrent_from_global_anigmas("future_future")
    
    
    
  
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
        return result
    
  def return_delta_from_global_as_dict(self):
        result= {
            "ici":self.get_precentage_diffrent_from_global_anigmas("ici"),
            "risc":self.get_precentage_diffrent_from_global_anigmas("risc"),
            "future_negetive_past":self.get_precentage_diffrent_from_global_anigmas("future_negetive_past"),
            "future_positive_past":self.get_precentage_diffrent_from_global_anigmas("future_positive_past"),
            "future_fatalic_present":self.get_precentage_diffrent_from_global_anigmas("future_fatalic_present"),
            "future_hedonistic_present":self.get_precentage_diffrent_from_global_anigmas("future_hedonistic_present"),
            "future_future":self.get_precentage_diffrent_from_global_anigmas("future_future")
        }
        return result
  
  def return_biggest_delata_from_global(self):
        delta_dict=self.return_delta_from_global_as_dict()
        max_key = max(delta_dict, key=lambda k: abs(delta_dict[k]))
        return max_key

  def print_anigma_result(self):
        anigma_max_abs=self.return_biggest_delata_from_global()
        anigmas.get_max_average_higed_from_anigma(self.df,anigma_max_abs)
        
        

    
  
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
  
  def get_precentage_diffrent_from_global_anigmas(self,anigma_name):
        global_anigmas=st.session_state.global_average
        return((self.return_anigmas_result_as_dict()[anigma_name]-global_anigmas[anigma_name])/global_anigmas[anigma_name])
        
    
    
    