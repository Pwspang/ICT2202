# ICT-2202

A Cutter plugin to extract static, obfuscated, and stack strings using [FLOSS](https://github.com/mandiant/flare-floss).

## Installation

Make sure you have the FLOSS binary in your `PATH`. You can check by running

```bash
floss --version
```

in your terminal. You should get an output similar to this

```text
floss.exe 1.7.0-alpha1
https://github.com/fireeye/flare-floss/
```

Clone this repository by running

```bash
git clone https://github.com/Pwspang/ICT2202
```

Place the `floss_cutter.py` file in `%appdata%\rizin\cutter\plugins\python`.
