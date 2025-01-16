import sys
import pandas as pd
import numpy as np


def validate_inputs(input_file, weights, impacts):
    try:
        data = pd.read_csv(input_file)
    except FileNotFoundError:
        raise Exception("Input file not found. Please check the file path.")
    except Exception as e:
        raise Exception(f"Error reading input file: {e}")

    # Check if the file has at least three columns
    if len(data.columns) < 3:
        raise Exception("Input file must contain at least three columns.")

    # Check if all values from the 2nd to last columns are numeric
    if not all(data.iloc[:, 1:].map(lambda x: isinstance(x, (int, float)) or pd.api.types.is_number(x)).all()):
        raise Exception("All values from the second column onward must be numeric.")

    # Parse weights and impacts
    weight_list = [float(w) for w in weights.split(',')]
    impact_list = impacts.split(',')

    # Check if the number of weights and impacts matches the number of criteria columns
    if len(weight_list) != len(data.columns) - 1 or len(impact_list) != len(data.columns) - 1:
        raise Exception("Number of weights and impacts must match the number of criteria columns.")

    # Validate impacts
    if not all(impact in ['+', '-'] for impact in impact_list):
        raise Exception("Impacts must be '+' or '-'.")

    return data, weight_list, impact_list



def topsis(data, weights, impacts):
    # Normalize the data
    normalized_data = data.iloc[:, 1:].div(np.sqrt((data.iloc[:, 1:] ** 2).sum()), axis=1)

    # Weighted normalized data
    weighted_data = normalized_data.mul(weights)

    # Determine ideal best and ideal worst
    ideal_best = []
    ideal_worst = []

    for i, impact in enumerate(impacts):
        if impact == '+':
            ideal_best.append(weighted_data.iloc[:, i].max())
            ideal_worst.append(weighted_data.iloc[:, i].min())
        else:
            ideal_best.append(weighted_data.iloc[:, i].min())
            ideal_worst.append(weighted_data.iloc[:, i].max())

    # Calculate distances from ideal best and worst
    distance_to_best = np.sqrt(((weighted_data - ideal_best) ** 2).sum(axis=1))
    distance_to_worst = np.sqrt(((weighted_data - ideal_worst) ** 2).sum(axis=1))

    # Calculate Topsis score
    topsis_score = distance_to_worst / (distance_to_best + distance_to_worst)

    # Add results to data
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
