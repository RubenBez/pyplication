# PyPlication [![Health Check](https://github.com/RubenBez/pyplication/actions/workflows/health-check.yml/badge.svg)](https://github.com/RubenBez/pyplication/actions/workflows/health-check.yml)

Small demo project for send and parsing HTML

## Getting Started

To setup the project initially run
```bash
$ pip install -e .
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
