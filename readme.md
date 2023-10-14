# Extract transcript from YouTube videos

* Adapted tutorial from Marc Maxmeister, 2022-09-01, https://stackoverflow.com/a/73572089/how-to-add-punctuation-to-text-using-python.
* Model used to add punctuation: https://huggingface.co/oliverguhr/fullstop-punctuation-multilang-large.
* Supported languages: English, German, French, Italian
* Keep in mind that we use an undocumented YouTube API part of the web client to get the subtitles. It might break at some random point in the future.
* Motivation: 
  1. Show rampant rambling in some YouTube videos.
  2. Get neatly formatted transcript from autogenerated subtitles.


## Example

* Run `python main.py -v stxVBJem3R`
   * This saves a transcript text file in the folder `output`.
   * `stxVBJem3R` is just an example of a YouTube video id.
* Run `python main.py -v stxVBJem3R -r > output.txt`
   * `stxVBJem3R` is just an example of a YouTube video id.
   * `-r` means raw, so all output is logged directly into console.
   * `> output.txt` is optional, it allows you to pipe the output directly into a text file.

```bash
$ python main.py -v 6wkVGQ8swBg -r
[Music].

Thank you everyone for coming today.

This is why care about wholesome games anyway.

Uh, before we get started, I was asked to ask everyone to silence your phones.

Uh, I'm very clumsy so if something goes off, I'll probably be startled and fall off the stage, so please keep that in mind.

Uh, today we're talking about wholesome games.

[...] (truncated to keep things short)
```


## Installation

1. Create a virtual environment with `python -m venv env`
2. Activate the virtual environment with `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (MacOS + Linux).
   * It can happen that the Powershell execution policy on Windows does not allow you to create a virtual environment.
   * To fix this you have to bypass the script execution policy in Powershell.
   * You can also set up VS Code  so it automatically allows you to activate the Python environment.
   * Open settings.json and add the following code: 
     ```json
       "terminal.integrated.profiles.windows": {
         "PowerShell": {
           "source": "PowerShell",
           "icon": "terminal-powershell",
           "args": ["-ExecutionPolicy", "Bypass"]
         }
       },
       "terminal.integrated.defaultProfile.windows": "PowerShell",
     ```
3. Run `pip install -r requirements.txt`. This might take a while because the punctuation model alone is 2.4 GB.
4. When running the script the first time, additional models get downloaded. This might take a few moments.


## Usage

* `-v, --video`:  
  **Required.** 11 digits presenting YouTube video id. 
  Can be optionally prefixed with an additional `?` to prevent leading dashes getting the video id interpreted as argument.
* `-l, --languages`:  
  Optional. Comma-separated list of languages to download languages of, e.g. `en,de`. 
  Note that the model can only process `en`, `de`, `fr` and `it`, but you can also try applying it to other languages.
* `-r, --raw`:  
  Optional, Flag. Print output directly onto the terminal.
* `-m, --preserve-markup`:  
  Optional, Flag. Preserve markup like italics and bold in subtitle (untested).

> **Info:** If a video id starts with a dash `-` or double dashes `--`, it gets interpreted as CLI argument.  
> You can prefix any video id with a `?` question mark to prevent this.  


## See also

* https://pypi.org/project/youtube-transcript-api/
* https://huggingface.co/oliverguhr/fullstop-punctuation-multilang-large
* https://stackoverflow.com/questions/31514136/how-to-add-punctuation-to-text-using-python/73572089#73572089
* https://stackoverflow.com/questions/56199111/visual-studio-code-cmd-error-cannot-be-loaded-because-running-scripts-is-disabl/67420296#67420296


## Credits

* Created by Krank (c) 2023 (https://krank.love/).
