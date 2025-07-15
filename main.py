from hyperon import MeTTa
from Correlation_Matcher import match_rule  

def load_metta_file(metta: MeTTa, filepath: str):
    with open(filepath, "r") as f:
        metta.run(f.read())

def main():
    m = MeTTa()
    load_metta_file(m, "rule.metta")
    load_metta_file(m, "implicator.metta")
    load_metta_file(m, "sample_rules.metta")

    summary = "customer asked about billing issues"
    best_rule = match_rule(m, summary)

    print("Best rule:", best_rule)

if __name__ == "__main__":
    main()
