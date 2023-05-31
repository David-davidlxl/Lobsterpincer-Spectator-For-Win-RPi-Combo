"""
Executes some tests for the complete digitization of a chessboard.
"""
import sklearn  # Required in Jetson to avoid cannot allocate memory in

# static TLS block error

# from tensorflow.keras.applications.imagenet_utils import preprocess_input as \
#         prein_squeezenet
# from tensorflow.keras.applications.mobilenet_v2 import preprocess_input as \
#         prein_mobilenet
# from tensorflow.keras.applications.xception import preprocess_input as \
#         prein_xception

from keras.applications.imagenet_utils import preprocess_input as prein_squeezenet
from keras.applications.mobilenet_v2 import preprocess_input as prein_mobilenet
from keras.applications.xception import preprocess_input as prein_xception
from keras.applications.nasnet import preprocess_input as prein_nasnet
from keras.applications.densenet import preprocess_input as prein_densenet

from livechess2fen.lc2fen.predict_board import (
    predict_board_keras,
    predict_board_onnx,
    predict_board_trt,
)


ACTIVATE_KERAS = False
MODEL_PATH_KERAS = "selected_models/Xception_last.h5"
IMG_SIZE_KERAS = 299
PRE_INPUT_KERAS = prein_xception

# MODEL_PATH_KERAS = "selected_models/NASNetMobile_all_last.h5"
# IMG_SIZE_KERAS = 224
# PRE_INPUT_KERAS = prein_nasnet

# MODEL_PATH_KERAS = "selected_models/DenseNet201_last.h5"
# PRE_INPUT_KERAS = prein_densenet
# IMG_SIZE_KERAS = 224


ACTIVATE_ONNX = True
MODEL_PATH_ONNX = "selected_models/Xception_last.onnx"
IMG_SIZE_ONNX = 299
PRE_INPUT_ONNX = prein_xception

ACTIVATE_TRT = False
MODEL_PATH_TRT = "selected_models/SqueezeNet1p1.trt"
IMG_SIZE_TRT = 227
PRE_INPUT_TRT = prein_squeezenet

path = "predictions/3.png"
a1_pos = "BL"


def main_keras():
    """Executes Keras test board predictions."""
    print("Keras predictions")
    fen, board_corners = predict_board_keras(
        MODEL_PATH_KERAS, IMG_SIZE_KERAS, PRE_INPUT_KERAS, path, a1_pos, test=False
    )
    print(fen)
    print(board_corners)


def main_onnx():
    """Executes ONNXRuntime test board predictions."""
    print("ONNXRuntime predictions")
    fen, board_corners = predict_board_onnx(
        MODEL_PATH_ONNX, IMG_SIZE_ONNX, PRE_INPUT_ONNX, path, a1_pos, test=False
    )
    print(fen)
    print(board_corners)


def main_tensorrt():
    """Executes TensorRT test board predictions."""
    print("TensorRT predictions")
    predict_board_trt(MODEL_PATH_TRT, IMG_SIZE_TRT, PRE_INPUT_TRT, test=True)


if __name__ == "__main__":
    if ACTIVATE_KERAS:
        main_keras()
    if ACTIVATE_ONNX:
        main_onnx()
    if ACTIVATE_TRT:
        main_tensorrt()
