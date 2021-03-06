import sys
from owkin_mm_dream import main, preprocess, make_dataset, DEFAULT_FEATURES
import pandas as pd

from sklearn import preprocessing

"""Entry point for owkin_mm_dream."""
if __name__ == "__main__":  # pragma: no cover
    # if sending two more arguments, running predict_more
    if len(sys.argv) in [5, 6]:
        # we need to be able to send the pathway file for docker
        if len(sys.argv) == 6:
            inp = sys.argv[2:]
            clf = main(inp[1], inp[2], pathway_file=sys.argv[1], showcase=False)
        else:
            inp = sys.argv
            clf = main(inp[1], inp[2], showcase=False)
        my_rna_data = pd.read_csv(inp[3], sep="\t", index_col=0)
        my_clinical_data = pd.read_csv(inp[4], sep=",").set_index("Patient")
        # making dataset
        my_rna_data, my_unc_clinical_data = preprocess(my_rna_data, my_clinical_data)
        X = make_dataset(my_rna_data, my_unc_clinical_data)

        # scaling the data
        scaler = preprocessing.StandardScaler().fit(X[DEFAULT_FEATURES].values)
        X_scaled = scaler.transform(X[DEFAULT_FEATURES].values)
        res = clf.predict(X_scaled)

        pd.DataFrame(
            data=res, columns=["pred"], index=my_unc_clinical_data.index
        ).to_csv("new_predictions.csv")
    else:
        print("showcase mode\n")
        # we need to be able to send the pathway file for docker
        if len(sys.argv) == 4:
            main(sys.argv[2], sys.argv[3], pathway_file=sys.argv[1], showcase=True)
        else:
            main(sys.argv[1], sys.argv[2], showcase=True)
