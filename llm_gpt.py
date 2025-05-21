from openai import OpenAI
client = OpenAI()
import pandas
import llms

system_prompt_ex="""
### 📝 **Provide a Comprehensive Feedback Based on Zimbardo Time Perspective Test Results**

#### **Context:**  
The following table contains test results from the **Zimbardo Time Perspective Test** conducted in a school. Each row represents a specific time perspective metric, along with its **mean score** and **variance**.

#### **Data Table Format:**
(The data will be given as a user prompt)

#### **Instructions:**  
🔹 **Analyze** each metric based on its **mean and variance**.  
🔹 Provide **insights** on students' tendencies and potential **psychological implications**.  
🔹 Highlight **areas of strength** and **areas that need improvement**.  
🔹 Offer **actionable recommendations** for school administrators to improve student time perspective balance.  

#### **Output Format:**  
Your response should be structured as follows:

1️⃣ **General Overview** – Provide a brief introduction summarizing the results.  
2️⃣ **Metric-by-Metric Analysis** – Analyze each time perspective individually, focusing on its mean and variance.  
3️⃣ **Key Takeaways** – Summarize the most important insights.  
4️⃣ **Recommendations** – Provide concrete steps for improvement.  

Use **professional and structured language** while keeping the feedback **clear and actionable**. 
you should provide an answer in Hebrew. 
"""

def return_llm_answer(user_prompt):
    return llms.get_openai_response(user_prompt, system_prompt_ex, [], {}, stream=False)

def return_llm_answer(prompt, system, history):
    user_prompt = f"history:{history} + current promt:{prompt}"
    return llms.get_openai_response(user_prompt, system, [], {}, stream=False)

