import draw_gauge
import draw_spider_graph
import streamlit as st
import draw_bar_chart

class Gauge_Graph_type:
    def __init__(self,anigma_type, name, value):
        if anigma_type=="ici":
            self.name = name
            self.name = "מיקוד שליטה פנימי"
            self.value = value
            self.global_average = st.session_state.global_average["ici"]
            self.research_average = st.session_state.research_average["ici"]
        elif anigma_type=="risc":
            self.name = name
            self.name = "חוסן"
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
        
    def get_fig_mobile(self):
        # קריאה לפונקציה המותאמת למובייל עם אותם פרמטרים
        fig = draw_spider_graph.draw_spider_graph_mobile(self.name, self.school_info_current, self.school_info_global, self.school_info_research)
        return fig
        
        
class Bar_Chart_Graph_type:
    def __init__(self,name,anigma_type,*args):
        self.name = name
        self.anigma_type = anigma_type
        self.reserch_average = st.session_state.research_average[anigma_type]
        self.global_average = st.session_state.global_average[anigma_type]
        self.dicts = self.create_list_of_dicts(*args)
        
    def create_list_of_dicts(self,*args):
        data_list = []
    
        # נוודא שהארגומנטים מגיעים בזוגות (שם, ערך)
        if len(args) % 2 != 0:
            raise ValueError("Arguments must be in pairs: (key1, value1, key2, value2, ...)")
    
        # ריצה על כל שני איברים (שם וערך)
        for i in range(0, len(args), 2):
            value = args[i][self.anigma_type]
            name = args[i + 1]
            data_list.append({"name":name,"value": value})  # יצירת מילון והכנסה לרשימה
    
        return data_list
    
    def make_fig(self):
        #reserarch shoil be first
        fig=draw_bar_chart.draw_bar_chart(self.name, self.dicts, self.reserch_average, "ממוצע מחקרי", self.global_average, "ממוצע ארצי")
        return fig