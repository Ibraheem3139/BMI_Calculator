# BMI_Calculator
Python based BMI Calculator

# Introduction
This program is a BMI (Body Mass Index) calculator with a graphical user interface (GUI) built using the Tkinter library. Here's what it does:

It creates a GUI window with fields for entering a person's name, weight in kilograms, and height in meters.

When the "Calculate BMI" button is pressed, it calculates the BMI of the person based on the provided weight and height and inserts this information along with the person's name and the current date into an SQLite database.

It displays the calculated BMI on the GUI.

It maintains a history of BMI records in a treeview widget, showing the name, BMI, and date for each record.

It provides a "Show Trend" button that, when pressed, displays a plot showing the BMI trend over time for the stored records.
