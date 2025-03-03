# from openai import OpenAI
# client = OpenAI()
# import pandas

# system_prompt="""
# ### 📝 **Provide a Comprehensive Feedback Based on Zimbardo Time Perspective Test Results**

# #### **Context:**  
# The following table contains test results from the **Zimbardo Time Perspective Test** conducted in a school. Each row represents a specific time perspective metric, along with its **mean score** and **variance**.

# #### **Data Table Format:**
# (The data will be given as a user prompt)

# #### **Instructions:**  
# 🔹 **Analyze** each metric based on its **mean and variance**.  
# 🔹 Provide **insights** on students' tendencies and potential **psychological implications**.  
# 🔹 Highlight **areas of strength** and **areas that need improvement**.  
# 🔹 Offer **actionable recommendations** for school administrators to improve student time perspective balance.  

# #### **Output Format:**  
# Your response should be structured as follows:

# 1️⃣ **General Overview** – Provide a brief introduction summarizing the results.  
# 2️⃣ **Metric-by-Metric Analysis** – Analyze each time perspective individually, focusing on its mean and variance.  
# 3️⃣ **Key Takeaways** – Summarize the most important insights.  
# 4️⃣ **Recommendations** – Provide concrete steps for improvement.  

# Use **professional and structured language** while keeping the feedback **clear and actionable**. 
# you should provide an answer in Hebrew. 
# """

# # def return_llm_answer(user_prompt):
# #     #system_prompt = system_prompt
# #     #user_prompt=user_prompt
 

# #     response = client.chat.completions.create(
# #         model="gpt-4o",
# #         messages=[
# #             {"role": "system", "content":  system_prompt},
# #             {"role":"user","content":user_prompt}
# #         ]
# #     )
# #     return response.choices[0].message.content

# def return_llm_answer(user_prompt_pandas_table):
#     user_prompt=user_prompt_pandas_table.to_markdown()
#     response = client.chat.completions.create(
#         model="gpt-4o",
#         messages=[
#             {"role": "system", "content": [{"type": "text", "text": system_prompt}]},
#             {"role": "user", "content": [{"type": "text", "text": user_prompt}]}
#         ]
#     )
#     return response.choices[0].message.content