import sys
import pandas as pd
import numpy as np


def validate_inputs(input_file, weights, impacts):
    try:
        data = pd.read_csv(input_file)
    except FileNotFoundError:
        raise Exception("Input file not found..")
    except Exception as e:
        raise Exception(f"Error reading input file: {e}")

    if len(data.columns) < 3:
        raise Exception("Input file must contain at least 3 columns.")
    #splitting weights and impacts by comma
    weight_list = [float(w) for w in weights.split(',')]
    impact_list = impacts.split(',')

    if len(weight_list) != len(data.columns) - 1 or len(impact_list) != len(data.columns) - 1:
        raise Exception("Number of weights and impacts must match the number of criteria columns.")

    if not all(impact in ['+', '-'] for impact in impact_list):
        raise Exception("Impacts must be '+' or '-'.")

    return data, weight_list, impact_list



def topsis(data, weights, impacts):
    normalized_data = data.iloc[:, 1:].div(np.sqrt((data.iloc[:, 1:] ** 2).sum()), axis=1)

    weighted_data = normalized_data.mul(weights)

    ideal_best = []
    ideal_worst = []

    for i, impact in enumerate(impacts):
        if impact == '+':
            ideal_best.append(weighted_data.iloc[:, i].max())
            ideal_worst.append(weighted_data.iloc[:, i].min())
        else:
            ideal_best.append(weighted_data.iloc[:, i].min())
            ideal_worst.append(weighted_data.iloc[:, i].max())
    #euclidean distance
    distance_to_best = np.sqrt(((weighted_data - ideal_best) ** 2).sum(axis=1))
    distance_to_worst = np.sqrt(((weighted_data - ideal_worst) ** 2).sum(axis=1))

    topsis_score = distance_to_worst / (distance_to_best + distance_to_worst)

    data['Topsis Score'] = np.round(topsis_score,3)
    data['Rank'] = topsis_score.rank(ascending=False).astype(int)

    return data


def main():
    if len(sys.argv) != 5:
        print("Usage: python <program.py> <InputDataFile> <Weights> <Impacts> <ResultFileName>")
        return

    input_file = sys.argv[1]
    weights = sys.argv[2]
    impacts = sys.argv[3]
    result_file = sys.argv[4]

    try:
        data, weight_list, impact_list = validate_inputs(input_file, weights, impacts)
        result = topsis(data, weight_list, impact_list)
        result.to_csv(result_file, index=False)
        print(f"Results saved to {result_file}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
