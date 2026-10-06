def analyze_symptoms(symptom_text):
    """
    Simple educational symptom-pattern analyzer.
    This is not a medical diagnosis.
    """

    symptoms = symptom_text.lower()

    if "fever" in symptoms and "cough" in symptoms:
        return "Flu-like pattern"

    if "cough" in symptoms and "runny nose" in symptoms:
        return "Common Cold-like pattern"

    if "sore throat" in symptoms and "cough" in symptoms:
        return "Throat/respiratory pattern"

    if (
        "stomach pain" in symptoms
        and "vomiting" in symptoms
        and "diarrhea" in symptoms
    ):
        return "Gastrointestinal pattern"

    if "headache" in symptoms and "fatigue" in symptoms:
        return "Headache/fatigue pattern"

    if "headache" in symptoms:
        return "Headache pattern"

    if "stomach pain" in symptoms:
        return "Stomach-related pattern"

    if "vomiting" in symptoms or "diarrhea" in symptoms:
        return "Gastrointestinal pattern"

    return "General symptom pattern"