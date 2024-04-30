from flask import Flask, request, render_template_string
from chemlib import Compound, Reaction

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Chemical Reaction Balancer</title>
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
    {{result}}
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
