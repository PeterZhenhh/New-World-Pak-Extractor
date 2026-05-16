# New World Pak Extractor

A Python tool for extracting game resources from the `.pak` files of New World: Aeternum.

This project was tested on the Steam version with **BuildID 22469132**, and all game resources in the tested packages were successfully extracted.

> The game is no longer receiving updates, so this extractor is intended for archival, modding research, and educational purposes only.

---

## Features

- Extract resources from New World `.pak` files
- Automatically restores original file modification timestamps from pak metadata
- Performs CRC validation during extraction
- Pure Python implementation
- Supports the Steam release build `22469132`
- Successfully tested on all available game resources from the tested version
- No additional Python dependencies required

---

## Disclaimer

This project is **not affiliated with or endorsed by Amazon Games**.

The extracted assets remain the property of their respective copyright holders.

Please use this tool responsibly and only for:

- Personal backup
- Modding research
- Preservation
- Educational analysis

Do not redistribute copyrighted game assets.

---

## Tested Version

| Platform | BuildID | Status |
| --- | --- | --- |
| Steam | 22469132 | Fully Working |

Game page: https://store.steampowered.com/app/1063730/New_World_Aeternum/

---

## Requirements

- Python 3.10+
- `oo2core_8_win64.dll`

No additional Python packages or dependencies are required.

---

## Setup

Before running the script:

1. Place `oo2core_8_win64.dll` in the same directory as `main.py`.

2. Edit the following lines in `main.py` and replace the paths with your own directories:

```python
gameRootPath = r"E:\SteamLibrary\steamapps\common\New World"
exportRootPath = r"E:\output"
```

### Path Description

- `gameRootPath`
  - The installation directory of the game
  - This directory must contain `PaksList.lst`

Example structure:

```text
New World/
├── PaksList.lst
├── assets/
├── bin64/
└── ...
```

- `exportRootPath`
  - Directory where extracted files will be exported


---

## Usage

Run the script:

```bash
python main.py
```

---

## Output

Extracted files will be written to the directory specified by `exportRootPath`.

The extractor will also:

- Restore the original modification timestamps stored in the pak metadata
- Verify extracted files using CRC checks

---

## Notes

- Some resources use Oodle compression and require `oo2core_8_win64.dll`.
- Extraction performance depends on storage speed and CPU performance.
- Repacking support is not currently implemented, may be added in the future. However, since the game is no longer releasing content updates, there is currently no estimated timeline for this feature.

---

## Legal

This repository does not include any game files or copyrighted assets.

Users are responsible for complying with local laws and the game's EULA.

---

## License

MIT License

Feel free to modify and improve the project.
