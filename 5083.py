# -*- coding: utf-8 -*-
"""5083.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1_mj-x0kese5qHcxL5vJ9i5JVcmTyhfFJ
"""

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from keras.datasets import mnist
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
import numpy as np

def normalize(train):
    # convert from integers to floats
    train_norm = train.astype('float32')


    # normalize to range 0-1
    train_norm = train_norm / 255.0

    # return normalized images
    return train_norm

# Wrapper function to convert labels to one hot encoding
def to_one_hot(train_labels, test_labels):
    encoder = OneHotEncoder(categories='auto')
    train_labels_encoded = encoder.fit_transform(train_labels.reshape(-1, 1)).toarray()
    test_labels_encoded = encoder.transform(test_labels.reshape(-1, 1)).toarray()
    return train_labels_encoded, test_labels_encoded

# Define the CNN model
cnn_model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(100, activation='relu'),
    Dense(10, activation='softmax')
])

# Compile the CNN model
cnn_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Define the pipeline steps
pipeline_steps = [
    ('preprocessing', FunctionTransformer(func=normalize, validate=False)),
    ('cnn_model', cnn_model)
    ]

# Create the pipeline
pipeline = Pipeline(pipeline_steps)

# Load the MNIST dataset
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Reshape and normalize the data
x_train = np.expand_dims(x_train, axis=-1)
x_test = np.expand_dims(x_test, axis=-1)
x_train = normalize(x_train)
x_test = normalize(x_test)
# Convert labels to one hot encoding
y_train, y_test = to_one_hot(y_train, y_test)

# Train-test split
x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.1, random_state=42)

# Fit the pipeline
pipeline.fit(x_train, y_train, cnn_model__epochs=5, cnn_model__batch_size=64, cnn_model__validation_data=(x_val, y_val))

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# Predict labels using the fitted pipeline
y_pred = pipeline.predict(x_test)

# Convert y_pred to one-hot encoded format
y_pred_onehot = to_categorical(np.argmax(y_pred, axis=1), num_classes=10)

# Calculate precision, recall, and F1 score
precision = precision_score(y_test, y_pred_onehot, average='macro')
recall = recall_score(y_test, y_pred_onehot, average='macro')
f1 = f1_score(y_test, y_pred_onehot, average='macro')

# Create a confusion matrix
conf_matrix = confusion_matrix(np.argmax(y_test, axis=1), np.argmax(y_pred_onehot, axis=1))

print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)
print("Confusion Matrix:\n", conf_matrix)

with open("metrics.txt", "w") as f:
    f.write(f"F1 Score = {f1.round(2)}, Presicison: {precision.round(2)}, Recall: {recall.round(2)}, confusion matrix: {conf_matrix}")

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

# Calculate the confusion matrix
conf_matrix = confusion_matrix(y_test.argmax(axis=1), y_pred.argmax(axis=1))

# Plot the confusion matrix
plt.figure(figsize=(10, 8))
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", xticklabels=range(10), yticklabels=range(10))
plt.xlabel('Predicted labels')
plt.ylabel('True labels')
plt.title('Confusion Matrix')
plt.show()
plt.savefig("model_results.png", dpi=120)