from src.prediction.predictor import build_prediction_frame
from src.models.trainer import FEATURE_COLUMNS
import pytest


def test_prediction_frame_has_expected_feature_order():
    frame = build_prediction_frame("Brazil", "Argentina", "2026-07-10")

    assert not frame.empty
    assert list(frame.columns) == FEATURE_COLUMNS


def test_prediction_rejects_unsupported_team():
    with pytest.raises(ValueError, match="Unsupported team"):
        build_prediction_frame("Brazil", "Czechoslovakia", "2026-11-09")
