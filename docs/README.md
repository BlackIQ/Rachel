# Rachel Docs

*Here is Rachel documents that is also available in [Rachel page](https://BlackIQ.github.io/Rachel).*

In document, we learn about:
- Installation
- Running
- Debugging
- Software Architect

### Installation

**Install packages**

Things you should have already:

- Python, Pip
- espeack, ffmpeg, mpg123
- git

**Clone and install Rachel requires**

```
git clone https://github.com/BlackIQ/Rachel && cd Rachel
pip3 install -r requirements.txt
```

**Install Rachel**

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

**How yo debug?**

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

**[pack](https://github.com/BlackIQ/Rachel/tree/master/pack) directory.**

Main dir is [pack](https://github.com/BlackIQ/Rachel/tree/master/pack) that Rachel is located there. As you can see, there is [rachel](https://github.com/BlackIQ/Rachel/tree/master/pack/rachel) dir inside if [pack](https://github.com/BlackIQ/Rachel/tree/master/pack).
In [rchel](https://github.com/BlackIQ/Rachel/tree/master/rachel) we have 3 dirs. Let's go for details.

- [code](https://github.com/BlackIQ/Rachel/tree/master/pack/code) directory.
  - [core.py](https://github.com/BlackIQ/Rachel/tree/master/pack/code/core.py) : Main functions and classes are all here.
  - [data.py](https://github.com/BlackIQ/Rachel/tree/master/pack/code/data.py) : Getting data and transfer data with PyAbr files.
  - [libabr.py](https://github.com/BlackIQ/Rachel/tree/master/pack/code/libabr.py) : PyAbr main library.
  - [rachel.py](https://github.com/BlackIQ/Rachel/tree/master/pack/code/rachel.py) : Rachel commands handler.
- [control](https://github.com/BlackIQ/Rachel/tree/master/pack/control) directory.
  - [compile](https://github.com/BlackIQ/Rachel/tree/master/pack/control/compile) : Compiling data.
  - [list](https://github.com/BlackIQ/Rachel/tree/master/pack/control/list): List file.
  - [manifest](https://github.com/BlackIQ/Rachel/tree/master/pack/control/manifest) : Main manifest file.
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