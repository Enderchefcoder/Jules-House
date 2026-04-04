import random

def audio_to_tags(audio_source):
    """
    Simulates turning raw audio source into sensory string tags representing 'energy' levels.
    For this prototype, we simulate different audio types.
    """
    # [Sample Index][Energy Level Hex]
    tags = []

    # Simulate a sequence of energy levels for different audio types
    if audio_source == "heavy_impact":
        energy_pattern = [0x10, 0x90, 0xFF, 0x80, 0x30, 0x10, 0x05]
    elif audio_source == "steady_hum":
        energy_pattern = [0x40, 0x42, 0x3F, 0x41, 0x40, 0x40, 0x41]
    elif audio_source == "bird_chirp":
        energy_pattern = [0x05, 0x20, 0x05, 0x30, 0x05, 0x25, 0x05]
    else:
        # Default/Random
        energy_pattern = [random.randint(0, 255) for _ in range(7)]

    for i, level in enumerate(energy_pattern):
        tags.append(f"w{i:02d}_{level:02x}")

    return f"<|AUDIO_SENSE: {'|'.join(tags)} |>"

def guess_audio_game():
    """A prototype for the AI to guess the audio type from its tags."""
    audio_types = ["heavy_impact", "steady_hum", "bird_chirp"]
    target = random.choice(audio_types)
    tags = audio_to_tags(target)

    print(f"Generated Sensory Packet: {tags}")
    print("AI Guessing Audio Source...")

    # Internal Logic (Simulated Guess)
    # 1. Parse tags to find max energy
    tag_parts = tags.strip("<|>").replace("AUDIO_SENSE: ", "").split("|")
    energies = [int(p.split("_")[1], 16) for p in tag_parts]
    max_e = max(energies)
    avg_e = sum(energies) / len(energies)
    variance = max_e - min(energies)

    if max_e > 200:
        guess = "heavy_impact"
    elif variance < 10:
        guess = "steady_hum"
    else:
        guess = "bird_chirp"

    print(f"Guess: {guess}")
    print(f"Correct: {guess == target}")
    return guess == target

if __name__ == "__main__":
    print("--- Feel AI: Audio Guessing Game Prototype ---")
    results = [guess_audio_game() for _ in range(3)]
    print(f"\nFinal Result: {results.count(True)}/3 Correct.")
