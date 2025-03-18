import pandas as pd
def return_var_from_df(df):
  return df.values.flatten().var(ddof=1)

def return_mean_from_df(df):
  return df.values.flatten().mean()

def return_mean_and_var_from_df(df):
    #return return_mean_from_df(df), return_var_from_df(df)
    return {"mean": return_mean_from_df(df), "var":  return_var_from_df(df)}
 
 
def return_sum_dict(df):
    return df.mean().to_dict()   
  
  