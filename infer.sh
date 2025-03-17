f5-tts_infer-cli \
--model "F5TTS_Base" \
--ref_audio ref.wav \
--ref_text "kế hoạch là vậy nhưng cả pháp lẫn tây ban nha vẫn chưa xác định được nơi nào phù hợp để mở màn chiến dịch." \
--gen_text "xin chào các bạn" \
--speed 1.0 \
--vocoder_name vocos \
--vocab_file data/your_training_dataset/vocab.txt \
--ckpt_file ckpts/your_training_dataset/model_last.pt \
