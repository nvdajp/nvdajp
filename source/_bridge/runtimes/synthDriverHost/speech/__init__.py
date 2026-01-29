# Minimal speech package for synthDriverHost runtime; nvwave only needs these.
from speech.types import SpeechSequence, SequenceItemT
from speech.commands import BreakCommand
__all__ = ["SpeechSequence", "SequenceItemT", "BreakCommand"]
