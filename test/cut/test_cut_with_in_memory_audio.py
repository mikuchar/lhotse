import numpy as np

from lhotse import Recording, MonoCut
from lhotse.testing.dummies import dummy_cut


def test_cut_with_in_memory_audio():
    path = "test/fixtures/mono_c0.wav"
    data = open(path, "rb").read()
    cut = dummy_cut(0, duration=0.5).drop_recording()

    assert cut.custom is None
    assert cut.load_audio() is None  # original cut has no audio data

    cut_with_audio = cut.with_memory_audio(data)

    assert cut.custom is None  # original cut is unmodified

    np.testing.assert_equal(
        cut_with_audio.load_audio(), Recording.from_file(path).load_audio()
    )


def test_cut_to_in_memory():
    path = "test/fixtures/mono_c0.wav"
    cut = dummy_cut(0, duration=0.5).drop_recording()
    cut.recording = Recording.from_file(path)

    memory_cut = cut.to_in_memory()

    np.testing.assert_equal(
        memory_cut.load_audio(), cut.load_audio()
    )


def test_cut_with_in_memory_audio_serialization():
    path = "test/fixtures/mono_c0.wav"
    data = open(path, "rb").read()
    cut = dummy_cut(0, duration=0.5).drop_recording()

    assert cut.custom is None
    assert cut.load_audio() is None  # original cut has no audio data

    cut_with_audio = cut.with_memory_audio(data)

    assert cut.custom is None  # original cut is unmodified

    data = cut_with_audio.to_dict()
    cut_deserialized = MonoCut.from_dict(data)

    np.testing.assert_equal(
        cut_deserialized.load_audio(), cut_with_audio.load_audio()
    )