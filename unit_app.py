import streamlit as st

def convert_units(value, from_unit, to_unit, conversion_dict):
    if from_unit in conversion_dict and to_unit in conversion_dict:
        return value * conversion_dict[to_unit] / conversion_dict[from_unit]
    return None

def main():
    st.title("Unit Converter")
    
    category = st.selectbox("Select Category", ["Length", "Weight", "Temperature"])
    
    units = {
        "Length": {"Meters": 1, "Kilometers": 1000, "Centimeters": 0.01, "Millimeters": 0.001, "Miles": 1609.34, "Yards": 0.9144, "Feet": 0.3048, "Inches": 0.0254},
        "Weight": {"Kilograms": 1, "Grams": 0.001, "Pounds": 0.453592, "Ounces": 0.0283495},
        "Temperature": {"Celsius": "C", "Fahrenheit": "F", "Kelvin": "K"}
    }
    
    from_unit = st.selectbox("From Unit", list(units[category].keys()))
    to_unit = st.selectbox("To Unit", list(units[category].keys()))
    value = st.number_input("Enter Value", min_value=0.0, format="%.4f")
    
    if st.button("Convert"):
        if category == "Temperature":
            result = None
            if from_unit == "Celsius" and to_unit == "Fahrenheit":
                result = (value * 9/5) + 32
            elif from_unit == "Celsius" and to_unit == "Kelvin":
                result = value + 273.15
            elif from_unit == "Fahrenheit" and to_unit == "Celsius":
                result = (value - 32) * 5/9
            elif from_unit == "Fahrenheit" and to_unit == "Kelvin":
                result = (value - 32) * 5/9 + 273.15
            elif from_unit == "Kelvin" and to_unit == "Celsius":
                result = value - 273.15
            elif from_unit == "Kelvin" and to_unit == "Fahrenheit":
                result = (value - 273.15) * 9/5 + 32
            else:
                result = value
        else:
            result = convert_units(value, from_unit, to_unit, units[category])
        
        st.success(f"{value} {from_unit} = {result:.4f} {to_unit}")

if __name__ == "__main__":
    main()