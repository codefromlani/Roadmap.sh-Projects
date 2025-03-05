from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)


length_conversions = {
    'meter': 1,
    'kilometer': 0.001,
    'centimeter': 100,
    'millimeter': 1000,
    'mile': 0.000621371,
    'yard': 1.09361,
    'foot': 3.28084,
    'inch': 39.3701
}

weight_conversions = {
    'kilogram': 1,
    'gram': 100,
    'milligram': 1000000,
    'pound': 2.20462,
    'ounce': 35.274
}

temperature_conversions = {
    'celsius': 'celsius',
    'fahrenheit': 'fahrenheit',
    'kelvin': 'kelvin'
}

volume_conversions = {
    'liter': 1,
    'milliliter': 1000,
    'gallon': 0.264172,
    'quart': 1.05669,
    'pint': 2.11338,
    'cup': 4.22675,
    'fluid_ounce': 33.814
}

def convert_units(value, from_unit, to_unit, unit_type):
    if unit_type == 'length':
        meters = value / length_conversions[from_unit]
        return meters * length_conversions[to_unit]
    
    elif unit_type == 'weight':
        kilograms = value / weight_conversions[from_unit]
        return kilograms * weight_conversions[to_unit]
    
    elif unit_type == 'temperature':
        # Temperature requires special formulas
        if from_unit == 'celsius' and to_unit == 'fahrenheit':
            return (value * 9/5) + 32
        elif from_unit == 'celsius' and to_unit == 'kelvin':
            return value + 273.15
        elif from_unit == 'fahrenheit' and to_unit == 'celsius':
            return (value - 32) * 5/9
        elif from_unit == 'fahrenheit' and to_unit == 'kelvin':
            return ((value - 32) * 5/9) + 273.15
        elif from_unit == 'kelvin' and to_unit == 'celsius':
            return value - 273.15
        elif from_unit == 'kelvin' and to_unit == 'fahrenheit':
            return ((value - 273.15) * 9/5) + 32
        else:
            return value
        
    elif unit_type == 'volume':
        liters = value / volume_conversions[from_unit]
        return liters * volume_conversions[to_unit]
    
    return None

@app.route('/')
def index():
    return redirect(url_for('length_converter'))  


@app.route('/length', methods=['GET', 'POST'])
def length_converter():
    result = None
    value = 0
    from_unit = ''
    to_unit = ''

    if request.method == 'POST':
        try:
            value = float(request.form['value'])
            from_unit = request.form['from_unit']
            to_unit = request.form['to_unit']

            result = convert_units(value, from_unit, to_unit, 'length')
            if result is not None:
                result = round(result, 6)

        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template(
        'length.html',
        result=result,
        value=value,
        from_unit=from_unit,
        to_unit=to_unit,
        length_units=length_conversions
    )

@app.route('/weight', methods=['GET', 'POST'])
def weight_converter():
    result = None
    value = 0
    from_unit = ''
    to_unit = ''

    if request.method == 'POST':
        try:
            value = float(request.form['value'])
            from_unit = request.form['from_unit']
            to_unit = request.form['to_unit']

            result = convert_units(value, from_unit, to_unit, 'weight')
            if result is not None:
                result = round(result, 6)

        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template(
        'weight.html',
        result=result,
        value=value,
        from_unit=from_unit,
        to_unit=to_unit,
        weight_units=weight_conversions
    )

@app.route('/temperature', methods=['GET', 'POST'])
def temperature_converter():
    result = None
    value = 0
    from_unit = ''
    to_unit = ''

    if request.method == 'POST':
        try:
            value = float(request.form['value'])
            from_unit = request.form['from_unit']
            to_unit = request.form['to_unit']

            result = convert_units(value, from_unit, to_unit, 'temperature')
            if result is not None:
                result = round(result, 6)

        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template(
        'temperature.html',
        result=result,
        value=value,
        from_unit=from_unit,
        to_unit=to_unit,
        temperature_units=temperature_conversions
    )

@app.route('/volume', methods=['GET', 'POST'])
def volume_converter():
    result = None
    value = 0
    from_unit = ''
    to_unit = ''

    if request.method == 'POST':
        try:
            value = float(request.form['value'])
            from_unit = request.form['from_unit']
            to_unit = request.form['to_unit']

            result = convert_units(value, from_unit, to_unit, 'volume')
            if result is not None:
                result = round(result, 6)

        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template(
        'volume.html',
        result=result,
        value=value,
        from_unit=from_unit,
        to_unit=to_unit,
        volume_units=volume_conversions
    )



if __name__ == '__main__':
    app.run(debug=True)