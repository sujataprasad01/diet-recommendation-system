from flask import Flask, request, render_template
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
import re
import os

os.environ["OPENAI_API_KEY"]="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"
app=Flask(__name__)


llm_restro=OpenAI(temperature=0.5)

prompt_template_restro=PromptTemplate(
    input_variables=['age', 'gender', 'weight', 'height', 'veg_or_nonveg', 'disease', 'allergics', 'foodtype'],
    template="Diet Recommendation Syatem:\n"
             """I want you to recommend 6 restaurants names, 
             5 breakfast names(more on fruits), 
             6 dinner names, 
             and 6 workout names(morning walk and all),"""
             "based on the following criteria:\n"
             "Person age:{age}\n"
             "Person gender:{gender}\n"
             "Person height:{height}\m"
             "Person veg_or_nonveg:{veg_or_nonveg}\n"
             "Person generic disease:{disease}\n"
             "Person region:{region}\n"
             "Person allergics:{allergics}\n"
             "Person foodtype:{foodtype}."
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST', 'GET'])
def recommend():
    if request.method=='POST':
        age=request.form['age']
        gender=request.form['gender']
        weight=request.form['weight']
        height=request.form['height']
        veg_or_nonveg=request.form['veg_or_nonveg']
        disease=request.form['disease']
        region=request.form['region']
        allergics=request.form['allergics']
        foodtype=request.form['foodtype']


        # chain=LLMChain(llm=llm_restro, prompt=prompt_template_restro)          
        chain_restro=LLMChain(llm=llm_restro, prompt=prompt_template_restro)          
        input_data={
            'age':age,
            'gender':gender,
            'weight':weight,
            'height':height,
            'veg_or_nonveg':veg_or_nonveg,
            'disease':disease,
            'region':region,
            'allergics':allergics,
            'foodtype':foodtype
        }
        results=chain_restro.run(input_data)

        restaurant_names=re.findall(r"Restaurants:(.*?)Breakfast:", results, re.DOTALL)
        breakfast_names=re.findall(r"Breakfast:(.*?)Dinner:", results, re.DOTALL)
        dinner_names=re.findall(r"Dinner:(.*?)Workouts:", results, re.DOTALL)
        workout_names=re.findall(r"Workouts:(.*?)$", results, re.DOTALL)


        restaurant_names=[name.strip() for name in restaurant_names[0].strip().split('\n') if name.strip()] if restaurant_names else []
        breakfast_names=[name.strip() for name in breakfast_names[0].strip().split('\n') if name.strip()] if breakfast_names else []
        dinner_names=[name.strip() for name in dinner_names[0].strip().split('\n') if name.strip()] if dinner_names else []
        workout_names=[name.strip() for name in workout_names[0].strip().split('\n') if name.strip()] if workout_names else []

        return render_template('result.html', restaurant_names=restaurant_names, breakfast_names=breakfast_names, dinner_names=dinner_names, workout_names=workout_names)


    return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)