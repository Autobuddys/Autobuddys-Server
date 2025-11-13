import os
import tensorflow as tf
from django.conf import settings

_model1 = None


def get_model1():
    """
    Lazily load and cache the TensorFlow model for predicting SBP.
    """
    global _model1
    if _model1 is None:
        model_path = os.path.join(settings.MODELS, "SBP_Model.h5")
        print(f"[ML Loader] Loading model from {model_path}...")
        _model1 = tf.keras.models.load_model(model_path, compile=False)
        print("[ML Loader] Model loaded successfully.")
    return _model1
