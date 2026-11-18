# langchain-movoa

Unlimited AI video generator with sound: on paid plans the tenth take of a shot costs what the first did, and your first clip is free to make right now. LangChain tool for [Movoa](https://movoa.ai/?utm_source=pypi-langchain&utm_medium=package): generate video clips with sound from a text prompt or animate a photo as the first frame from an agent.

## Install

```bash
pip install langchain-movoa
```

Set `MOVOA_API_KEY` from [movoa.ai/settings/apikeys](https://movoa.ai/settings/apikeys), or pass `api_key=`. Runs cost credits on your Movoa account at the prices on [movoa.ai/pricing](https://movoa.ai/pricing).

## Usage

```python
from langchain_movoa import MovoaVideoGenerator

tool = MovoaVideoGenerator()  # reads MOVOA_API_KEY
clip_url = tool.invoke({
    "prompt": "a paper boat drifting down a rain gutter, low angle",
    "duration": 6,
})
```

To animate a still photo, pass `image_url`:

```python
clip_url = tool.invoke({
    "prompt": "the camera slowly orbits the statue while soft light sweeps across it",
    "image_url": "https://example.com/statue.jpg",
})
```

## Models

`model` defaults to `minimax-h3`; other model ids: `veo-3-1-fast`, `seedance-2-5`, `seedance-2`, `seedance-2-fast`, `seedance-2-mini`.

## Links

- [Movoa](https://movoa.ai/?utm_source=pypi-langchain&utm_medium=package)
- [Text to video](https://movoa.ai/video/text-to-video)
- [API keys](https://movoa.ai/settings/apikeys)
- [Pricing](https://movoa.ai/pricing)
