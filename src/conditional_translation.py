
import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

CONDITION_FILE = os.path.join(DATASET_DIR, "conditions.csv")
INPUT_IMAGE = os.path.join(DATASET_DIR, "input_image.jpg")


def create_sample_image(path):
    """Create a sample landscape if no input image is provided."""
    height, width = 400, 600
    image = np.zeros((height, width, 3), dtype=np.uint8)

    # Sky gradient (BGR)
    for y in range(260):
        ratio = y / 260
        image[y, :, 0] = int(210 - 50 * ratio)
        image[y, :, 1] = int(170 - 30 * ratio)
        image[y, :, 2] = int(100 + 70 * ratio)

    # Ground
    image[260:, :] = (55, 125, 45)

    # Distant hills
    cv2.fillPoly(
        image,
        [np.array([[0, 270], [130, 160], [280, 270]], np.int32)],
        (90, 115, 65)
    )
    cv2.fillPoly(
        image,
        [np.array([[220, 270], [410, 145], [600, 270]], np.int32)],
        (70, 100, 55)
    )

    # Sun
    cv2.circle(image, (480, 75), 35, (80, 220, 255), -1)

    # Trees
    for x, y, size in [(90, 275, 45), (160, 285, 35),
                       (430, 285, 40), (535, 290, 48)]:
        cv2.rectangle(
            image, (x - 5, y), (x + 5, y + size),
            (35, 65, 25), -1
        )
        cv2.circle(image, (x, y - 10), size, (30, 95, 25), -1)

    cv2.imwrite(path, image)
    print("Sample landscape image created:", path)


def apply_condition(image, condition):
    """Apply a condition-specific visual transformation."""
    row = condition

    brightness = float(row["brightness"])
    contrast = float(row["contrast"])
    blue_tone = float(row["blue_tone"])

    # Adjust brightness and contrast
    result = cv2.convertScaleAbs(
        image, alpha=contrast, beta=(brightness - 1.0) * 100
    ).astype(np.float32)

    # OpenCV stores image channels in BGR order.
    if condition["condition"] == "sunset":
        result[:, :, 2] *= 1.0 + 0.45
        result[:, :, 1] *= 1.0 + 0.12
        result[:, :, 0] *= 1.0 - 0.20

    elif condition["condition"] == "night":
        result[:, :, 0] += 35 * blue_tone
        result[:, :, 1] += 10 * blue_tone

    elif condition["condition"] == "day":
        result[:, :, 1] += 5

    result = np.clip(result, 0, 255).astype(np.uint8)
    return result


def main():
    conditions = pd.read_csv(CONDITION_FILE)

    if not os.path.exists(INPUT_IMAGE):
        create_sample_image(INPUT_IMAGE)

    image = cv2.imread(INPUT_IMAGE)
    if image is None:
        raise ValueError(
            "Could not load input image. Check dataset/input_image.jpg."
        )

    outputs = {"original": image}
    analysis = []

    for _, condition in conditions.iterrows():
        translated = apply_condition(image, condition)
        name = str(condition["condition"])

        output_path = os.path.join(
            OUTPUT_DIR, f"{name}_output.png"
        )
        cv2.imwrite(output_path, translated)
        outputs[name] = translated

        analysis.append({
            "condition": name,
            "mean_brightness": round(float(np.mean(
                cv2.cvtColor(translated, cv2.COLOR_BGR2GRAY)
            )), 2),
            "mean_blue_channel": round(float(np.mean(
                translated[:, :, 0]
            )), 2),
            "output_file": f"{name}_output.png"
        })

        print(f"Generated {name} output: {output_path}")

    # Create a comparison figure
    names = list(outputs.keys())
    fig, axes = plt.subplots(1, len(names), figsize=(16, 4))

    for ax, name in zip(axes, names):
        rgb_image = cv2.cvtColor(outputs[name], cv2.COLOR_BGR2RGB)
        ax.imshow(rgb_image)
        ax.set_title(name.replace("_", " ").title())
        ax.axis("off")

    fig.suptitle("Conditional Image Translation Comparison")
    plt.tight_layout()

    comparison_path = os.path.join(
        RESULTS_DIR, "condition_comparison.png"
    )
    plt.savefig(comparison_path, dpi=200, bbox_inches="tight")
    plt.close()

    analysis_df = pd.DataFrame(analysis)
    analysis_path = os.path.join(
        RESULTS_DIR, "condition_analysis.csv"
    )
    analysis_df.to_csv(analysis_path, index=False)

    print("\nAll conditions processed successfully!")
    print("Analysis saved:", analysis_path)
    print("Comparison saved:", comparison_path)
    print("\nCondition analysis:")
    print(analysis_df.to_string(index=False))


if __name__ == "__main__":
    main()
