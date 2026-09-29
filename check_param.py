import torch
import traceback
from surya.model.recognition.config import SuryaOCRConfig
from surya.model.recognition.model import load_model

orig_init = SuryaOCRConfig.__init__
def patched_init(self, **kwargs):
    encoder_config = kwargs.pop('encoder', {})
    decoder_config = kwargs.pop('decoder', {'pad_token_id': 0, 'bos_token_id': 1, 'eos_token_id': 2})
    text_encoder_config = kwargs.pop('text_encoder', {})
    orig_init(self, encoder=encoder_config, decoder=decoder_config, text_encoder=text_encoder_config, **kwargs)

SuryaOCRConfig.__init__ = patched_init
def patched_get_text_config(self, **kwargs):
    return self.decoder if hasattr(self, "decoder") else None
SuryaOCRConfig.get_text_config = patched_get_text_config

import transformers.modeling_utils
orig_load_param = transformers.modeling_utils._load_parameter_into_model
def patched_load_param(model, param_name, param, *args, **kwargs):
    try:
        orig_load_param(model, param_name, param, *args, **kwargs)
    except Exception as e:
        print(f"FAILED TO LOAD PARAM: {param_name}")
        raise e
transformers.modeling_utils._load_parameter_into_model = patched_load_param

try:
    load_model('vikp/surya_rec2')
except Exception as e:
    print(traceback.format_exc())
    print("Error caught:", str(e))
