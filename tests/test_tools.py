from unittest import mock

import movoa
from langchain_movoa import MovoaVideoGenerator


def test_video_defaults_to_minimax_h3_and_maps_image():
    with mock.patch.object(movoa, "generate_video", return_value="https://cdn.movoa.ai/v.mp4") as g:
        out = MovoaVideoGenerator(api_key="test-key").invoke(
            {"prompt": "a paper boat", "duration": 6, "image_url": "https://x/y.png", "resolution": "768p"}
        )
    assert out == "https://cdn.movoa.ai/v.mp4"
    assert g.call_args.args[1] == "minimax-h3"
    assert g.call_args.args[2] == "https://x/y.png"
    assert g.call_args.kwargs["duration"] == 6
    assert g.call_args.kwargs["resolution"] == "768p"
    assert "aspect_ratio" not in g.call_args.kwargs
    assert g.call_args.kwargs["api_key"] == "test-key"


def test_refusals_become_text():
    cases = [
        (movoa.AuthError("Invalid API key", 401), "API key"),
        (movoa.QuotaError("Insufficient credits", 402), "out of credits"),
        (movoa.PlanError("purchase required", 403), "plan"),
        (movoa.BusyError("Video generation is already in progress", 409), "still generating"),
        (movoa.RejectedError("blocked", 400, -2, "content_blocked"), "reword"),
        (movoa.GenerationError("failed", "task-1", "timeout", "timeout"), "timeout"),
        (movoa.TimeoutError("still running", task_id="task-2"), "task-2"),
    ]
    for err, needle in cases:
        with mock.patch.object(movoa, "generate_video", side_effect=err):
            out = MovoaVideoGenerator(api_key="test-key").invoke({"prompt": "x"})
        assert needle in out, (err, out)


def test_live_wrong_key_goes_to_auth_branch():
    out = MovoaVideoGenerator(api_key="invalid-test-fixture-token").invoke({"prompt": "a paper boat"})
    assert out.startswith("Movoa needs a valid API key")
