import os, json
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models, callbacks
from tensorflow.keras.optimizers import Adam

BASE_DIR   = r"C:\Users\gakil\OneDrive\Desktop\TomatoAI"
TRAIN_PATH = os.path.join(BASE_DIR, "Tomato", "Train")
VAL_PATH   = os.path.join(BASE_DIR, "Tomato", "Val")
MODEL_DIR  = os.path.join(BASE_DIR, "model")
os.makedirs(MODEL_DIR, exist_ok=True)

print("Train path:", TRAIN_PATH)
print("Exists:", os.path.exists(TRAIN_PATH))

if not os.path.exists(TRAIN_PATH):
    print("ERROR: Folder not found!")
    exit(1)

train_gen = ImageDataGenerator(rescale=1./255, rotation_range=30, zoom_range=0.2, horizontal_flip=True)
val_gen   = ImageDataGenerator(rescale=1./255)

train_data = train_gen.flow_from_directory(TRAIN_PATH, target_size=(224,224), batch_size=32, class_mode='categorical')
val_data   = val_gen.flow_from_directory(VAL_PATH, target_size=(224,224), batch_size=32, class_mode='categorical')

with open(os.path.join(MODEL_DIR, "class_indices.json"), "w") as f:
    json.dump(train_data.class_indices, f)
print("Classes saved:", train_data.class_indices)

base = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224,224,3))
base.trainable = False
model = models.Sequential([base, layers.GlobalAveragePooling2D(), layers.Dense(256, activation='relu'), layers.Dropout(0.4), layers.Dense(train_data.num_classes, activation='softmax')])
model.compile(optimizer=Adam(0.001), loss='categorical_crossentropy', metrics=['accuracy'])

cb = [callbacks.EarlyStopping(patience=5, restore_best_weights=True), callbacks.ModelCheckpoint(os.path.join(MODEL_DIR, "tomato_disease_model.h5"), save_best_only=True)]
model.fit(train_data, validation_data=val_data, epochs=20, callbacks=cb, verbose=1)
print("DONE! Run: python app.py")
