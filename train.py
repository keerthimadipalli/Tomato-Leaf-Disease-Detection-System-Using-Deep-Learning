"""
=============================================================
  TOMATO DISEASE DETECTOR — TRAINING SCRIPT
  Uses MobileNetV2 Transfer Learning for high accuracy
  Run: python train.py
=============================================================
"""

import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models, callbacks
from tensorflow.keras.optimizers import Adam
import os
import json
import matplotlib.pyplot as plt

# ─────────────────────────────────────────────────────────────
# PATHS
# ─────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
TRAIN_PATH = os.path.join(BASE_DIR, "dataset", "Tomato", "Train")
VAL_PATH   = os.path.join(BASE_DIR, "dataset", "Tomato", "Val")
MODEL_DIR  = os.path.join(BASE_DIR, "model")
os.makedirs(MODEL_DIR, exist_ok=True)

IMG_SIZE   = (224, 224)
BATCH_SIZE = 32
EPOCHS     = 25

# ─────────────────────────────────────────────────────────────
# DATA AUGMENTATION
# ─────────────────────────────────────────────────────────────
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    zoom_range=0.3,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    vertical_flip=True,
    brightness_range=[0.7, 1.3],
    shear_range=0.2,
    fill_mode='nearest'
)

val_datagen = ImageDataGenerator(rescale=1./255)

train_data = train_datagen.flow_from_directory(
    TRAIN_PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=True
)

val_data = val_datagen.flow_from_directory(
    VAL_PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=False
)

NUM_CLASSES = train_data.num_classes
print(f"\n✅ Found {NUM_CLASSES} classes: {list(train_data.class_indices.keys())}")

# Save class indices so the app knows the order
with open(os.path.join(MODEL_DIR, "class_indices.json"), "w") as f:
    json.dump(train_data.class_indices, f, indent=2)
print("✅ Saved class_indices.json")

# ─────────────────────────────────────────────────────────────
# MODEL — MobileNetV2 Transfer Learning
# ─────────────────────────────────────────────────────────────
base_model = MobileNetV2(
    weights='imagenet',
    include_top=False,
    input_shape=(224, 224, 3)
)

# Freeze base model first
base_model.trainable = False

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.BatchNormalization(),
    layers.Dense(256, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(NUM_CLASSES, activation='softmax')
])

model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# ─────────────────────────────────────────────────────────────
# PHASE 1 TRAINING — Frozen base (10 epochs)
# ─────────────────────────────────────────────────────────────
print("\n🚀 PHASE 1: Training top layers only...\n")

cb_list = [
    callbacks.EarlyStopping(monitor='val_accuracy', patience=5, restore_best_weights=True),
    callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.3, patience=3, min_lr=1e-6),
    callbacks.ModelCheckpoint(
        os.path.join(MODEL_DIR, "best_model.h5"),
        monitor='val_accuracy',
        save_best_only=True,
        verbose=1
    )
]

history1 = model.fit(
    train_data,
    validation_data=val_data,
    epochs=10,
    callbacks=cb_list
)

# ─────────────────────────────────────────────────────────────
# PHASE 2 FINE-TUNING — Unfreeze last 50 layers
# ─────────────────────────────────────────────────────────────
print("\n🔥 PHASE 2: Fine-tuning last layers...\n")

base_model.trainable = True
for layer in base_model.layers[:-50]:
    layer.trainable = False

model.compile(
    optimizer=Adam(learning_rate=1e-4),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

history2 = model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS,
    callbacks=cb_list
)

# ─────────────────────────────────────────────────────────────
# SAVE MODEL
# ─────────────────────────────────────────────────────────────
model.save(os.path.join(MODEL_DIR, "tomato_disease_model.h5"))
print("\n✅ Model saved to model/tomato_disease_model.h5")

# ─────────────────────────────────────────────────────────────
# SAVE TRAINING PLOT
# ─────────────────────────────────────────────────────────────
# Combine both histories
acc  = history1.history['accuracy'] + history2.history['accuracy']
val_acc = history1.history['val_accuracy'] + history2.history['val_accuracy']
loss = history1.history['loss'] + history2.history['loss']
val_loss = history1.history['val_loss'] + history2.history['val_loss']

plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(acc, label='Train Accuracy')
plt.plot(val_acc, label='Val Accuracy')
plt.title('Accuracy')
plt.xlabel('Epoch')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(loss, label='Train Loss')
plt.plot(val_loss, label='Val Loss')
plt.title('Loss')
plt.xlabel('Epoch')
plt.legend()

plt.tight_layout()
plt.savefig(os.path.join(MODEL_DIR, "training_history.png"))
print("✅ Training plot saved to model/training_history.png")
print("\n🎉 TRAINING COMPLETE!")
