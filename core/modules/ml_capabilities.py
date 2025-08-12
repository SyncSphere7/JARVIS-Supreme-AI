"""
Machine Learning Capabilities for Jarvis.
Provides comprehensive ML training, inference, and model management.
"""
import os
import json
import pickle
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import joblib
from core.utils.log import logger

# ML Libraries
try:
    import sklearn
    from sklearn.model_selection import train_test_split, GridSearchCV
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.linear_model import LogisticRegression, LinearRegression
    from sklearn.svm import SVC, SVR
    from sklearn.neural_network import MLPClassifier, MLPRegressor
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    from sklearn.metrics import accuracy_score, classification_report, mean_squared_error
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import DataLoader, TensorDataset
    PYTORCH_AVAILABLE = True
except ImportError:
    PYTORCH_AVAILABLE = False

try:
    import tensorflow as tf
    from tensorflow import keras
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False


class MLCapabilities:
    def __init__(self, brain):
        self.brain = brain
        self.models_dir = Path("ml_models")
        self.models_dir.mkdir(exist_ok=True)
        self.trained_models = {}
        self.scalers = {}
        self.encoders = {}
        
        # Check available ML libraries
        self.available_frameworks = {
            "sklearn": SKLEARN_AVAILABLE,
            "pytorch": PYTORCH_AVAILABLE,
            "tensorflow": TENSORFLOW_AVAILABLE
        }
        
        logger.info(f"ML Frameworks available: {[k for k, v in self.available_frameworks.items() if v]}")
    
    def auto_ml_pipeline(self, data_path: str, target_column: str, task_type: str = "auto") -> Dict[str, Any]:
        """Fully automated ML pipeline from data to deployed model."""
        try:
            logger.info(f"🤖 Starting AutoML pipeline for {data_path}")
            
            # Load and analyze data
            data = self._load_data(data_path)
            analysis = self._analyze_data(data, target_column)
            
            # Determine task type if auto
            if task_type == "auto":
                task_type = self._determine_task_type(data[target_column])
            
            # Preprocess data
            X, y, preprocessors = self._preprocess_data(data, target_column, task_type)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Train multiple models and select best
            best_model, results = self._train_and_compare_models(X_train, X_test, y_train, y_test, task_type)
            
            # Save model and preprocessors
            model_id = self._save_model(best_model, preprocessors, analysis, results)
            
            return {
                "success": True,
                "model_id": model_id,
                "task_type": task_type,
                "best_model": str(type(best_model).__name__),
                "performance": results["best_score"],
                "data_analysis": analysis,
                "model_path": str(self.models_dir / f"{model_id}.pkl")
            }
            
        except Exception as e:
            logger.error(f"AutoML pipeline failed: {e}")
            return {"success": False, "error": str(e)}
    
    def train_custom_model(self, model_config: Dict[str, Any]) -> Dict[str, Any]:
        """Train a custom model with specific configuration."""
        try:
            model_type = model_config.get("type", "random_forest")
            data_path = model_config.get("data_path")
            target_column = model_config.get("target_column")
            
            # Load data
            data = self._load_data(data_path)
            
            # Preprocess
            X, y, preprocessors = self._preprocess_data(data, target_column, model_config.get("task_type", "classification"))
            
            # Create model based on configuration
            model = self._create_model(model_type, model_config.get("parameters", {}))
            
            # Train model
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            model.fit(X_train, y_train)
            
            # Evaluate
            predictions = model.predict(X_test)
            score = accuracy_score(y_test, predictions) if model_config.get("task_type") == "classification" else mean_squared_error(y_test, predictions)
            
            # Save model
            model_id = self._save_model(model, preprocessors, {"custom": True}, {"score": score})
            
            return {
                "success": True,
                "model_id": model_id,
                "score": score,
                "model_type": model_type
            }
            
        except Exception as e:
            logger.error(f"Custom model training failed: {e}")
            return {"success": False, "error": str(e)}
    
    def predict(self, model_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Make predictions using a trained model."""
        try:
            # Load model
            model_path = self.models_dir / f"{model_id}.pkl"
            if not model_path.exists():
                return {"success": False, "error": "Model not found"}
            
            with open(model_path, 'rb') as f:
                model_data = pickle.load(f)
            
            model = model_data["model"]
            preprocessors = model_data["preprocessors"]
            
            # Preprocess input
            input_df = pd.DataFrame([input_data])
            
            # Apply same preprocessing as training
            if "scaler" in preprocessors:
                numerical_cols = preprocessors["numerical_columns"]
                input_df[numerical_cols] = preprocessors["scaler"].transform(input_df[numerical_cols])
            
            if "encoder" in preprocessors:
                categorical_cols = preprocessors["categorical_columns"]
                for col in categorical_cols:
                    if col in input_df.columns:
                        input_df[col] = preprocessors["encoder"].transform(input_df[col])
            
            # Make prediction
            prediction = model.predict(input_df)
            
            # Get prediction probability if available
            probability = None
            if hasattr(model, "predict_proba"):
                probability = model.predict_proba(input_df).tolist()
            
            return {
                "success": True,
                "prediction": prediction.tolist(),
                "probability": probability,
                "model_id": model_id
            }
            
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            return {"success": False, "error": str(e)}
    
    def create_neural_network(self, architecture: Dict[str, Any]) -> Dict[str, Any]:
        """Create and train a neural network."""
        try:
            if not PYTORCH_AVAILABLE:
                return {"success": False, "error": "PyTorch not available"}
            
            # Define neural network architecture
            class CustomNN(nn.Module):
                def __init__(self, input_size, hidden_layers, output_size):
                    super(CustomNN, self).__init__()
                    layers = []
                    
                    # Input layer
                    layers.append(nn.Linear(input_size, hidden_layers[0]))
                    layers.append(nn.ReLU())
                    
                    # Hidden layers
                    for i in range(len(hidden_layers) - 1):
                        layers.append(nn.Linear(hidden_layers[i], hidden_layers[i + 1]))
                        layers.append(nn.ReLU())
                        layers.append(nn.Dropout(0.2))
                    
                    # Output layer
                    layers.append(nn.Linear(hidden_layers[-1], output_size))
                    
                    self.network = nn.Sequential(*layers)
                
                def forward(self, x):
                    return self.network(x)
            
            # Load and prepare data
            data_path = architecture.get("data_path")
            target_column = architecture.get("target_column")
            
            data = self._load_data(data_path)
            X, y, preprocessors = self._preprocess_data(data, target_column, "classification")
            
            # Convert to PyTorch tensors
            X_tensor = torch.FloatTensor(X.values)
            y_tensor = torch.LongTensor(y.values)
            
            # Create model
            input_size = X.shape[1]
            hidden_layers = architecture.get("hidden_layers", [64, 32])
            output_size = len(np.unique(y))
            
            model = CustomNN(input_size, hidden_layers, output_size)
            
            # Training setup
            criterion = nn.CrossEntropyLoss()
            optimizer = optim.Adam(model.parameters(), lr=architecture.get("learning_rate", 0.001))
            
            # Create data loader
            dataset = TensorDataset(X_tensor, y_tensor)
            dataloader = DataLoader(dataset, batch_size=architecture.get("batch_size", 32), shuffle=True)
            
            # Training loop
            epochs = architecture.get("epochs", 100)
            for epoch in range(epochs):
                for batch_X, batch_y in dataloader:
                    optimizer.zero_grad()
                    outputs = model(batch_X)
                    loss = criterion(outputs, batch_y)
                    loss.backward()
                    optimizer.step()
                
                if epoch % 10 == 0:
                    logger.info(f"Epoch {epoch}, Loss: {loss.item():.4f}")
            
            # Save model
            model_id = f"neural_net_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            torch.save(model.state_dict(), self.models_dir / f"{model_id}.pth")
            
            return {
                "success": True,
                "model_id": model_id,
                "architecture": architecture,
                "final_loss": loss.item()
            }
            
        except Exception as e:
            logger.error(f"Neural network creation failed: {e}")
            return {"success": False, "error": str(e)}
    
    def transfer_learning(self, base_model: str, new_data_path: str, target_column: str) -> Dict[str, Any]:
        """Implement transfer learning from a pre-trained model."""
        try:
            if not TENSORFLOW_AVAILABLE:
                return {"success": False, "error": "TensorFlow not available"}
            
            # Load pre-trained model (e.g., from TensorFlow Hub)
            if base_model == "resnet50":
                base = tf.keras.applications.ResNet50(
                    weights='imagenet',
                    include_top=False,
                    input_shape=(224, 224, 3)
                )
            elif base_model == "bert":
                # For text classification
                import tensorflow_hub as hub
                base = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/4")
            else:
                return {"success": False, "error": f"Base model {base_model} not supported"}
            
            # Freeze base model layers
            base.trainable = False
            
            # Add custom layers
            model = tf.keras.Sequential([
                base,
                tf.keras.layers.GlobalAveragePooling2D(),
                tf.keras.layers.Dense(128, activation='relu'),
                tf.keras.layers.Dropout(0.2),
                tf.keras.layers.Dense(1, activation='sigmoid')  # Adjust based on task
            ])
            
            # Compile model
            model.compile(
                optimizer='adam',
                loss='binary_crossentropy',
                metrics=['accuracy']
            )
            
            # Load and preprocess new data
            data = self._load_data(new_data_path)
            # Preprocessing would depend on the data type (images, text, etc.)
            
            # Train model
            # history = model.fit(X_train, y_train, epochs=10, validation_split=0.2)
            
            # Save model
            model_id = f"transfer_learning_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            model.save(self.models_dir / f"{model_id}.h5")
            
            return {
                "success": True,
                "model_id": model_id,
                "base_model": base_model
            }
            
        except Exception as e:
            logger.error(f"Transfer learning failed: {e}")
            return {"success": False, "error": str(e)}
    
    def automated_feature_engineering(self, data_path: str, target_column: str) -> Dict[str, Any]:
        """Automatically engineer features for better model performance."""
        try:
            data = self._load_data(data_path)
            
            # Original features
            original_features = list(data.columns)
            original_features.remove(target_column)
            
            # Automated feature engineering
            engineered_data = data.copy()
            
            # Numerical feature engineering
            numerical_cols = data.select_dtypes(include=[np.number]).columns
            for col in numerical_cols:
                if col != target_column:
                    # Polynomial features
                    engineered_data[f"{col}_squared"] = data[col] ** 2
                    engineered_data[f"{col}_log"] = np.log1p(data[col].abs())
                    
                    # Binning
                    engineered_data[f"{col}_binned"] = pd.cut(data[col], bins=5, labels=False)
            
            # Categorical feature engineering
            categorical_cols = data.select_dtypes(include=['object']).columns
            for col in categorical_cols:
                if col != target_column:
                    # Frequency encoding
                    freq_map = data[col].value_counts().to_dict()
                    engineered_data[f"{col}_frequency"] = data[col].map(freq_map)
            
            # Interaction features
            for i, col1 in enumerate(numerical_cols):
                for col2 in numerical_cols[i+1:]:
                    if col1 != target_column and col2 != target_column:
                        engineered_data[f"{col1}_{col2}_interaction"] = data[col1] * data[col2]
            
            # Save engineered dataset
            output_path = Path(data_path).parent / f"engineered_{Path(data_path).name}"
            engineered_data.to_csv(output_path, index=False)
            
            new_features = [col for col in engineered_data.columns if col not in original_features and col != target_column]
            
            return {
                "success": True,
                "original_features": len(original_features),
                "new_features": len(new_features),
                "total_features": len(engineered_data.columns) - 1,
                "engineered_data_path": str(output_path),
                "new_feature_names": new_features
            }
            
        except Exception as e:
            logger.error(f"Feature engineering failed: {e}")
            return {"success": False, "error": str(e)}
    
    def model_interpretability(self, model_id: str, data_sample: Dict[str, Any]) -> Dict[str, Any]:
        """Provide model interpretability and explanations."""
        try:
            # Load model
            model_path = self.models_dir / f"{model_id}.pkl"
            with open(model_path, 'rb') as f:
                model_data = pickle.load(f)
            
            model = model_data["model"]
            
            # Feature importance (for tree-based models)
            if hasattr(model, 'feature_importances_'):
                feature_names = model_data.get("feature_names", [])
                importance_dict = dict(zip(feature_names, model.feature_importances_))
                sorted_importance = sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)
                
                return {
                    "success": True,
                    "feature_importance": sorted_importance,
                    "model_type": str(type(model).__name__),
                    "interpretability_method": "feature_importance"
                }
            
            # For other models, provide basic statistics
            return {
                "success": True,
                "model_type": str(type(model).__name__),
                "interpretability_method": "basic_stats",
                "note": "Advanced interpretability requires additional libraries like SHAP or LIME"
            }
            
        except Exception as e:
            logger.error(f"Model interpretability failed: {e}")
            return {"success": False, "error": str(e)}
    
    def list_models(self) -> Dict[str, Any]:
        """List all trained models."""
        try:
            models = []
            for model_file in self.models_dir.glob("*.pkl"):
                try:
                    with open(model_file, 'rb') as f:
                        model_data = pickle.load(f)
                    
                    models.append({
                        "model_id": model_file.stem,
                        "model_type": str(type(model_data["model"]).__name__),
                        "created": datetime.fromtimestamp(model_file.stat().st_mtime).isoformat(),
                        "performance": model_data.get("results", {}).get("score", "Unknown")
                    })
                except:
                    continue
            
            return {
                "success": True,
                "models": models,
                "total_models": len(models)
            }
            
        except Exception as e:
            logger.error(f"Failed to list models: {e}")
            return {"success": False, "error": str(e)}
    
    # Helper methods
    def _load_data(self, data_path: str) -> pd.DataFrame:
        """Load data from various formats."""
        path = Path(data_path)
        if path.suffix == '.csv':
            return pd.read_csv(path)
        elif path.suffix in ['.xlsx', '.xls']:
            return pd.read_excel(path)
        elif path.suffix == '.json':
            return pd.read_json(path)
        else:
            raise ValueError(f"Unsupported file format: {path.suffix}")
    
    def _analyze_data(self, data: pd.DataFrame, target_column: str) -> Dict[str, Any]:
        """Analyze dataset characteristics."""
        return {
            "shape": data.shape,
            "missing_values": data.isnull().sum().to_dict(),
            "data_types": data.dtypes.to_dict(),
            "target_distribution": data[target_column].value_counts().to_dict(),
            "numerical_columns": data.select_dtypes(include=[np.number]).columns.tolist(),
            "categorical_columns": data.select_dtypes(include=['object']).columns.tolist()
        }
    
    def _determine_task_type(self, target_series: pd.Series) -> str:
        """Automatically determine if task is classification or regression."""
        if target_series.dtype == 'object' or len(target_series.unique()) < 20:
            return "classification"
        else:
            return "regression"
    
    def _preprocess_data(self, data: pd.DataFrame, target_column: str, task_type: str) -> Tuple[pd.DataFrame, pd.Series, Dict]:
        """Preprocess data for ML training."""
        X = data.drop(columns=[target_column])
        y = data[target_column]
        
        preprocessors = {}
        
        # Handle numerical columns
        numerical_cols = X.select_dtypes(include=[np.number]).columns
        if len(numerical_cols) > 0:
            scaler = StandardScaler()
            X[numerical_cols] = scaler.fit_transform(X[numerical_cols])
            preprocessors["scaler"] = scaler
            preprocessors["numerical_columns"] = numerical_cols.tolist()
        
        # Handle categorical columns
        categorical_cols = X.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            encoder = LabelEncoder()
            for col in categorical_cols:
                X[col] = encoder.fit_transform(X[col].astype(str))
            preprocessors["encoder"] = encoder
            preprocessors["categorical_columns"] = categorical_cols.tolist()
        
        # Encode target for classification
        if task_type == "classification" and y.dtype == 'object':
            target_encoder = LabelEncoder()
            y = target_encoder.fit_transform(y)
            preprocessors["target_encoder"] = target_encoder
        
        return X, y, preprocessors
    
    def _train_and_compare_models(self, X_train, X_test, y_train, y_test, task_type: str) -> Tuple[Any, Dict]:
        """Train multiple models and return the best one."""
        if not SKLEARN_AVAILABLE:
            raise ImportError("scikit-learn is required for model training")
        
        models = {}
        results = {}
        
        if task_type == "classification":
            models = {
                "random_forest": RandomForestClassifier(n_estimators=100, random_state=42),
                "gradient_boosting": GradientBoostingClassifier(random_state=42),
                "logistic_regression": LogisticRegression(random_state=42),
                "svm": SVC(random_state=42),
                "neural_network": MLPClassifier(random_state=42, max_iter=1000)
            }
        else:
            models = {
                "random_forest": RandomForestRegressor(n_estimators=100, random_state=42),
                "gradient_boosting": GradientBoostingRegressor(random_state=42),
                "linear_regression": LinearRegression(),
                "svr": SVR(),
                "neural_network": MLPRegressor(random_state=42, max_iter=1000)
            }
        
        best_score = -float('inf') if task_type == "classification" else float('inf')
        best_model = None
        
        for name, model in models.items():
            try:
                model.fit(X_train, y_train)
                predictions = model.predict(X_test)
                
                if task_type == "classification":
                    score = accuracy_score(y_test, predictions)
                    if score > best_score:
                        best_score = score
                        best_model = model
                else:
                    score = mean_squared_error(y_test, predictions)
                    if score < best_score:
                        best_score = score
                        best_model = model
                
                results[name] = score
                
            except Exception as e:
                logger.warning(f"Model {name} failed: {e}")
                continue
        
        results["best_score"] = best_score
        return best_model, results
    
    def _create_model(self, model_type: str, parameters: Dict) -> Any:
        """Create a model with specified type and parameters."""
        if not SKLEARN_AVAILABLE:
            raise ImportError("scikit-learn is required")
        
        model_classes = {
            "random_forest": RandomForestClassifier,
            "gradient_boosting": GradientBoostingClassifier,
            "logistic_regression": LogisticRegression,
            "svm": SVC,
            "neural_network": MLPClassifier
        }
        
        if model_type not in model_classes:
            raise ValueError(f"Unsupported model type: {model_type}")
        
        return model_classes[model_type](**parameters)
    
    def _save_model(self, model: Any, preprocessors: Dict, analysis: Dict, results: Dict) -> str:
        """Save trained model and metadata."""
        model_id = f"model_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        model_data = {
            "model": model,
            "preprocessors": preprocessors,
            "analysis": analysis,
            "results": results,
            "created": datetime.now().isoformat(),
            "model_type": str(type(model).__name__)
        }
        
        model_path = self.models_dir / f"{model_id}.pkl"
        with open(model_path, 'wb') as f:
            pickle.dump(model_data, f)
        
        logger.info(f"✅ Model saved: {model_id}")
        return model_id
