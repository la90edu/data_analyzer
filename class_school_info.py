import pandas as pd
import anigmas
import draw_gauge
import plotly
from graph_manager import Gauge_Graph_type, Spider_Graph_type   
import streamlit as st   
import texts               

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

    self.worst_anigma=self.return_biggest_delata_from_global_positive_wrost_anigma()[0]
    self.worst_anigma_value=self.return_biggest_delata_from_global_positive_wrost_anigma()[1]
    self.worst_anigma_name=texts.return_translate_anigma_name(self,self.worst_anigma)
    self.best_anigma=self.return_biggest_delata_from_global_negetive_best_anigma()[0]
    self.best_anigma_value=self.return_biggest_delata_from_global_negetive_best_anigma()[1]
    self.best_anigma_name=texts.return_translate_anigma_name(self,self.best_anigma)
    
    
  
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
  
  def return_biggest_delata_from_global_positive_wrost_anigma(self): # when global is bigger than local
        delta_dict=self.return_delta_from_global_as_dict()
        positive_delta_dict = {key: value for key, value in delta_dict.items() if value > 0}

        #finds the max key from the positive delta dict
        max_key = max(positive_delta_dict, key=positive_delta_dict.get)
        max_value = positive_delta_dict[max_key]
        
        return max_key,max_value
    
  def return_biggest_delata_from_global_negetive_best_anigma(self): # when local is bigger than global
        delta_dict=self.return_delta_from_global_as_dict()
        negetive_delta_dict = {key: value for key, value in delta_dict.items() if value < 0}
        
        min_key = min(negetive_delta_dict, key=negetive_delta_dict.get)
        min_value = negetive_delta_dict[min_key]
        
        return min_key,min_value

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
        
        local=self.return_anigmas_result_as_dict()[anigma_name]
        global_=global_anigmas[anigma_name]
        
        delta=(global_-local)/global_
        
        return delta
        # return((self.return_anigmas_result_as_dict()[anigma_name]-global_anigmas[anigma_name])/global_anigmas[anigma_name])
        
  
  def return_worst_heg_according_to_wrost_anigma(self):
        worst_heg=anigmas.return_wrost_heg_from_anigma_acoording_to_delta_from_global(self.df,self.worst_anigma) 
        return worst_heg

  def return_first_and_second_worst_heg_according_to_wrost_anigma(self):
        key1,value1,key2,value2=anigmas.return_first_and_second_heg_for_worst_heg(self.df,self.worst_anigma)
        key1_name=texts.return_translate_heg_name(key1)
        key2_name=texts.return_translate_heg_name(key2) 
        
        return key1_name,value1,key2_name,value2
        
