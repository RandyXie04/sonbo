from surya.model.recognition.config import SuryaOCRConfig

orig_init = SuryaOCRConfig.__init__
def patched_init(self, **kwargs):
    encoder_config = kwargs.pop('encoder', {})
    decoder_config = kwargs.pop('decoder', {'pad_token_id': 0, 'bos_token_id': 1, 'eos_token_id': 2})
    text_encoder_config = kwargs.pop('text_encoder', {})
    orig_init(self, encoder=encoder_config, decoder=decoder_config, text_encoder=text_encoder_config, **kwargs)

SuryaOCRConfig.__init__ = patched_init
c = SuryaOCRConfig.from_pretrained('vikp/surya_rec2')
print(c.encoder)
