# Quickstart: Creating a New Expert

This guide provides a quick overview of how to use the `new` command to create your first trading expert.

## Prerequisites

Ensure that the `metaexpert` library is installed in your Python environment.

## Step 1: Run the `new` command

Open your terminal and run the following command. You can replace `"My First Expert"` with any name you choose.

```sh
metaexpert new "My First Expert"
```

## Step 2: Inspect the Output

The command will create a new directory in your current location. Based on the example above, the structure will be:

```
my_first_expert/
└── main.py
```

- The directory is named using the `snake_case` version of your input.
- The `main.py` file contains the complete code from the project's template, ready for you to modify.
- The class name inside `main.py` has been updated to `MyFirstExpert`.

## Step 3: Start Developing

You can now navigate into the new directory and start developing your trading strategy by editing `main.py`.

```sh
cd my_first_expert
# Open main.py in your favorite editor
```
