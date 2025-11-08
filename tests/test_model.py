import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
import numpy as np
from src.data_loader import load_iris_data
from src.model import IrisClassifier

from sklearn.linear_model import LogisticRegression

from src.data_loader import load_iris_data, get_feature_names, get_target_names
from src.model import IrisClassifier

class TestIrisClassifier:
    def setup_method(self):
        """Setup method that runs before each test"""
        self.X_train, self.X_test, self.y_train, self.y_test = load_iris_data(test_size=0.3, random_state=42)
        self.classifier = IrisClassifier()

    def test_model_initialization(self):
        """Test that model initializes correctly"""
        assert not self.classifier.is_trained
        assert self.classifier.model is not None

    def test_model_training(self):
        """Test model training functionality"""
        self.classifier.train(self.X_train, self.y_train)
        assert self.classifier.is_trained

    def test_model_prediction(self):
        """Test model prediction functionality"""
        self.classifier.train(self.X_train, self.y_train)
        predictions = self.classifier.predict(self.X_test[:5])
        assert len(predictions) == 5
        assert all(isinstance(pred, (np.int32, np.int64, int)) for pred in predictions)

    def test_model_evaluation(self):
        """Test model evaluation functionality"""
        self.classifier.train(self.X_train, self.y_train)
        accuracy, report = self.classifier.evaluate(self.X_test, self.y_test)

        assert 0 <= accuracy <= 1
        assert isinstance(report, str)
        assert "precision" in report.lower()

    def test_model_save_load(self, tmp_path):
        """Test model saving and loading"""
        self.classifier.train(self.X_train, self.y_train)

        # Save model
        save_path = tmp_path / "test_model.pkl"
        self.classifier.save_model(str(save_path))
        assert save_path.exists()

        # Load model
        new_classifier = IrisClassifier()
        new_classifier.load_model(str(save_path))
        assert new_classifier.is_trained

        # Verify predictions match
        original_pred = self.classifier.predict(self.X_test[:5])
        loaded_pred = new_classifier.predict(self.X_test[:5])
        assert np.array_equal(original_pred, loaded_pred)

def test_data_loading():
    """Test data loading functionality"""
    X_train, X_test, y_train, y_test = load_iris_data()

    assert X_train.shape[1] == 4  # 4 features
    assert len(np.unique(y_train)) == 3  # 3 classes
    assert len(X_train) + len(X_test) == 150  # Total samples





# --- Test 1: Data Loader - Check data shape and split ---
def test_data_loader_split():
    """
    Tests the load_iris_data function.
    Checks if the data is loaded and split into the correct shapes.
    """
    # Load data with a 20% test split (default)
    X_train, X_test, y_train, y_test = load_iris_data(test_size=0.2, random_state=42)

    # Total Iris samples = 150
    # 80% train = 120 samples
    # 20% test = 30 samples
    # 4 features
    
    # Check types
    assert isinstance(X_train, np.ndarray)
    assert isinstance(X_test, np.ndarray)
    assert isinstance(y_train, np.ndarray)
    assert isinstance(y_test, np.ndarray)

    # Check shapes
    assert X_train.shape == (120, 4)
    assert y_train.shape == (120,)
    assert X_test.shape == (30, 4)
    assert y_test.shape == (30,)

# --- Test 2: Model - Check training and prediction (Sanity Check) ---
def test_model_train_predict():
    """
    Tests the IrisClassifier's train and predict methods.
    This is a "sanity check" to ensure the model can be trained
    and can produce a prediction without errors.
    """
    # 1. Load data (we only need training data for this)
    X_train, _, y_train, _ = load_iris_data()
    
    # 2. Initialize classifier
    classifier = IrisClassifier()
    
    # 3. Check if it's not trained initially
    assert classifier.is_trained == False
    
    # 4. Train the model
    classifier.train(X_train, y_train)
    
    # 5. Check if it's marked as trained
    assert classifier.is_trained == True
    
    # 6. Make a prediction on a single sample
    # Use the first sample from the training set
    sample = X_train[0:1] # Keep it as a 2D array
    prediction = classifier.predict(sample)
    
    # 7. Check the prediction output
    assert prediction is not None
    assert isinstance(prediction, np.ndarray)
    assert prediction.shape == (1,)

# --- Test 3: Model - Check Save and Load functionality ---
def test_model_save_load(tmp_path):
    """
    Tests that the IrisClassifier can be saved to a file
    and then loaded back correctly.
    The 'tmp_path' fixture is provided by pytest to create
    a temporary directory.
    """
    # 1. Create a dummy trained model
    X_train, _, y_train, _ = load_iris_data()
    classifier_to_save = IrisClassifier()
    classifier_to_save.train(X_train, y_train)
    
    # 2. Define a temporary file path
    model_path = os.path.join(tmp_path, "test_model.pkl")
    
    # 3. Save the model
    classifier_to_save.save_model(model_path)
    
    # 4. Check if the file was actually created
    assert os.path.exists(model_path)
    
    # 5. Initialize a new, untrained classifier
    classifier_to_load = IrisClassifier()
    assert classifier_to_load.is_trained == False
    
    # 6. Load the model from the file
    classifier_to_load.load_model(model_path)
    
    # 7. Check if the loaded classifier is now marked as trained
    assert classifier_to_load.is_trained == True
    
    # 8. Verify it can make the same prediction
    sample = X_train[0:1]
    pred_original = classifier_to_save.predict(sample)
    pred_loaded = classifier_to_load.predict(sample)
    
    assert pred_original == pred_loaded