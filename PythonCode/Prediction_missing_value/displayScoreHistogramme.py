import matplotlib.pyplot as plt

# Données
data_with_weather = {
    'KNN': {'MSE': 29.279765866817296, 'MAE': 1.4423992648194197, 'R2': 0.8623419392162366},
    'KNN_S': {'MSE': 33.8442528063198, 'MAE': 1.570791571638071, 'R2': 0.8408821221048974},
    'KNN_T': {'MSE': 25.778509822993243, 'MAE': 1.2876630390181119, 'R2': 0.878803003812606},
    'interpolationST': {'MSE': 140.0021443271244, 'MAE': 4.305564447107905, 'R2': 0.341783544946925},
    'randomForest': {'MSE': 19.99275484273342, 'MAE': 1.131653445830308, 'R2': 0.9060045809828384},
    'regressionLineaire': {'MSE': 29.535271552051398, 'MAE': 1.5270662862517748, 'R2': 0.8611406858555185},
    'regressionLasso': {'MSE': 31.14275274111297, 'MAE': 1.5765545014817817, 'R2': 0.8535831546840219},
    'regressionRidge': {'MSE': 29.53528600974346, 'MAE': 1.5270663178279755, 'R2': 0.8611406178830538},
    'GBM': {'MSE': 22.13968247175029, 'MAE': 1.2593188008240142, 'R2': 0.8959108563472709},
    'ANN': {'MSE': 22.906498333180533, 'MAE': 1.2066824050772347, 'R2': 0.8923056914377266}
}

data_without_weather = {
    'KNN': {'MSE': 31.175012080248365, 'MAE': 1.4893224290995637, 'R2': 0.8534314882366963},
    'KNN_S': {'MSE': 36.1125449389733, 'MAE': 1.6214324663449375, 'R2': 0.8302178053992089},
    'KNN_T': {'MSE': 27.20830717099467, 'MAE': 1.3264911825957326, 'R2': 0.8720808486172769},
    'interpolationST': {'MSE': 139.7965826559224, 'MAE': 4.305014873767917, 'R2': 0.34274998781937993},
    'randomForest': {'MSE': 36.10587340699423, 'MAE': 1.756906844942814, 'R2': 0.8302491714339947},
    'regressionLineaire': {'MSE': 36.106064114204486, 'MAE': 1.757034779337526, 'R2': 0.8302482748289856},
    'regressionLasso': {'MSE': 36.106064114204486, 'MAE': 1.757034779337526, 'R2': 0.8302482748289856},
    'regressionRidge': {'MSE': 36.106064114204486, 'MAE': 1.757034779337526, 'R2': 0.8302482748289856},
    'GBM': {'MSE': 36.106064114205715, 'MAE': 1.7570347793373, 'R2': 0.8302482748289798},
    'ANN': {'MSE': 36.11893108829481, 'MAE': 1.7643557597875892, 'R2': 0.8301877810835955}
}


# Paramètres pour l'affichage
metrics = ['MSE', 'MAE', 'R2']
colors = ['b', 'g', 'r']
width = 0.2

# Création des graphes
fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(18, 6))
fig.suptitle("MSE, MAE and R2 values for different models without weather data")

for i, (ax, metric) in enumerate(zip(axes, metrics)):
    ax.bar(
        range(len(data_with_weather)),
        [model[metric] for model in data_with_weather.values()],
        color=colors[i]
    )
    ax.set_xticks(range(len(data_with_weather)))
    ax.set_xticklabels(data_with_weather.keys(), rotation=45)
    ax.set_title(metric)
    ax.set_xlabel("Models")
    ax.set_ylabel("Value")

# Affichage des graphes
plt.tight_layout()
plt.show()