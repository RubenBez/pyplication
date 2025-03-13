# PyPlication [![Health Check](https://github.com/RubenBez/pyplication/actions/workflows/health-check.yml/badge.svg)](https://github.com/RubenBez/pyplication/actions/workflows/health-check.yml)

Small demo project for send and parsing HTML

## Getting Started

To setup the project initially run this and restart vscode
```bash
$ python3 -m venv .venv
```

Run to install dependencies, run
```bash
$ pip install -r requirements.txt
```

To start the API

```bash
$ flask --app pyplication run
```

You can run test te verify everything is working. 
> Make sure to give execution permission to the script
> ```bash
> $ chmod +x scripts/test.sh
> ```

```bash
$ ./scripts/test.sh
```

## Tests

The whole project is also tested. Verify by running 

```bash
$ pytest
```

## AI (WIP)

To setup training data for the AI, run the following

```bash
$ python3 ai/scrappy.py
```

This will take some time depending on your internet speed, but you will end-up with `training_data.csv` that can be fed into a Model