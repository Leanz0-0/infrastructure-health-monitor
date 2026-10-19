
def is_sustained_high(samples, threshold=85, required=3):
    if len(samples) < required:
        return False

    recent_samples = samples[-required:]

    return all(value >= threshold for value in recent_samples)
