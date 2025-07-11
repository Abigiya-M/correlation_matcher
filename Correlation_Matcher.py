from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine
import hyperon

# Load the embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize MeTTa
m = hyperon.Metta()

# Load OpenPsi rules file
m.load_file("rules.metta")


def get_all_rules():
    """
    Query MeTTa to get all rule IDs from &psiRules.
    You might need to write a helper in rules.metta if this doesn't exist yet.
    For now, assume it returns a list of rule IDs.
    """
    result = m.evaluate('(getCategories)')  # fallback example
    print("Available categories/rules:", result)

    rules = m.evaluate('(collapse (match &psiRules (: $rule .) $rule))')
    return [str(r) for r in rules]


def get_rule_context(rule_id: str) -> str:
    """
    Query MeTTa to get the context string of a given rule.
    """
    result = m.evaluate(f'(getContext &psiRules {rule_id})')
    if result:
        return str(result[0])
    return ""


def match_rule(conversation_summary: str) -> str:
    """
    Given a conversation summary, find the most correlated rule.
    """
    # Embed the conversation summary
    summary_vector = embedder.encode(conversation_summary)

    rules = get_all_rules()
    if not rules:
        raise ValueError("No rules found in &psiRules")

    best_rule = None
    best_score = -1

    for rule in rules:
        context = get_rule_context(rule)
        if not context:
            continue

        context_vector = embedder.encode(context)
        similarity = 1 - cosine(summary_vector, context_vector)

        print(f"Rule: {rule}, Context: {context}, Similarity: {similarity:.4f}")

        if similarity > best_score:
            best_score = similarity
            best_rule = rule

    return best_rule


if __name__ == "__main__":
    summary = input("Enter conversation summary: ")
    best_rule = match_rule(summary)

    if best_rule:
        print(f"Best matching rule: {best_rule}")
    else:
        print("No matching rule found.")
