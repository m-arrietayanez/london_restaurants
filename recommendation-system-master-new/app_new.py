import flask
import pandas as pd

app = flask.Flask(__name__, template_folder='templates')

df2 = pd.read_csv('./model/alya_open_table.csv')

def get_recommendations(cuisine):
    new_df = df2[(df2['cuisine'] == cuisine)]
    rest_name = new_df['full_name']
    rest_cuisine = new_df['cuisine']
    rest_price = new_df['price_range']
    rest_rating = new_df['rating']
    rest_location = new_df['location']
    return_df = pd.DataFrame(columns=['Name','Cuisine','Price','Rating','Location'])
    return_df['Name'] = rest_name
    return_df['Cuisine'] = rest_cuisine
    return_df['Price'] = rest_price
    return_df['Rating'] = rest_rating
    return_df['Location'] = rest_location
    return return_df


all_cuisines= ["International", "Seafood", "Steak", "Latin American", "Indian", "Vietnamese", "Asian", "Italian",
              "Middle Eastern", "Russian", "Vegetarian / Vegan", "Japanese", "Korean", "Chinese", "Spanish", "American",
            "Chinese (Sichuan)", "Modern European", "French", "Others", "Thai", "British", "Greek"]

# Set up the main route
@app.route('/', methods=['GET', 'POST'])

def main():
    if flask.request.method == 'GET':
        return(flask.render_template('index_new.html'))
            
    if flask.request.method == 'POST':
        r_cuisine = flask.request.form['cuisine_name']
        r_cuisine = r_cuisine.title()
        if (r_cuisine not in all_cuisines) :
            return(flask.render_template('negative_new.html',name=r_cuisine))
        else:
            result_final = get_recommendations(r_cuisine)
            names = []
            cuisines = []
            prices = []
            ratings=[]
            locations=[]
            for i in range(len(result_final)):
               names.append(result_final.iloc[i][0])
               cuisines.append(result_final.iloc[i][1])
               prices.append(result_final.iloc[i][2])
               ratings.append(result_final.iloc[i][3])
               locations.append(result_final.iloc[i][4])

            return flask.render_template('positive_new.html',rest_names=names,rest_cuisines=cuisines,rest_prices=prices,
                                         rest_ratings=ratings,rest_locations=locations,search_name=r_cuisine)

if __name__ == '__main__':
    app.run()