from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('home.html', result="")

@app.route('/submit', methods=['POST'])
def submit():
    budget = float(request.form.get('budget'))
    duration = int(request.form.get('duration'))
    preferences = request.form.get('preferences')
    best_combinations = get_best_combination(budget, duration, preferences)

    result_string = "The best combination is: \n"
    for best_combination in best_combinations:
        if best_combination:
            result_string += f"Hotel {best_combination[0]} and Restaurant {best_combination[2]}\n"
        else:
            result_string += "No combination found within the given budget and duration.\n"
    return render_template('home.html', result=format_str(result_string))

def format_str(in_string):
    """Replaces '\n' with </br> to properly display the string in
    an html file
    """
    return "</br>".join(in_string.split("\n"))

def get_best_combination(budget, duration, preference):
    conn = sqlite3.connect('gotrip.sqlite3')
    cursor = conn.cursor()

    cursor.execute('''SELECT h.hname, h.price AS hotel_price, r.rname, r.price AS restaurant_price
                      FROM hotel h
                      JOIN city c ON h.id_city = c.id
                      JOIN restaurant r ON r.id_city = c.id
                      WHERE c.nature = ? OR c.culture = ?
                   ''', (preference == "nature", preference == "culture"))

    results = cursor.fetchall()
    # Filter results based on budget and duration   
    filtered_results = [(hname, float(hotel_price), rname, float(restaurant_price))
                        for hname, hotel_price, rname, restaurant_price in results
                        if float(hotel_price) + (float(restaurant_price)) <= (budget / duration)]

    # Calculate the total cost for each combination, including transportation
    combinations = []
    for combination in filtered_results:
        total_cost = combination[1] + (combination[3] * duration) + (150 * (duration - 1))
        if total_cost <= budget:
            combinations.append((combination, total_cost))

    # Rank the combinations based on the preference specified
    if preference == "nature":
        # Sort by the total cost in ascending order
        combinations.sort(key=lambda x: x[1])
    elif preference == "culture":
        # Sort by the total cost in ascending order
        combinations.sort(key=lambda x: x[1])
    elif preference == "gastronomy":
        # Promote results with gastronomy preference by sorting by total cost in descending order
        combinations.sort(key=lambda x: x[1], reverse=True)

    conn.close()

    # Return the best combination
    best_combination = []
    if combinations:
        try:
            for i in range(duration):
                best_combination.append(combinations[i][0])   
            return best_combination
        except IndexError:
            return None
    else:
        return None
