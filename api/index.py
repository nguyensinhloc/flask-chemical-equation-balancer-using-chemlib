from flask import Flask, request, render_template_string
from chemlib import Compound, Reaction

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Chemical Reaction Balancer</title>
    <style>
        body {
            background-image: url("./background.jpg");
            background-size: cover;
            text-align: center;
        }

        h1 {
            font-size: 100px;
            font-family: 'Arial Narrow', sans-serif;
        }

        form label, input {
            font-size: 50px;
            font-family: "Arial Narrow", Helvetica, Arial, sans-serif;
            border-radius: 50px;
        }

        form input[type=submit] {
            background: linear-gradient(315deg, #1e30f3 0%, #e21e80 100%);
            color: white;
            cursor: pointer;
            transition: all 0.3s ease;
            margin: 32px;
            border: none;
            letter-spacing: 1.5px;
            box-shadow: rgb(0 0 0 / 5%) 0 0 8px;
            padding: 17px 40px;
            text-transform: uppercase;
        }

        form input[type=submit]:hover {
            background: hsl(261deg, 80%, 48%);
            color: hsl(0, 0%, 100%);
            box-shadow: rgb(93, 24, 220) 0px 7px 29px 0px;
            letter-spacing: 3px;
        }

        form input[type=submit]:active {
            letter-spacing: 3px;
            background-color: hsl(261deg, 80%, 48%);
            color: hsl(0, 0%, 100%);
            box-shadow: rgb(93, 24, 220) 0px 0px 0px 0px;
            transform: translateY(10px);
            transition: 100ms;
        }
        .result-display {
            font-size: 50px;
            color: black;
            background-color: white;
            padding: 10px;
            margin-top: 20px;
            border: 1px solid #ddd;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            display: inline-block;
        }

    </style>
</head>
<body>
    <h1>Chemical Reaction Balancer</h1>
    <form method="POST">
        <label for="reactants">Enter the reactants (separated by '+'):</label><br>
        <input type="text" id="reactants" name="reactants"><br>
        <label for="products">Enter the products (separated by '+'):</label><br>
        <input type="text" id="products" name="products"><br>
        <input type="submit" value="Balance">
    </form>
    <div class="result-display">
        {{result}}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def balance_reaction():
    result = ""
    if request.method == 'POST':
        reactants_input = request.form['reactants']
        products_input = request.form['products']
        reactants = [Compound(chemical.strip()) for chemical in reactants_input.split('+')]
        products = [Compound(chemical.strip()) for chemical in products_input.split('+')]
        reaction = Reaction(reactants=reactants, products=products)
        reaction.balance()
        if reaction.is_balanced:
            result = f"The balanced equation is: {reaction.formula}"
        else:
            result = "The equation could not be balanced."
    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == '__main__':
    app.run(debug=False)
