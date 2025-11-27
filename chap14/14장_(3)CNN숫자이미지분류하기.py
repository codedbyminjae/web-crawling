# mnist CNN 전체 실행 코드 (TensorFlow 2.x 호환 버전)

from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

import matplotlib.pyplot as plt
import numpy as np
import sys
from PIL import Image
import os

# 1) MNIST 데이터 로드
(X_train_0, Y_train_0), (X_test_0, Y_test_0) = mnist.load_data()

print("학습 데이터 수 : %d" % (X_train_0.shape[0]))
print("평가 데이터 수 : %d" % (X_test_0.shape[0]))

# 2) 이미지 하나 출력
plt.imshow(X_train_0[0], cmap='Greys')
plt.show()

print("class : %d " % (Y_train_0[0]))

# 이미지 픽셀 값 출력
for x in X_train_0[0]:
    for i in x:
        sys.stdout.write('%4d' % i)
    sys.stdout.write('\n')

# 3) 입력값 reshape + 정규화
X_train = X_train_0.reshape(X_train_0.shape[0], 28, 28, 1).astype('float32') / 255
X_test  = X_test_0.reshape(X_test_0.shape[0], 28, 28, 1).astype('float32') / 255

# 4) 라벨 one-hot encoding
Y_train = to_categorical(Y_train_0, 10)
Y_test  = to_categorical(Y_test_0, 10)

print(Y_train[0])  # 확인용 출력

# 5) CNN 모델 구성
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), input_shape=(28, 28, 1), activation='relu'))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(10, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# 6) 모델 저장 경로 생성
MODEL_DIR = './14장_data/model/'
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

modelpath = MODEL_DIR + "{epoch:02d}-{val_loss:.4f}.hdf5"
checkpointer = ModelCheckpoint(filepath=modelpath, monitor='val_loss', verbose=1, save_best_only=True)
early_stopping_callback = EarlyStopping(monitor='val_loss', patience=5)

# 7) 모델 훈련
history = model.fit(
    X_train, Y_train,
    validation_data=(X_test, Y_test),
    epochs=30,
    batch_size=200,
    verbose=1,
    callbacks=[early_stopping_callback, checkpointer]
)

# 8) 정확도 출력
print("\nTest Accuracy: %.4f" % (model.evaluate(X_test, Y_test)[1]))

# 9) 학습/검증 손실 시각화
y_vloss = history.history['val_loss']
y_loss = history.history['loss']

x_len = np.arange(len(y_loss))
plt.plot(x_len, y_vloss, marker='.', c="red", label='Testset_loss')
plt.plot(x_len, y_loss, marker='.', c="blue", label='Trainset_loss')
plt.legend(loc='upper right')
plt.grid()
plt.xlabel('epoch')
plt.ylabel('loss')
plt.show()

# 10) 학습된 모델로 예측 실험
test_num = X_train[0].reshape(-1, 28, 28, 1)
prediction = model.predict(test_num)
print('입력한 이미지는 %f 확률로 %d 입니다!' %
      (prediction[0, prediction.argmax()], prediction.argmax()))

# 11) 새로운 이미지 로드 및 전처리
test = Image.open('./14장_data/test7.jpg')
test_gray = test.convert("L")
test_gray = test_gray.resize((28, 28))

test_data = np.asarray(test_gray)

plt.imshow(test_data, cmap='Greys')
plt.show()

# (1) 색 반전
test_data_v = []
for i in range(28):
    row = []
    for j in range(28):
        row.append(255 - test_data[i][j])
    test_data_v.append(row)

plt.imshow(test_data_v, cmap='Greys')
plt.show()

# (2) 모델 입력 형태로 변환
test_data_v2 = np.asarray(test_data_v)
test_data_v2 = test_data_v2.reshape(-1, 28, 28, 1).astype('float32') / 255

# (3) 모델 예측
prediction_new = model.predict(test_data_v2)
test_class = prediction_new.argmax()

print('입력한 이미지는 %f 확률로 %d 입니다!' %
      (prediction_new[0, test_class] * 100, test_class))
g