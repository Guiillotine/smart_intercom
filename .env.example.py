DEVICE="cuda" # cpu | cuda

# ------------- Automatic Speech Recognition -------------

ASR_MODEL_SIZE="small"  # base | small | medium | large-v3

ASR_COMPUTE_TYPE="float16" # int8 | float16

# ------------------------- TTS --------------------------

TTS_MODEL_ID_RU='v5_ru'
TTS_SPEAKER_RU='xenia'

TTS_MODEL_ID_EN='v3_en'
TTS_SPEAKER_EN='en_0'

TTS_SAMPLE_RATE=48000

# ------------------------- Face -------------------------

FACE_PROVIDERS="CUDAExecutionProvider" # CPUExecutionProvider | CUDAExecutionProvider

DET_SCORE_THRESHOLD=0.6

# ------------------------- BOT --------------------------

BASE_URL="https://api.vsegpt.ru/v1"

MODEL="openai/gpt-4o-mini"

MODEL_SUPPORTS_STRUCTURED_OUTPUTS=False

API_KEY=api_key