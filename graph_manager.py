import draw_gauge
import draw_spider_graph
import streamlit as st

class Gauge_Graph_type:
    def __init__(self,anigma_type, name, value):
        if anigma_type=="ici":
            self.name = "ICI"
            self.name = name
            self.value = value
            self.global_average = st.session_state.global_average["ici"]
            self.research_average = st.session_state.research_average["ici"]
        elif anigma_type=="risc":
            self.name = "RISC"
            self.name = name
            self.value = value
            self.global_average = st.session_state.global_average["risc"]
            self.research_average = st.session_state.research_average["risc"]
        else:
            return "anigma type not found"
        

    def get_fig(self):
        fig=draw_gauge.draw_graph_gauge(self.name,self.value, self.global_average, self.research_average)
        return fig
        
        
class Spider_Graph_type:
    def __init__(self, name, current_averages):
        self.name = name
        self.school_info_current = current_averages
        self.school_info_global = st.session_state.global_average
        self.school_info_research = st.session_state.research_average
        
    def get_fig(self):
        fig= draw_spider_graph.draw_spider_graph(self.name, self.school_info_current, self.school_info_global, self.school_info_research)    
        return fig
        