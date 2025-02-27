from flask import Flask, request, render_template, jsonify
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer

app = Flask(__name__)

# Load the dataset and train the KMeans model
data = {"Age,Gender,Weight (kg),Height (cm),Activity Level,Dietary Preferences,Medical Conditions"
"14,Other,16,71,Medium,Gluten-Free,Hypertension"
"49,Other,69,199,High,Vegan,High Cholesterol"
"98,Male,19,140,High,Non-Vegetarian,Obesity"
"91,Other,48,138,Medium,Non-Vegetarian,Diabetes"
"92,Male,88,82,Medium,Non-Vegetarian,Hypertension"
"73,Other,55,73,Medium,Non-Vegetarian,Obesity"
"54,Other,21,169,Low,Gluten-Free,High Cholesterol"
"10,Female,100,166,Medium,Vegan,Obesity"
"100,Female,123,90,Low,Vegan,High Cholesterol"
"15,Female,111,177,High,Non-Vegetarian,None"
"24,Female,39,69,Low,Vegetarian,Hypertension"
"41,Male,89,145,Low,Gluten-Free,Diabetes"
"53,Male,118,191,High,Keto,Diabetes"
"49,Male,37,162,Medium,Vegan,Diabetes"
"86,Other,66,68,High,Gluten-Free,Diabetes"
"64,Other,18,55,Low,Gluten-Free,None"
"14,Male,150,115,Low,Gluten-Free,None"
"5,Male,130,50,High,Keto,Obesity"
"58,Female,93,112,High,Gluten-Free,Hypertension"
"80,Female,50,51,Medium,Vegan,High Cholesterol"
"11,Female,140,174,Medium,Non-Vegetarian,Hypertension"
"60,Other,115,156,High,Keto,High Cholesterol"
"69,Male,133,52,Medium,Vegan,Hypertension"
"95,Female,15,185,Medium,Non-Vegetarian,Obesity"
"70,Other,135,75,High,Non-Vegetarian,Hypertension"
"62,Other,107,135,High,Gluten-Free,None"
"29,Female,89,80,High,Non-Vegetarian,Obesity"
"13,Female,128,99,Medium,Non-Vegetarian,Diabetes"
"29,Female,140,54,Low,Vegan,Hypertension"
"98,Other,73,179,Low,Gluten-Free,None"
"64,Male,70,111,Low,Vegan,None"
"14,Other,90,60,Medium,Gluten-Free,Hypertension"
"63,Other,141,79,Low,Vegan,Obesity"
"67,Female,61,123,High,Non-Vegetarian,Hypertension"
"58,Male,96,67,High,Non-Vegetarian,Diabetes"
"49,Male,147,117,Low,Non-Vegetarian,Diabetes"
"97,Female,56,92,Low,Gluten-Free,Diabetes"
"34,Male,57,106,Medium,Vegan,Diabetes"
"14,Female,43,67,High,Vegan,High Cholesterol"
"75,Female,20,151,Low,Vegetarian,None"
"9,Female,76,198,High,Non-Vegetarian,Obesity"
"13,Male,24,120,Low,Vegan,Hypertension"
"57,Other,100,118,High,Gluten-Free,Obesity"
"2,Other,91,65,Medium,Non-Vegetarian,Diabetes"
"77,Other,120,61,Medium,Gluten-Free,Obesity"
"58,Male,105,191,High,Vegetarian,Diabetes"
"5,Other,69,168,Medium,Vegan,Obesity"
"4,Male,22,122,Medium,Gluten-Free,Obesity"
"28,Other,98,193,High,Vegan,Diabetes"
"28,Other,59,112,Low,Gluten-Free,High Cholesterol"
"51,Male,105,177,Medium,Vegetarian,None"
"81,Female,39,152,Low,Keto,Hypertension"
"63,Other,68,123,High,Keto,None"
"8,Female,103,173,High,Non-Vegetarian,High Cholesterol"
"21,Other,92,187,Medium,Gluten-Free,High Cholesterol"
"23,Other,71,74,High,Non-Vegetarian,Hypertension"
"61,Male,35,85,Low,Non-Vegetarian,Hypertension"
"13,Other,87,105,Medium,Non-Vegetarian,None"
"60,Female,134,123,Low,Keto,Obesity"
"47,Male,101,160,High,Gluten-Free,High Cholesterol"
"49,Male,26,190,High,Vegan,Hypertension"
"30,Other,22,173,Low,Gluten-Free,Obesity"
"94,Male,53,159,High,Vegan,High Cholesterol"
"66,Male,18,66,Low,Keto,High Cholesterol"
"29,Other,49,83,Low,Vegan,Diabetes"
"27,Female,142,75,Low,Non-Vegetarian,High Cholesterol"
"23,Female,17,86,Low,Vegetarian,Hypertension"
"99,Female,58,114,Medium,Vegetarian,Diabetes"
"89,Female,112,132,Low,Gluten-Free,Obesity"
"12,Male,110,129,Low,Keto,High Cholesterol"
"2,Female,69,162,High,Gluten-Free,Hypertension"
"36,Male,140,158,High,Keto,High Cholesterol"
"72,Other,128,91,High,Vegan,None"
"28,Other,20,101,Medium,Vegetarian,Obesity"
"12,Other,60,87,Medium,Vegetarian,None"
"95,Male,67,76,Medium,Keto,Diabetes"
"33,Male,139,187,Low,Vegetarian,Diabetes"
"54,Other,59,133,Low,Non-Vegetarian,Obesity"
"4,Other,127,183,Medium,Gluten-Free,High Cholesterol"
"26,Other,135,184,Low,Vegetarian,Obesity"
"98,Other,93,197,Medium,Vegan,None"
"86,Male,61,52,Low,Non-Vegetarian,Obesity"
"8,Other,112,173,Low,Vegan,None"
"43,Other,150,50,Low,Non-Vegetarian,High Cholesterol"
"56,Male,148,161,High,Gluten-Free,Hypertension"
"59,Other,131,126,Medium,Vegetarian,Diabetes"
"33,Female,81,198,High,Vegan,Obesity"
"32,Female,84,155,Medium,Keto,Diabetes"
"52,Female,112,162,High,Keto,Obesity"
"71,Female,127,114,Low,Vegan,High Cholesterol"
"84,Female,105,61,Low,Vegetarian,Obesity"
"14,Male,75,136,Medium,Non-Vegetarian,Diabetes"
"96,Other,96,75,Low,Vegan,High Cholesterol"
"70,Other,56,85,Medium,Gluten-Free,None"
"77,Other,117,183,Medium,Non-Vegetarian,None"
"96,Female,122,82,High,Vegetarian,Hypertension"
"11,Male,41,65,Medium,Vegetarian,Obesity"
"37,Female,15,63,Low,Vegetarian,Obesity"
"23,Other,106,192,High,Keto,Diabetes"
"79,Other,97,80,Medium,Keto,Obesity"
"34,Other,63,87,Medium,Gluten-Free,Hypertension"
"41,Female,60,73,High,Vegan,Obesity"
"17,Female,48,140,Medium,Keto,Obesity"
"66,Male,38,178,High,Vegetarian,None"
"77,Female,40,169,Medium,Non-Vegetarian,Diabetes"
"38,Male,62,106,High,Vegan,Diabetes"
"85,Other,27,78,Low,Gluten-Free,High Cholesterol"
"51,Female,39,107,Medium,Keto,Hypertension"
"53,Female,129,124,High,Gluten-Free,Hypertension"
"83,Other,96,168,High,Non-Vegetarian,Diabetes"
"10,Other,53,146,Low,Vegan,Hypertension"
"31,Male,108,142,Medium,Vegetarian,None"
"31,Other,15,161,Medium,Keto,None"
"82,Other,20,98,Medium,Non-Vegetarian,Diabetes"
"16,Male,122,56,Medium,Keto,High Cholesterol"
"14,Other,51,121,High,Vegan,High Cholesterol"
"26,Female,62,110,Medium,Vegetarian,None"
"44,Female,68,94,Low,Non-Vegetarian,None"
"8,Other,129,51,Low,Non-Vegetarian,Diabetes"
"31,Other,101,73,Low,Gluten-Free,Diabetes"
"44,Male,70,183,Medium,Vegan,Diabetes"
"98,Female,102,87,Medium,Vegan,Obesity"
"86,Other,92,110,Low,Non-Vegetarian,Obesity"
"28,Female,83,181,High,Vegan,Diabetes"
"39,Other,110,133,High,Vegetarian,Hypertension"
"32,Male,129,57,Medium,Gluten-Free,None"
"84,Other,97,155,Low,Vegan,Hypertension"
"11,Other,134,105,Medium,Gluten-Free,Hypertension"
"48,Female,148,76,Medium,Gluten-Free,Diabetes"
"45,Male,17,50,Medium,Vegan,Diabetes"
"67,Male,58,169,Low,Vegan,None"
"8,Male,99,76,Medium,Keto,None"
"87,Other,52,190,High,Gluten-Free,Hypertension"
"46,Female,56,135,Medium,Vegetarian,Hypertension"
"34,Other,65,157,High,Keto,Obesity"
"55,Male,75,92,Low,Gluten-Free,Hypertension"
"34,Other,115,157,Medium,Non-Vegetarian,Obesity"
"87,Female,122,152,High,Vegan,Obesity"
"60,Male,138,171,Low,Non-Vegetarian,Diabetes"
"55,Female,147,172,High,Keto,Obesity"
"14,Male,16,128,High,Vegetarian,High Cholesterol"
"12,Male,20,161,Medium,Vegetarian,High Cholesterol"
"23,Female,101,57,Medium,Gluten-Free,High Cholesterol"
"43,Female,40,131,Low,Gluten-Free,High Cholesterol"
"81,Female,119,123,Low,Vegan,Obesity"
"12,Male,78,167,Medium,Non-Vegetarian,Hypertension"
"92,Other,129,83,Low,Keto,Diabetes"
"66,Male,97,178,Medium,Non-Vegetarian,None"
"93,Male,122,158,Low,Vegetarian,High Cholesterol"
"8,Female,105,131,Low,Keto,Obesity"
"75,Female,134,110,Low,Vegetarian,Obesity"
"80,Other,62,60,High,Vegan,Hypertension"
"4,Other,138,193,High,Vegetarian,High Cholesterol"
"74,Female,145,70,Medium,Vegetarian,Hypertension"
"13,Other,36,193,Low,Vegan,Diabetes"
"21,Female,131,109,High,Gluten-Free,Hypertension"
"71,Female,53,148,Low,Gluten-Free,Obesity"
"2,Other,23,135,Low,Non-Vegetarian,High Cholesterol"
"6,Other,140,105,Medium,Non-Vegetarian,Diabetes"
"2,Other,37,55,High,Non-Vegetarian,Obesity"
"33,Male,48,51,Medium,Gluten-Free,Obesity"
"1,Male,87,102,High,Vegetarian,None"
"64,Other,141,123,Low,Gluten-Free,Hypertension"
"64,Female,94,74,Low,Keto,Diabetes"
"50,Other,131,191,Medium,Vegan,Diabetes"
"74,Female,138,96,Low,Vegan,Hypertension"
"86,Other,49,195,Low,Vegetarian,Obesity"
"68,Male,121,135,High,Gluten-Free,Obesity"
"71,Male,75,133,Low,Vegan,Hypertension"
"1,Male,55,116,Low,Gluten-Free,None"
"22,Female,105,79,Medium,Non-Vegetarian,None"
"11,Female,35,116,High,Keto,High Cholesterol"
"3,Female,67,137,Low,Keto,Obesity"
"7,Female,58,99,Medium,Gluten-Free,None"
"27,Female,132,116,Medium,Gluten-Free,High Cholesterol"
"58,Female,75,98,Medium,Keto,Obesity"
"20,Male,119,75,Low,Keto,Obesity"
"71,Female,48,150,High,Vegan,High Cholesterol"
"59,Male,63,73,Medium,Vegan,Diabetes"
"44,Male,71,80,Low,Vegan,Hypertension"
"71,Female,20,164,High,Vegan,Obesity"
"43,Male,86,189,Low,Vegan,None"
"12,Other,108,143,Medium,Gluten-Free,Diabetes"
"30,Female,125,117,High,Vegan,None"
"19,Male,128,149,Low,Keto,Hypertension"
"8,Male,24,111,Medium,Vegan,None"
"16,Other,53,117,Medium,Vegetarian,High Cholesterol"
"13,Female,94,185,Medium,Gluten-Free,None"
"47,Female,18,117,Low,Vegetarian,Obesity"
"86,Male,92,137,High,Vegetarian,Obesity"
"13,Male,116,146,High,Vegan,Hypertension"
"35,Male,76,199,High,Vegan,High Cholesterol"
"25,Male,73,83,Low,Vegetarian,Hypertension"
"4,Other,30,133,Medium,Keto,Obesity"
"64,Male,148,108,High,Vegan,Hypertension"
"9,Male,85,69,High,Vegetarian,Hypertension"
"38,Male,73,132,Low,Gluten-Free,High Cholesterol"
"90,Other,113,200,High,Vegan,Hypertension"
"91,Other,146,115,Medium,Vegan,High Cholesterol"
"42,Female,89,55,Low,Non-Vegetarian,High Cholesterol"
} # Replace with your actual dataset
# Handle missing values
imputer = SimpleImputer(strategy='mean')
data[['Age', 'Weight (kg)', 'Height (cm)']] = imputer.fit_transform(data[['Age', 'Weight (kg)', 'Height (cm)']])

