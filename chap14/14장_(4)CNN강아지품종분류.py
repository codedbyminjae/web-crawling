import os
import glob
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

# ---------------------------------------------------------
# 1. 데이터 경로 및 카테고리 설정
# ---------------------------------------------------------
root_dir = "./14장_data/dog/"
categories = ["말티즈", "요크셔", "푸들"]
num_class = len(categories)

image_width = 64
image_height = 64

# ---------------------------------------------------------
# 2. 이미지 로드 및 배열 변환
# ---------------------------------------------------------
X = []  # 이미지
Y = []  # 라벨 인덱스

for idx, category in enumerate(categories):
    image_dir = root_dir + category
    files = glob.glob(image_dir + "/*.*")

    for i, f in enumerate(files):
        img = Image.open(f).convert("RGB")
        img = img.resize((image_width, image_height))
        data = np.asarray(img)

        X.append(data)
        Y.append(idx)

    print(f"{image_dir} : {i+1}개 로드 완료")

print(f"image shape : {data.shape}")
print("총 이미지 수 X :", len(X))
print("총 라벨 수 Y   :", len(Y))

# ---------------------------------------------------------
# 3. numpy 배열 변환
# ---------------------------------------------------------
np_x = np.array(X)
np_y = np.array(Y)

print("np_x.shape =", np_x.shape)
print("np_y.shape =", np_y.shape)

# ---------------------------------------------------------
# 4. Train/Test 분리
# ---------------------------------------------------------
X_train, X_test, Y_train, Y_test = train_test_split(
    np_x, np_y, test_size=0.2, random_state=42
)

# 정규화
X_train = X_train.astype("float32") / 255
X_test  = X_test.astype("float32") / 255

# One-hot encoding
Y_train = to_categorical(Y_train, num_class)
Y_test  = to_categorical(Y_test, num_class)

print("Y_train one-hot sample :", Y_train[0])

# ---------------------------------------------------------
# 5. CNN 모델 구성
# ---------------------------------------------------------
input_shape = (image_width, image_height, 3)

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=input_shape))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(num_class, activation='softmax'))

model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

# ---------------------------------------------------------
# 6. 모델 저장 경로 설정
# ---------------------------------------------------------
MODEL_DIR = root_dir + "model/"
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

modelpath = MODEL_DIR + "{epoch:02d}-{val_loss:.4f}.hdf5"
checkpointer = ModelCheckpoint(filepath=modelpath, monitor='val_loss', verbose=1, save_best_only=True)
early_stop = EarlyStopping(monitor='val_loss', patience=5)

# ---------------------------------------------------------
# 7. 모델 학습
# ---------------------------------------------------------
model.fit(
    X_train, Y_train,
    validation_data=(X_test, Y_test),
    epochs=30,
    batch_size=20,
    verbose=1,
    callbacks=[checkpointer, early_stop]
)

# ---------------------------------------------------------
# 8. 모델 평가
# ---------------------------------------------------------
score = model.evaluate(X_test, Y_test)
print("loss =", score[0])
print("accuracy =", score[1])

# ---------------------------------------------------------
# 9. 새로운 이미지 예측
# ---------------------------------------------------------
new_files = glob.glob(root_dir + "new/*.*")
print("new files:", new_files)

image_size = 64
new_img = []
new_X = []

for fname in new_files:
    img = Image.open(fname).convert("RGB")
    img = img.resize((image_size, image_size))
    new_img.append(img)

    new_data = np.asarray(img).astype("float32") / 255
    new_X.append(new_data)

new_X = np.array(new_X)

# 예측
new_predict = model.predict(new_X)

# ---------------------------------------------------------
# 10. 결과 출력
# ---------------------------------------------------------
for i, pred in enumerate(new_predict):
    plt.figure(figsize=(1.5,1.5))
    plt.imshow(new_img[i])
    plt.axis("off")
    plt.show()

    top1 = pred.argmax()

    if pred[top1] > 0.78:
        print(f"입력:{new_files[i]} => 예측:{categories[top1]} | Score={pred[top1]*100:.2f}%\n")
    else:
        top2 = np.argsort(pred)[-2]
        print(f"입력:{new_files[i]} => {categories[top1]}({pred[top1]*100:.2f}%) + "
              f"{categories[top2]}({pred[top2]*100:.2f}%) 믹스견\n")
