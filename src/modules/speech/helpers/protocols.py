from typing import Protocol

import torch


class SileroTTSProtocol(Protocol):
  speaker: str
  def apply_tts(self, text: str, speaker: str, sample_rate: int) -> torch.Tensor:
    ...
