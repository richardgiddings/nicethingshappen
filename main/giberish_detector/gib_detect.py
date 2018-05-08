import pickle
from main.giberish_detector import gib_detect_train
import os

def test_input(input_text):
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'gib_model.pki')
    model_data = pickle.load(open(file_path, 'rb'))

    model_mat = model_data['mat']
    threshold = model_data['thresh']
    return gib_detect_train.avg_transition_prob(input_text, model_mat) > threshold