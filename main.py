# main.py
from hyperon import MeTTa
from correlation_matcher import match_rule

m = MeTTa()
m.load_file("rules.metta")
m.load_file("implicator.metta")

summary = "The user is frustrated about long waiting times."

best_rule = match_rule(m, summary)

if best_rule:
    print(f"Best matching rule: {best_rule}")
else:
    print("No matching rule found.")