imputer_cat = SimpleImputer(strategy='most_frequent')
data[['Medical Conditions']] = imputer_cat.fit_transform(data[['Medical Conditions']])

# Convert categorical data to numeric for clustering
data['Gender'] = data['Gender'].astype('category').cat.codes
data['Activity Level'] = data['Activity Level'].astype('category').cat.codes
data['Dietary Preferences'] = data['Dietary Preferences'].astype('category').cat.codes
data['Medical Conditions'] = data['Medical Conditions'].astype('category').cat.codes

# Define features for clustering
X = data[['Age', 'Weight (kg)', 'Height (cm)', 'Activity Level', 'Dietary Preferences', 'Medical Conditions']]

# Fit KMeans model
kmeans = KMeans(n_clusters=3, random_state=0)
data['Cluster'] = kmeans.fit_predict(X)

# Function to generate diet plan based on the cluster
def generate_diet_plan(cluster):
    if cluster == 0:
        return {
            "Breakfast": "Scrambled eggs with spinach, whole grain bread, almond milk smoothie",
            "Lunch": "Grilled chicken salad with steamed broccoli, coconut water",
            "Dinner": "Baked salmon with roasted sweet potatoes, steamed greens"
        }
    elif cluster == 1:
        return {
            "Breakfast": "Oatmeal with almond butter and chopped nuts, fresh fruit",
            "Lunch": "Quinoa salad with chickpeas, avocado, sautéed greens",
            "Dinner": "Lentil stew with brown rice, steamed greens"
        }
    else:
        return {
            "Breakfast": "Gluten-free pancake with almond butter and nuts, green tea",
            "Lunch": "Vegetable soup with a side of brown rice, fresh fruit",
            "Dinner": "Grilled tofu with roasted sweet potatoes and kale"
        }

