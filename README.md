# Statys: Statistical Analyzers

[![Latest release](https://img.shields.io/github/release/gugarosa/statys.svg)](https://github.com/gugarosa/statys/releases)
[![Build status](https://img.shields.io/travis/com/gugarosa/statys/master.svg)](https://github.com/gugarosa/statys/releases)
[![Open issues](https://img.shields.io/github/issues/gugarosa/statys.svg)](https://github.com/gugarosa/statys/issues)
[![License](https://img.shields.io/github/license/gugarosa/statys.svg)](https://github.com/gugarosa/statys/blob/master/LICENSE)

## Welcome to Statys.

Do you feel the urge to create better insights and statistically analyzing your experimental results? Are you tired of re-implementing statistical tests for every analysis? If yes, Statys is the real deal! This package provides an easy-to-go implementation of statistical analyzers. From sampling measurements to non-parametric tests, we will foster all research related to statistical tests.

Use Statys if you need a library or wish to:
* Analyze your experimental results;
* Design or use pre-loaded statistical tests;
* Mix-and-match different measurements to create insights;
* Because it is wise to analyze things.

Read the docs at [statys.readthedocs.io](https://statys.readthedocs.io).

Statys is compatible with: **Python 3.6+**.

---

## Package guidelines

1. The very first information you need is in the very **next** section.
2. **Installing** is also easy if you wish to read the code and bump yourself into, follow along.
3. Note that there might be some **additional** steps in order to use our solutions.
4. If there is a problem, please do not **hesitate**. Call us.

---

## Getting started: 60 seconds with Statys

First of all. We have examples. Yes, they are commented. Just browse to `examples/`, chose your subpackage, and follow the example. Alternatively, if you wish to learn even more, please take a minute:

Statys is based on the following structure, and you should pay attention to its tree:

```yaml
- statys
    - core
        - distribution
    - plotters
        - critical
        - significance
    - tests
        - friedman
        - mann_whitney
        - measure
        - wilcoxon
    - utils
        - constants
        - exception
        - logging
        - wrappers
```

### Core

Core is the core. Essentially, it is the parent of everything. You should find parent classes defining the basis of our structure. They should provide variables and methods that will help to construct other modules.

### Plotters

An alternative way to analyze a statistical test is by visualizing it. Hence, this package provides some customized functions that create friendly and readable plots to help users in their insights.

### Tests

Analysis should be conducted on tests, correct? This package offers a variety of statistical tests, such as Friedman, Wilcoxon, and sampling measurements, e.g., mean, median, and standard deviation.

### Utils

This is a utility package. Everyday things shared across the application should be implemented here. It is better to implement once and use it as you wish than re-implementing the same thing repeatedly.

---

## Installation

We believe that everything has to be easy. Not tricky or daunting, Statys will be the one-to-go package that you will need, from the first installation to the daily-tasks implementing needs. If you may just run the following under your most preferred Python environment (raw, conda, virtualenv, whatever):

```bash
pip install statys
```

Alternatively, if you prefer to install the bleeding-edge version, please clone this repository and use:

```bash
pip install -e .
```

---

## Environment configuration

Note that sometimes, there is a need for additional implementation. If needed, from here, you will be the one to know all of its details.

### Ubuntu

No specific additional commands are needed.

### Windows

No specific additional commands are needed.

### MacOS

No specific additional commands are needed.

---

## Support

We know that we do our best, but it is inevitable to acknowledge that we make mistakes. If you ever need to report a bug, report a problem, talk to us, please do so! We will be available at our bests at this repository or gustavo.rosa@unesp.br.

---
