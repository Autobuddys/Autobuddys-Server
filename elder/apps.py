from django.apps import AppConfig

# import os
# import tensorflow as tf
# from django.conf import settings
# import pickle
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import confusion_matrix, f1_score, accuracy_score


class ElderConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "elder"
    # MODEL_FILE_1 = os.path.join(settings.MODELS, "SBP_Model.h5")
    # model1 = tf.keras.models.load_model(MODEL_FILE_1, compile=False)

    # MODEL_FILE_2 = os.path.join(settings.MODELS, "DBP_Model.h5")
    # model2 = tf.keras.models.load_model(MODEL_FILE_2)
    # MODEL_FILE_3 = os.path.join(settings.MODELS, "fall_predict_model.sav")
    # model3 = pickle.load(open(MODEL_FILE_3, 'rb'))
