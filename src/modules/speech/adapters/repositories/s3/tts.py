import soundfile as sf

from src.config.settings import Settings


class SpeechS3Repo(S3BaseRepo, ISpeechS3Repo):
    def __init__(self):
        pass

    def put_object(name, audio, tts_sample_rate) -> str:
        sf.write(name, audio, tts_sample_rate) # TODO: тестовая заглушка

        print("\nSAVED_FILE:", name)

        return f"s3_path_mock_{name}"
