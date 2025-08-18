from transformers import pipeline

# Load Hugging Face zero-shot classifier
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

CATEGORIES = ["Billing Issue", "Technical Support", "General Query"]

def classify_email(email_text: str) -> str:
    """
    Classify email into categories using Hugging Face zero-shot classification.
    """
    result = classifier(email_text, candidate_labels=CATEGORIES)
    return result["labels"][0]  # return top predicted category


if __name__ == "__main__":
    # Quick test
    test_texts = [
        "My payment did not go through.",
        "The app crashes every time I open it.",
        "Can you tell me about your pricing plans?"
    ]
    for text in test_texts:
        print(f"Email: {text}")
        print("Predicted Category:", classify_email(text))
        print("-" * 40)