# Flask route to display the HTML form
@app.route('/')
def index():
    return render_template('index.html')

# Flask route to predict diet based on input from HTML form
@app.route('/predict_diet', methods=['POST'])
def predict_diet():
    try:
        # Get input data from the form
        age = int(request.form['age'])
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        activity_level = request.form['activity_level']
        dietary_preferences = request.form['dietary_preferences']
        medical_conditions = request.form['medical_conditions']

        # Prepare input for prediction
        input_data = pd.DataFrame([{
            'Age': age,
            'Weight (kg)': weight,
            'Height (cm)': height,
            'Activity Level': activity_level,
            'Dietary Preferences': dietary_preferences,
            'Medical Conditions': medical_conditions
        }])

        # Handle missing values in the input data
        input_data[['Age', 'Weight (kg)', 'Height (cm)']] = imputer.transform(input_data[['Age', 'Weight (kg)', 'Height (cm)']])
        input_data[['Medical Conditions']] = imputer_cat.transform(input_data[['Medical Conditions']])

        # Convert categorical data to numeric
        input_data['Activity Level'] = input_data['Activity Level'].astype('category').cat.codes
        input_data['Dietary Preferences'] = input_data['Dietary Preferences'].astype('category').cat.codes
        input_data['Medical Conditions'] = input_data['Medical Conditions'].astype('category').cat.codes

        # Predict the cluster for the input data
        cluster = kmeans.predict(input_data[['Age', 'Weight (kg)', 'Height (cm)', 'Activity Level', 'Dietary Preferences', 'Medical Conditions']])[0]

        # Generate the diet plan for the predicted cluster
        diet_plan = generate_diet_plan(cluster)

        # Return the diet plan to the user
        return render_template('index.html', diet_plan=diet_plan)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
