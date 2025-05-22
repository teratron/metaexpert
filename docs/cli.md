# MetaExpert Command Line Interface

## Basic Commands

The MetaExpert package provides a command line interface (CLI) for convenient use of various functions.

### Creating a New Expert from Template

To create a new expert file based on a template, use the `--new` argument:

```bash
metaexpert --new my_expert
```

This command will create a new file `my_expert.py` in the current directory, using the `template.py` template.

You can also specify a directory path directly in the file path:

```bash
metaexpert --new ./experts/my_expert
```

This command will create a new file `my_expert.py` in the `./experts` directory.

### Other Command Line Arguments

MetaExpert supports various arguments for configuring trading parameters:

```bash
metaexpert --stock binance --mode paper --type futures --contract usd_m --pair BTCUSDT
```

A complete list of arguments can be obtained using the command:

```bash
metaexpert --help
```