# Semi-Intransient Matrix Network

Modern API wrapper for Genshin Impact & Honkai: Star Rail built on asyncio and pydantic.

## Requirements

- Python 3.9+
- httpx
- Pydantic

## Example

A very simple example of how simnet would be used:

```python3
import asyncio
import simnet

async def main():
    cookies = {} # write your cookies
    player_id = 123456789
    async with simnet.StarRailClient(cookies, player_id=player_id) as client:
        data = await client.get_starrail_user()
        print(f"Player has a total of {data.stats.avatar_num} characters")

asyncio.run(main())
```

> Note that Hoyolab has not implemented Battle Chronicle for Honkai Star Rail yet (as of 05/16/2023).
> HSR related features will be unavailable for global players. For more details, check issue #24

## Credits
- [genshin.py](https://github.com/thesadru/genshin.py/): fork source 