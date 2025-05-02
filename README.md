# Doran's Package

[![PyPI version](https://badge.fury.io/py/dorans.svg)](https://badge.fury.io/py/dorans)
[![Publish](https://github.com/gptilt/dorans/actions/workflows/publish.yaml/badge.svg)](https://github.com/gptilt/dorans/actions/workflows/publish.yaml)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC_BY--NC_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

<p align="center">
<img src="./docs/assets/logo.png" alt="Doran's" width="150" height="150">
</p>

*`dorans` is part of the [GPTilt](https://github.com/gptilt) project.*

`dorans` is [Master Doran's](https://wiki.leagueoflegends.com/en-us/Universe:Doran) premier Python package, filled with key formulas that hold the secrets to the game's mechanics!

## Features

**Disclaimer:** *`dorans` is still level 1!*

For now, here's what you can get:

* **Champion Experience (XP):** Functions to calculate champion level, XP gained from kill, monster, etc.
* **Death Timer:** Function that computes the death timer from champion level and the game minutes.

Future additions may include utilities for gold calculation, damage analysis, and more!

## Getting Started

Install `dorans` directly from PyPI:

```bash
pip install dorans
```

Import it, and try it out!

```py
from dorans import xp

print(xp.total_from_level(17))
# Output: 16480

print(xp.from_event(
    "assist",
    champion_level=6,
    enemy_level=6,
    number_of_assists=2
))
# Output: 134.0
```

## Contributing

Contributions are welcome! If you have ideas for new utilities, find bugs, or want to improve existing code, please feel free to open an issue or submit a pull request on the GitHub repository.

## License

All datasets are licensed under the [Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/).

GPTilt isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing Riot Games properties. Riot Games, and all associated properties are trademarks or registered trademarks of Riot Games, Inc.
