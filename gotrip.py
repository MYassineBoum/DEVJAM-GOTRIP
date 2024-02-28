from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('home.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Retrieve form data
    budget = request.form.get('budget')
    duration = request.form.get('duration')
    preferences = request.form.get('preferences')

    best_combination = get_best_combination(budget, duration, preferences)

    if best_combination:
        result_string = f"The best combination is: Hotel {best_combination[0]} and Restaurant {best_combination[2]}"
    else:
        result_string = "No combination found within the given budget and duration."

    return result_string


def get_best_combination(budget, duration, preference):
    conn = sqlite3.connect('gotrip.sqlite3')
    cursor = conn.cursor()

    cursor.execute('''SELECT h.hname, h.price AS hotel_price, r.rname, r.price AS restaurant_price
                      FROM hotel h
                      JOIN city c ON h.id_city = c.id
                      JOIN restaurant r ON r.id_city = c.id
                      WHERE c.nature = ? AND c.culture = ?
                   ''', (preference, preference))

    results = cursor.fetchall()

    # Filter results based on budget and duration
    filtered_results = [(hname, hotel_price, rname, restaurant_price)
                        for hname, hotel_price, rname, restaurant_price in results
                        if hotel_price + restaurant_price <= budget]

    # Calculate the total cost for each combination, including transportation
    combinations = []
    for combination in filtered_results:
        total_cost = combination[1] + combination[3] + 150  # Default transportation cost
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
    if combinations:
        best_combination = combinations[0][0]
        return best_combination
    else:
        return None
