[![license](https://img.shields.io/github/license/BlackIQ/Ashley?style=flat-square)](https://github.com/BlackIQ)

[![code-size](https://img.shields.io/github/languages/code-size/BlackIQ/Ashley?style=flat-square)](https://github.com/BlackIQ)

# Hey there ! I am Rachel :)

An assistant written in **Python**!

---

Anyway, I can't do difficult stuff, but I am a lovely Assistant!

There is no MySQL in This version :)
In this case we use [pyabr](https://github.com/manijamali2003/pyabr) Database Extension named **Control**.

README map:
- Installation
- Run
- Debug
- Software Architect
- Thanks from developers.

---

### Installation

#### Install packages.

Things you should have already:

- Python, Pip
- espeack, ffmpeg, mpg123
- git

#### Clone and install Rachel requires

```
git clone https://github.com/BlackIQ/Rachel && cd Rachel
pip3 install -r requirements.txt
```

#### Install Rachel

```
sudo python3 setup.py
```

---

### Run

You can run **Rachel** with command.

```
Rachel
```

---

### Debugging

When you clone and install **Rachel**, you can not run it via `python3 Rachel.py`. You have to enter Rachel command. But
for **debugging** you should run `debug.py` and it will debug it for you.

#### How yo debug?

```
python3 debug.py
```

---

### Software Architecture

```
Rachel
├── buildlibs
│   ├── control.py
│   ├── pack_archives.py
│   └── ui
│       └── setup.ui
├── packs
│   └── rachel
│       ├── code
│       │   ├── core.py
│       │   ├── data.py
│       │   ├── libabr.py
│       │   └── rachel.py
│       ├── control
│       │   ├── compile
│       │   ├── list
│       │   └── manifest
│       └── data
│           ├── etc
│           │   └── rachel
│           └── usr
│               └── share
│                   └── docs
│                       └── rachel
│                           ├── AUTHERS
│                           ├── LICENSE
│                           └── version.md
├── README.md
├── requirements.txt
├── setup.py
├── debug.db
├── debug.py
└── LICENSE

12 directories, 21 files
```

Well, As you can see, here we have a nice architect!

**[Buildlibs](https://github.com/BlackIQ/Rachel/tree/master/buildlibs) directory.**

Here we have control and archive manager files. And setup ui file.

- [control.py](https://github.com/BlackIQ/Rachel/tree/master/buildlibs/pack_archives.py) : control file is one of pyabr database control files that Rachel uses it too.
- [pack_archives.py](https://github.com/BlackIQ/Rachel/tree/master/buildlibs/pack_archives.py) : pack_archives.py is again one of pyabr archive manager that Rachel uses too.
- [ui](https://github.com/BlackIQ/Rachel/tree/master/buildlibs/ui) directory:
  - [setup.ui](https://github.com/BlackIQ/Rachel/tree/master/buildlibs/ui/setup.ui) : There is a dir named `ui` and in dir there is ui file for setup.

**`packs` directory.**

Main dir is `pack` that Rachel is located there. As you can see, there is `rachel` dir inside if `pack`.
In `rachel` we have 3 dirs. Let's go for details.

- `code` directory.
  - `core.py` : Main functions and classes are all here.
  - `data.py` : Getting data and transfer data with PyAbr files.
  - `libabr.py` : PyAbr main library.
  - `rachel.py` : Rachel commands handler.
- `control` directory.
  - `compile` : Compiling data.
  - `list`: List file.
  - `manifest` : Main manifest file.
- `data` directory.
  - `etc` directory.
    - `rachel` : This file includes Rachel and User data.
  - `usr` directory.
    - `share` directory.
      - `docs` directory.
        - `rachel` directory.
          - `AUTHERS` : Developers.
          - `LICENSE` : License name.
          - `version.md` : Version and more information about it.

**Single files.**

- `README.md` : Rachel README.
- `requirements.txt` : Libraries that Rachel need.
- `setup.py` : Setup file for installing Rachel.
- `debug.db` : PyAbr database control system file.
- `debug.py` : Rachel debugging file.
- `LICENSE` : Rachel License under GPL-3

---

### After all , I love guys that had worked on Rachel

- [Erfan Saberi](https://github.com/erfansaberi) :heart:, for big new updates and **Hacktoberfest**.
- [Mani Jamali](https://github.com/manijamali2003) :star:, for new platform and setup.
- [Amirmahdi Tafreshi](https://github.com/mr-tafreshi) :pen:, for Rachel packages.
- [Annahita Mirhosseini](https://github.com/Annahita2004) :sparkles:, for features idea.