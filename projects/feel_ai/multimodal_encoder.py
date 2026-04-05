import os
import json
from vision import vision_to_tokens
from audio import audio_to_tags

class MultimodalEncoder:
    """
    Synthesizes vision and audio tokens into a single 'Sensory Packet'
    for LLMs to process the combined 'vibe' of an environment.
    """
    def __init__(self):
        self.packet_id = 0

    def generate_packet(self, image_path, audio_source):
        self.packet_id += 1

        vision_tokens = vision_to_tokens(image_path)
        audio_tags = audio_to_tags(audio_source)

        mood = self.classify_mood(vision_tokens, audio_tags)

        packet = {
            "packet_id": self.packet_id,
            "vision": vision_tokens,
            "audio": audio_tags,
            "mood_classification": mood
        }

        return packet

    def classify_mood(self, vision_tokens, audio_tags):
        """
        Simple heuristic classifier for 'mood' based on sensory data.
        """
        # Parse brightness from vision tokens
        # Example token: v00_ffffff_ff
        try:
            v_parts = vision_tokens.strip("<|>").replace("VISUAL_SENSE: ", "").split("|")
            brightness_values = [int(p.split("_")[2], 16) for p in v_parts if len(p.split("_")) > 2]
            avg_brightness = sum(brightness_values) / len(brightness_values) if brightness_values else 0
        except Exception:
            avg_brightness = 128

        # Parse energy from audio tags
        # Example tag: w00_ff
        try:
            a_parts = audio_tags.strip("<|>").replace("AUDIO_SENSE: ", "").split("|")
            energy_values = [int(p.split("_")[1], 16) for p in a_parts if len(p.split("_")) > 1]
            max_energy = max(energy_values) if energy_values else 0
            avg_energy = sum(energy_values) / len(energy_values) if energy_values else 0
        except Exception:
            max_energy = 0
            avg_energy = 0

        # Heuristic rules for mood
        if avg_brightness > 180 and avg_energy < 50:
            return "Serene / High Visibility"
        elif max_energy > 200:
            return "High Intensity / Alert"
        elif avg_brightness < 50 and avg_energy < 50:
            return "Gloomy / Low Energy"
        elif avg_brightness < 100 and max_energy > 150:
            return "Tense / Chaotic"
        else:
            return "Neutral / Stable"

if __name__ == "__main__":
    encoder = MultimodalEncoder()

    # Test with available artifacts
    test_image = "visual/aether_swarm_v1.png"
    if not os.path.exists(test_image):
        test_image = "visual/aether_3d_v1.png"

    if os.path.exists(test_image):
        print(f"--- Generating Multimodal Sensory Packet for {test_image} ---")
        packet = encoder.generate_packet(test_image, "heavy_impact")
        print(json.dumps(packet, indent=2))

        print("\n--- Test 2: Steady Hum ---")
        packet2 = encoder.generate_packet(test_image, "steady_hum")
        print(f"Mood: {packet2['mood_classification']}")
    else:
        print("No test images found in visual/ directory.")
