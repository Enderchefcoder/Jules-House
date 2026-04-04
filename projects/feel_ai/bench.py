import random
import time
from datetime import datetime

# Logic from audio.py
def audio_to_tags(audio_source):
    tags = []
    if audio_source == "heavy_impact":
        energy_pattern = [random.randint(0x80, 0xFF) for _ in range(3)] + [random.randint(0, 0x40) for _ in range(4)]
    elif audio_source == "steady_hum":
        base = random.randint(0x30, 0x60)
        energy_pattern = [base + random.randint(-5, 5) for _ in range(7)]
    elif audio_source == "bird_chirp":
        energy_pattern = [random.randint(0, 0x10) if i % 2 == 0 else random.randint(0x20, 0x50) for i in range(7)]
    else:
        energy_pattern = [random.randint(0, 255) for _ in range(7)]

    for i, level in enumerate(energy_pattern):
        tags.append(f"w{i:02d}_{level:02x}")
    return f"<|AUDIO_SENSE: {'|'.join(tags)} |>"

def guess_audio(tags):
    tag_parts = tags.strip("<|>").replace("AUDIO_SENSE: ", "").split("|")
    energies = [int(p.split("_")[1], 16) for p in tag_parts]
    max_e = max(energies)
    avg_e = sum(energies) / len(energies)
    variance = max_e - min(energies)

    if max_e > 200:
        return "heavy_impact"
    elif variance < 15:
        return "steady_hum"
    else:
        return "bird_chirp"

def run_tokbench(n=500):
    audio_types = ["heavy_impact", "steady_hum", "bird_chirp"]
    correct = 0
    start_time = time.time()

    results_summary = {t: {"total": 0, "correct": 0} for t in audio_types}

    for _ in range(n):
        target = random.choice(audio_types)
        tags = audio_to_tags(target)
        guess = guess_audio(tags)

        results_summary[target]["total"] += 1
        if guess == target:
            correct += 1
            results_summary[target]["correct"] += 1

    end_time = time.time()
    accuracy = (correct / n) * 100
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report = f"## TokBench Results - {timestamp}\n"
    report += f"- **Total Samples**: {n}\n"
    report += f"- **Overall Accuracy**: {accuracy:.2f}%\n"
    report += f"- **Duration**: {end_time - start_time:.4f}s\n"
    report += "| Audio Type | Total | Correct | Accuracy |\n"
    report += "|---|---|---|---|\n"
    for t, stats in results_summary.items():
        acc = (stats["correct"] / stats["total"]) * 100 if stats["total"] > 0 else 0
        report += f"| {t} | {stats['total']} | {stats['correct']} | {acc:.2f}% |\n"
    report += "\n"

    return report

if __name__ == "__main__":
    print("Running TokBench (500 samples)...")
    report = run_tokbench(500)

    with open("projects/feel_ai/bench.md", "a") as f:
        f.write(report)

    print("Benchmark complete. Results saved to projects/feel_ai/bench.md")
