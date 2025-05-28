import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import time

print("Loading data...")
data_dict = pickle.load(open('./data.pickle', 'rb'))

data = np.asarray(data_dict['data'])
labels = np.asarray(data_dict['labels'])

print(f"Number of samples: {len(data)}")
print(f"Number of unique labels: {len(set(labels))}")

# Split the data
x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)

print("Training model...")
start_time = time.time()

model = RandomForestClassifier(n_estimators=100, min_samples_split=5)
model.fit(x_train, y_train)

end_time = time.time()
print(f"Training completed in {end_time - start_time:.2f} seconds")

# Evaluate the model
print("\nEvaluating model...")
y_predict = model.predict(x_test)

score = accuracy_score(y_predict, y_test)
print(f'Accuracy: {score*100:.2f}%')

# Save the model
print("\nSaving model...")
f = open('model.p', 'wb')
pickle.dump({'model': model}, f)
f.close()
print("Model saved as 'model.p'") 