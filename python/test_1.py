import pandas
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
# Make a dictionary of data for boot sizes
# and harness sizes in cm
data = {
    'Tamanho_botas' : [ 39, 38, 37, 39, 38, 35, 37, 36, 35, 40, 
                    40, 36, 38, 39, 42, 42, 36, 36, 35, 41, 
                    42, 38, 37, 35, 40, 36, 35, 39, 41, 37, 
                    35, 41, 39, 41, 42, 42, 36, 37, 37, 39,
                    42, 35, 36, 41, 41, 41, 39, 39, 35, 39
 ],
    'Tamanho_arreios': [ 58, 58, 52, 58, 57, 52, 55, 53, 49, 54,
                59, 56, 53, 58, 57, 58, 56, 51, 50, 59,
                59, 59, 55, 50, 55, 52, 53, 54, 61, 56,
                55, 60, 57, 56, 61, 58, 53, 57, 57, 55,
                60, 51, 52, 56, 55, 57, 58, 57, 51, 59
                ]
}

# Convert it into a table using pandas
dataset = pandas.DataFrame(data)

#print(dataset)


# Print the data
# In normal python we would write
# print(dataset)
# but in Jupyter notebooks, we simply write the name
# of the variable and it is printed nicely 
dataset

# Load a library to do the hard work for us


# First, we define our formula using a special syntax
# separa a variavel dependente da independente 
formula = "Tamanho_botas ~ Tamanho_arreios"

# Create the model, but don't train it yet
model = smf.ols(formula = formula, data = dataset)


# verificar se tem parametro treinado
if not hasattr(model, 'params'):
    print("Model selected but it does not have parameters set. We need to train it!")
# Train (fit) the model so that it creates a line that 
# fits our data. This method does the hard work for
# us. We will look at how this method works in a later unit.

fitted_model = model.fit()

# Print information about our model now it has been fit
print("Os seguintes parametros do modelo foram encontrados:\n" +
        f"Inclinacao da linha: {fitted_model.params.iloc[1]}\n"+
        f"Intercepto da linha: {fitted_model.params.iloc[0]}")



# Show a scatter plot of the data points and add the fitted line
# Don't worry about how this works for now
plt.scatter(dataset["Tamanho_arreios"], dataset["Tamanho_botas"])
plt.plot(dataset["Tamanho_arreios"], fitted_model.params.iloc[1] * dataset["Tamanho_arreios"] + fitted_model.params.iloc[0], 'r', label='Fitted line')

# add labels and legend
plt.xlabel("Tamanho_arreios")
plt.ylabel("Tamanho_botas")
plt.legend()


harness_size_input = 0.0
while harness_size_input != -1:
# harness_size states the size of the harness we are interested in
    harness_size_input = float(input("Tamanho do arreio: "))
    harness_size= { 'Tamanho_arreios' : [harness_size_input] }

    # Use the model to predict what size of boots the dog will fit
    approximate_boot_size = fitted_model.predict(harness_size)

    # Print the result
    print("Estimated approximate_boot_size:")
    print(approximate_boot_size[0])