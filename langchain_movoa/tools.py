"""Movoa video generation as a LangChain tool.

Unlimited AI video generator with sound: on paid plans the tenth take of a shot
costs what the first did, and your first clip is free to make right now.

Runs cost credits on a Movoa account: pass ``api_key`` or set ``MOVOA_API_KEY``
(create a key at https://movoa.ai/settings/apikeys).
"""

from typing import Any, Dict, Literal, Optional, Type

import movoa
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


def _explain(e: movoa.MovoaError) -> str:
    if isinstance(e, movoa.AuthError):
        return f"Movoa needs a valid API key (create one at https://movoa.ai/settings/apikeys): {e}"
    if isinstance(e, movoa.QuotaError):
        return f"The Movoa account is out of credits: {e}"
    if isinstance(e, movoa.PlanError):
        return f"That model or quality needs a Movoa plan first: {e}"
    if isinstance(e, movoa.BusyError):
        return f"Another Movoa run on this account is still generating; wait for it: {e}"
    if isinstance(e, movoa.RejectedError):
        return f"Movoa refused the prompt, reword it: {e}"
    if isinstance(e, movoa.GenerationError):
        return f"The Movoa run failed ({e.failure_kind or 'no failure code'}); reword the prompt rather than retrying it as is"
    if isinstance(e, movoa.TimeoutError):
        return f"Movoa run {e.task_id} is still generating; check it later"
    return f"Movoa error: {e}"


def _params(**kw: Any) -> Dict[str, Any]:
    return {k: v for k, v in kw.items() if v is not None}


class MovoaVideoInput(BaseModel):
    """Arguments for :class:`MovoaVideoGenerator`."""

    prompt: str = Field(description="The shot: what happens, where, and how the camera moves.")
    image_url: Optional[str] = Field(default=None, description="Public https url of a first frame to animate (photo to video).")
    duration: Optional[int] = Field(default=None, description="Clip length in seconds.")
    resolution: Optional[Literal["480p", "720p", "768p", "1080p"]] = Field(default=None, description="Output resolution.")
    aspect_ratio: Optional[Literal["16:9", "4:3", "1:1", "3:4", "9:16", "21:9"]] = Field(
        default=None, description="Shape of the clip, default 16:9."
    )


class MovoaVideoGenerator(BaseTool):
    """Generate a video clip with sound on Movoa and return its url. Takes minutes.

    ``model`` defaults to ``minimax-h3``; other ids: ``veo-3-1-fast``,
    ``seedance-2-5``, ``seedance-2``, ``seedance-2-fast``, ``seedance-2-mini``.
    """

    name: str = "movoa_video_generator"
    description: str = (
        "Generates a short video clip with sound on Movoa from a text prompt, or animates "
        "a photo at a public https url, and returns a url to the mp4 clip. Takes several minutes."
    )
    args_schema: Type[BaseModel] = MovoaVideoInput
    api_key: Optional[str] = None
    model: str = movoa.DEFAULT_MODEL
    sound: Optional[bool] = None
    timeout: float = 900.0

    def _run(
        self,
        prompt: str,
        image_url: Optional[str] = None,
        duration: Optional[int] = None,
        resolution: Optional[str] = None,
        aspect_ratio: Optional[str] = None,
        **_: object,
    ) -> str:
        try:
            return movoa.generate_video(
                prompt,
                self.model,
                image_url,
                api_key=self.api_key,
                timeout=self.timeout,
                **_params(
                    duration=duration,
                    resolution=resolution,
                    aspect_ratio=aspect_ratio,
                    sound=self.sound,
                ),
            )
        except movoa.MovoaError as e:
            return _explain(e)
