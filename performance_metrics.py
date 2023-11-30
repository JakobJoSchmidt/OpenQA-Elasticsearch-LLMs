import json
from google.colab import drive

# Mount Google Drive
drive.mount('/content/drive')

# Path to the JSON file in Google Drive
data_path = "/content/drive/MyDrive/Evaluation/qa_dataset.json"

# Load the data from the JSON file
with open(data_path, 'r') as file:
    qa_data = json.load(file)

# Initialize counters
TP = 0
FP = 0
FN = 0

for question in qa_data["questions"]:
    if question["answer_correct"]:
        TP += 1
    else:
        if question["answer_given"]:  # If an answer was provided by the system
            FP += 1
        else:  # If no answer was provided by the system
            FN += 1

# Calculate precision, recall, and F1
precision = TP / (TP + FP) if (TP + FP) != 0 else 0
recall = TP / (TP + FN) if (TP + FN) != 0 else 0
f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) != 0 else 0

print(f"TP: {TP:.4f}")
print(f"FP: {FP:.4f}")
print(f"FN: {FN:.4f}")
print()
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1 Score: {f1:.4f}")