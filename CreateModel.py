import joblib
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from PoseDatasets import Dataset
from LoadVideo import FramesMeasured
from sklearn.ensemble import RandomForestClassifier

Input, Output = Dataset.getFlattenedDataset('pose_data.csv',framesPerSample=FramesMeasured)
x_train, x_test, y_train, y_test = train_test_split(Input,Output,test_size=.3, random_state=42)

model = RandomForestClassifier(
    n_estimators=200,         # Use 200 trees
    n_jobs=-1,                # Use all available CPU cores
)

model.fit(x_train, y_train)

#Test
y_pred = model.predict(x_test)
accuracy = accuracy_score(y_test, y_pred)
print(accuracy)

joblib.dump(model, "random_forest_LiveTimeArya.pkl")