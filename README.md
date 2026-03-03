# Password Strength Analyzer & Custom Wordlist Generator

A Python tool that analyzes password strength using entropy calculations, 
zxcvbn scoring, and a built-in database of 1000+ common passwords. 
It also generates custom attack wordlists from personal information tokens.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## Features

### Password Analyzer
- **Entropy calculation** based on character pool size
- **zxcvbn integration** for pattern-based scoring
- **Common password database** with 1000+ passwords and 28,000+ mutations
- **Pattern detection** (keyboard walks, repeated characters, sequences)
- **Character set analysis** (lowercase, uppercase, digits, symbols)
- **Crack time estimation**
- **Actionable suggestions** for improvement

### Wordlist Generator
- **Case mutations** (lower, UPPER, Title, sWAPCASE)
- **Leetspeak substitutions** (a→@, e→3, s→$, o→0)
- **Year appending** (1970-2029, two-digit variants)
- **Token combinations** with separators (john_fluffy, john.rex)
- **Date fragment extraction** from birthdays
- **Reverse words**
- **Common suffix appending** (!, 123, @, #)
- **Export to .txt** compatible with Hashcat, John the Ripper, Hydra

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/harshhhhh10/Password-Analyzer-Wordlist-Generator.git
cd Password-Analyzer-Wordlist-Generator
