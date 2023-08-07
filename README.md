# caster

Caster is a tool for translating `*.xliff` files from `zh-CN` to `zh-TW`, integrated with Crowdin API support.

## Installsation

Clone this repository and create a virtual environment with python >= 3.8:

```bash
$ python -m venv venv
```

Activate the virtual environment and install the dependencies:

```bash
$ source venv/bin/activate # or venv\Scripts\activate.bat on Windows
$ pip install -r requirements.txt
```

## Usage

```bash
$ caster -h
usage: caster [-h] {local,remote} ...

Translate XLIFF files from simplified Chinese to traditional Chinese. Integrate with Crowdin.

positional arguments:
  {local,remote}
    local         Translate a local XLIFF file.
    remote        Translate a remote XLIFF file from Crowdin.

options:
  -h, --help      show this help message and exit


$ caster local -h
usage: caster local [-h] -f FILE -o OUTPUT

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  The XLIFF file to translate. (zh-CN)
  -o OUTPUT, --output OUTPUT
                        The output file. (zh-TW)


$ caster remote -h
usage: caster remote [-h] -p PROJECT -t TOKEN [-f FILE] [--dry-run]

options:
  -h, --help            show this help message and exit
  -p PROJECT, --project PROJECT
                        The Crowdin project ID.
  -t TOKEN, --token TOKEN
                        The Crowdin API token.
  -f FILE, --file FILE  The XLIFF file glob to translate.
  --dry-run             Don't actually upload the translated file to Crowdin.
```