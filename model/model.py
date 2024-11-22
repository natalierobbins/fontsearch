import tensorflow as tf
import numpy as np
from tqdm import tqdm
import logging
import h5py
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# load datasets
logger.info('[ ] loading datasets...')
X = np.load('X_norm.npy')
X = np.expand_dims(X, axis=-1)
y = np.load('./model/y.npy')
y = np.expand_dims(y, axis=-1)
logger.info('[x] loading datasets...')


# split
logger.info('[ ] splitting datasets...')
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2, # 80/20 split
    random_state=42
)

X_train, X_val, y_train, y_val = train_test_split(
    X_train, y_train, 
    test_size=0.2,  # 80/20 split
    random_state=42
)
logger.info('[x] splitting datasets...')

logger.info('[ ] instantiating model...')
model = Sequential([
    # input shape (93121, 448, 448, 1)
    tf.keras.Input(shape=(448, 448, 1)),
    Conv2D(32, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(512, activation='relu'),
    Dropout(0.5),
    Dense(128, activation='relu'),
    Dense(4038, activation='sigmoid')
    # output shape (93121, 4038)
])
logger.info('[x] instantiating model...')
logger.info('[ ] compiling model...')
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)
logger.info('[x] compiling model...')

acc_checkpont = tf.keras.callbacks.ModelCheckpoint(
    'checkpoint.model.keras',
    monitor='val_accuracy',
    save_best_only=True,
    save_weights_only=False
)

logger.info('[ ] starting train...')
model.fit(
    X_train, y_train,
    epochs=10,
    batch_size=32,
    validation_data=(X_val, y_val),
    verbose=2,
    callbacks=[acc_checkpont]
)
logger.info('[x] starting train...')


logger.info('[ ] saving model...')
model.save('initial.keras')
logger.info('[x] saving model...')