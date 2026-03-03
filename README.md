# Password Strength Analyzer & Custom Wordlist Generator

A Python-based cybersecurity tool that analyzes password strength using multiple scoring engines and generates custom attack wordlists from personal information tokens.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows%20|%20Linux%20|%20Mac-blue?style=for-the-badge)

---

## Table of Contents

- [About](#about)
- [Features](#features)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
  - [GUI Mode](#gui-mode)
  - [CLI Mode](#cli-mode)
- [CLI Commands Reference](#cli-commands-reference)
- [Scoring System](#scoring-system)
- [Common Password Database](#common-password-database)
- [Wordlist Mutations](#wordlist-mutations)
- [Wordlist Compatibility](#wordlist-compatibility)
- [Screenshots](#screenshots)
- [Requirements](#requirements)
- [Disclaimer](#disclaimer)
- [License](#license)
- [Author](#author)

---

## About

This tool serves two purposes:

1. **Password Strength Analysis** — Evaluates any password using Shannon entropy calculations, zxcvbn pattern matching, and a built-in database of 1000+ commonly breached passwords with 28,000+ mutations.

2. **Custom Wordlist Generation** — Takes personal information (names, pet names, birthdays, favorite teams, etc.) and generates targeted wordlists using intelligent mutation strategies like leetspeak, case variations, year appending, and token combinations.

Built as a cybersecurity educational tool for understanding password security and demonstrating why personal information should never be used in passwords.

---

## Features

### Password Analyzer

| Feature | Description |
|---------|-------------|
| Entropy Calculation | Shannon entropy based on character pool size |
| zxcvbn Integration | Pattern-based scoring using Dropbox's zxcvbn library |
| Common Password Check | 1,043 base passwords + 28,000+ mutations from breach databases |
| Pattern Detection | Identifies keyboard walks, repeated characters, common sequences |
| Character Set Analysis | Checks for lowercase, uppercase, digits, and symbols |
| Crack Time Estimation | Estimates time to crack via offline attack |
| Suggestions | Actionable tips to improve password strength |

### Wordlist Generator

| Feature | Description |
|---------|-------------|
| Case Mutations | lower, UPPER, Title, sWAPCASE, Capitalize |
| Leetspeak | a→@, a→4, e→3, s→$, o→0, t→7, and more |
| Year Appending | 1970-2029 full years + 00-99 two-digit variants |
| Token Combinations | Joins tokens pairwise/triply with separators |
| Date Fragments | Extracts MMDD, DDMM, YYYY, YY from birthdays |
| Reverse Words | hello → olleh |
| Common Suffixes | !, 123, @, #, qwerty, 007, and more |
| Separator Variants | underscore, dash, dot, @, # between tokens |
| Initials Extraction | John Smith → js, JS |
| Length Filtering | Configurable min/max word length |
| Export to .txt | One word per line, ready for cracking tools |

---

## Project Structure
    password-strength-analyzer/
    ├── main.py # Entry point (CLI / GUI dispatcher)
    ├── cli_app.py # Argparse CLI interface
    ├── gui_app.py # Tkinter GUI interface
    ├── password_analyzer.py # Strength analysis engine
    ├── wordlist_generator.py # Wordlist generation + mutations
    ├── common_passwords.py # 1000+ common passwords database
    ├── utils.py # Shared constants and helpers
    ├── requirements.txt # Python dependencies
    ├── setup.py # Package setup
    ├── .gitignore # Git ignore rules
    ├── LICENSE # MIT License
    └── README.md # Documentation (this file)
---

## Architecture
                ┌──────────────────────────┐
     ┌────────>│     gui_app.py (Tkinter)  │
     │         │                           │
     │         │  Tab 1: Password Analyser │───> password_analyzer.py
     │         │  Tab 2: Wordlist Generator│───> wordlist_generator.py
     │         │                           │
     │         └──────────────────────────┘
     │
    main.py ─┤
    │
    │ ┌──────────────────────────┐
    └────────>│ cli_app.py (argparse) │
    │ │
    │ Command: analyse ────────────> password_analyzer.py
    │ Command: generate ───────────> wordlist_generator.py
    │ Command: both ───────────────> both modules
    │ │
    └──────────────────────────┘
    │
    ┌──────────┴──────────┐
    │ │
    ┌────┴─────┐ ┌──────────┴──────────┐
    │ utils.py │ │ common_passwords.py │
    └──────────┘ └─────────────────────┘

---

## Installation

### 1. Clone the Repository

    ```bash
    git clone https://github.com/YOUR_USERNAME/password-strength-analyzer.git
    cd password-strength-analyzer

### 2. Install Dependencies

    pip install -r requirements.txt
    
### 3. Verify Installation

    python -c "from utils import calculate_entropy; print('utils OK')"
    python -c "from common_passwords import is_common_password; print('common_passwords OK')"
    python -c "from password_analyzer import analyse; print('analyzer OK')"
    python -c "from wordlist_generator import WordlistGenerator; print('generator OK')"
    python -c "from cli_app import run_cli; print('cli OK')"
    python -c "from gui_app import run_gui; print('gui OK')"

### Usage
### GUI Mode
Launch the graphical interface:

    Bash
    python main.py gui
    
Or simply:

    Bash
    python main.py

### The GUI has two tabs:

     Tab 1: Password Analyser — Enter a password, click Analyse, see the full strength report with score bar, stats, common password check, and suggestions.
    
     Tab 2: Wordlist Generator — Enter personal tokens (names, pets, DOB, extras), configure mutation options, generate the wordlist, preview results, and export to .txt.

### CLI Mode
### Analyse a Password

    Bash
     python main.py cli analyse --password "YourPasswordHere"
     
Example:

    Bash
    python main.py cli analyse --password "password123"

Output:
  
        text
  
      ============================================================
               PASSWORD STRENGTH ANALYSIS REPORT
      ============================================================
        Password       : password123
        Length          : 11
        Entropy (bits)  : 65.21
        Unique ratio    : 82%
        Charsets used   : lowercase, digits
      
      ------------------------------------------------------------
        COMMON PASSWORD DATABASE CHECK
           Database size : 1,043 base passwords
           With mutations: 28,547 total entries
      
        +==================================================+
        |  WARNING: THIS IS A COMMON PASSWORD!             |
        +==================================================+
           Matched       : 'password123'
           Crack time    : < 1 second (dictionary attack)
      
      ------------------------------------------------------------
        Custom Score    : 0/4  Very Weak
        zxcvbn Score    : 0/4  Very Weak
        Crack time      : less than a second
      
        * OVERALL       : 0/4  Very Weak
      ------------------------------------------------------------
        Suggestions:
            - THIS IS A COMMONLY USED PASSWORD - CHANGE IT IMMEDIATELY!
            -    Matched common password: 'password123'
            -    It can be cracked in less than 1 second.
            -    Use a unique passphrase with 4+ random words.
      ============================================================
      Example with a strong password:
      
      Bash
      
      python main.py cli analyse --password "Tr0ub4dor&3_x7!Kq"
      Output:
      
      text
      
      ============================================================
               PASSWORD STRENGTH ANALYSIS REPORT
      ============================================================
        Password       : Tr0ub4dor&3_x7!Kq
        Length          : 18
        Entropy (bits)  : 118.0
        Unique ratio    : 94%
        Charsets used   : lowercase, uppercase, digits, symbols
      
      ------------------------------------------------------------
        COMMON PASSWORD DATABASE CHECK
           Database size : 1,043 base passwords
           With mutations: 28,547 total entries
           Status        : NOT found in common password list

    ------------------------------------------------------------
      Custom Score    : 4/4  Very Strong
      zxcvbn Score    : 4/4  Very Strong
      Crack time      : centuries
    
      * OVERALL       : 4/4  Very Strong
    ------------------------------------------------------------
    ============================================================

Example with a strong password:

    Bash
    
    python main.py cli analyse --password "Tr0ub4dor&3_x7!Kq"

Output:

    text
    
    ============================================================
             PASSWORD STRENGTH ANALYSIS REPORT
    ============================================================
      Password       : Tr0ub4dor&3_x7!Kq
      Length          : 18
      Entropy (bits)  : 118.0
      Unique ratio    : 94%
      Charsets used   : lowercase, uppercase, digits, symbols
    
    ------------------------------------------------------------
      COMMON PASSWORD DATABASE CHECK
         Database size : 1,043 base passwords
         With mutations: 28,547 total entries
         Status        : NOT found in common password list
    
    ------------------------------------------------------------
      Custom Score    : 4/4  Very Strong
      zxcvbn Score    : 4/4  Very Strong
      Crack time      : centuries
    
      * OVERALL       : 4/4  Very Strong
    ------------------------------------------------------------
    ============================================================
  
 ### Generate a Wordlist

    Bash
    
    python main.py cli generate \
        --name "John Smith" \
        --pet "Fluffy" "Rex" \
        --dob "1990-03-15" \
        --extra "Yankees" "pizza" \
        --output wordlist.txt

Output:

    text
    
    [*] Generating wordlist with 5 token(s) and 1 date(s) ...
    [+] 48,231 candidates written to 'wordlist.txt' in 1.37s

### Analyse + Generate Together
    Bash
    
    python main.py cli both \
        --password "JohnFluffy90" \
        --name "John Smith" \
        --pet "Fluffy" \
        --dob "1990-03-15" \
        --output wordlist.txt
        
This runs the full analysis first, then generates the wordlist.

### CLI Commands Reference
### Analyse Command
    Bash
    
    python main.py cli analyse --password "PASSWORD"
    
    Flag	Short	Description	Required
    --password	-p	Password to analyse	Yes
### Generate Command

    Bash
    python main.py cli generate [OPTIONS]
    
    Flag	Short	Description	Default
    --name	-n	Target name(s)	—
    --pet		Pet name(s)	—
    --dob		Date(s) of birth	—
    --extra		Extra keywords (team, city, hobby)	—
    --output	-o	Output file path	wordlist.txt
    --min-len		Minimum word length	4
    --max-len		Maximum word length	64
    --no-leet		Disable leetspeak mutations	Off
    --no-years		Disable year appending	Off
    --no-combos		Disable token combinations	Off
    --combo-depth		Tokens to combine (2 or 3)	2

### Both Command

    Bash
    python main.py cli both --password "PASSWORD" [GENERATE OPTIONS]
    
Accepts --password plus all generate options listed above.

### Help
    Bash
    
    python main.py cli --help
    python main.py cli analyse --help
    python main.py cli generate --help
    python main.py cli both --help
    
### Scoring System
### Score Scale (0-4)
          Score	Label	Entropy Range	Color
          0	Very Weak	< 28 bits or common password	Red
          1	Weak	28 - 35 bits	Orange
          2	Fair	36 - 49 bits	Yellow
          3	Strong	50 - 59 bits	Green
          4	Very Strong	60+ bits	Dark Green
          
### Scoring Logic

    Custom Entropy Score — Based on Shannon entropy calculation using character pool size, with penalties for short length, low unique character ratio, and detected patterns.
    
    zxcvbn Score — Uses Dropbox's zxcvbn library for dictionary-based and pattern-based analysis.
    
    Common Password Check — Any password found in the common database is instantly scored 0 regardless of entropy.
    
    Overall Score — The minimum of Custom Score and zxcvbn Score. This conservative approach ensures the tool never overestimates password strength.

### Penalties Applied

    Condition	Penalty
    Found in common password database	Score = 0 (instant fail)
    Length < 8 characters	-2 from score
    Unique character ratio < 40%	-1 from score
    Common patterns detected	-1 from score

### Common Password Database
### Coverage
    1,043 base passwords sourced from real-world breach databases
    28,000+ expanded entries including case mutations, digit suffixes, symbol suffixes, and reversed versions
    
### Sources
    RockYou breach database analysis
    NordPass annual most common passwords reports
    Have I Been Pwned aggregated data
    SecLists common credentials collection
    
### Categories Covered

    Category	Examples
    Top Global	123456, password, qwerty, iloveyou
    Keyboard Patterns	qwerty, asdfgh, 1q2w3e4r, qazwsx
    Number Patterns	123456, 111111, 987654321
    Repeated Characters	aaaaaa, 000000
    Common Names	john, michael, jessica, ashley
    Sports	football, baseball, jordan23, messi
    Pop Culture	starwars, pokemon, minecraft, avengers
    Technology	google, facebook, iphone, github
    Animals	dragon, monkey, tiger, fluffy
    Food & Drinks	coffee, chocolate, pizza, beer
    Music	metallica, eminem, beatles, blink182
    Countries & Cities	london, paris, india, tokyo
    Trending 2024	chatgpt, crypto, bitcoin, tesla

### Detection Methods
    Direct Match — Exact match against base passwords
    Mutation Match — Checks UPPER, Title, capitalize, +digit, +symbol variants
    Stripped Match — Removes trailing digits/symbols and rechecks
    Reverse Match — Reverses the password and rechecks

 ### Wordlist Mutations
The generator applies these mutation strategies to each input token:

### 1. Case Variants
    text
    
    hello → hello, Hello, HELLO, hELLO, Hello
### 2. Leetspeak Substitutions
    text
    
    hello → h3llo, h3ll0, h€ll0, #3ll0
Substitution map:

    text
    
    a → @, 4    e → 3      i → 1, !    o → 0
    b → 8      g → 9, 6    l → 1, |    s → $, 5
    c → (, {   h → #       t → 7, +    z → 2
### 3. Year Appending
    text
    
    hello → hello1990, hello2024, hello90, hello24
### 4. Common Suffix Appending
    text
    
    hello → hello!, hello123, hello@, hello007, helloqwerty
### 5. Reverse
    text
    
    hello → olleh, Olleh
### 6. Token Combinations
    text
    
    john + fluffy → johnfluffy, fluffyjohn, john_fluffy, john.fluffy
### 7. Date Fragment Extraction
    text
    
    1990-03-15 → 1990, 90, 0315, 1503, 03151990, 19900315
    john + 1990-03-15 → john1990, john90, john0315, John1990
### 8. Initials
    text
    
    John Smith → js, JS

### Wordlist Compatibility
The exported .txt file contains one word per line. It is directly compatible with:

    Bash
    
    # Hashcat
    hashcat -m 2500 capture.hccapx wordlist.txt
    
    # John the Ripper
    john --wordlist=wordlist.txt hashes.txt
    
    # Hydra (SSH example)
    hydra -l admin -P wordlist.txt ssh://192.168.1.1
    
    # Aircrack-ng
    aircrack-ng -w wordlist.txt capture.cap
    
    # Medusa
    medusa -u admin -P wordlist.txt -h 192.168.1.1 -M ssh
    
### Sample Wordlist Output
    text
    
    fluffy
    Fluffy
    FLUFFY
    fluffy!
    fluffy123
    fluffy1990
    Fluffy1990
    flu$$y
    fl00ffy
    john
    John
    j0hn
    johnfluffy
    john_fluffy
    John.Fluffy
    js
    JS
    john1990
    ...
    
### Screenshots
### CLI — Password Analysis
    text
    
    $ python main.py cli analyse -p "monkey123"
    
    ============================================================
             PASSWORD STRENGTH ANALYSIS REPORT
    ============================================================
      Password       : monkey123
    
      COMMON PASSWORD DATABASE CHECK
      +==================================================+
      |  WARNING: THIS IS A COMMON PASSWORD!             |
      +==================================================+
    
      * OVERALL       : 0/4  Very Weak
    ============================================================

### CLI — Wordlist Generation
    text
    
    $ python main.py cli generate --name "John" --pet "Rex" --dob "1995-06-20" -o wordlist.txt
    
    [*] Generating wordlist with 2 token(s) and 1 date(s) ...
    [+] 32,456 candidates written to 'wordlist.txt' in 0.98s

### GUI — Password Analyser Tab
    text
    
    ┌────────────────────────────────────────────────────┐
    │  [Password Analyser]  [Wordlist Generator]         │
    │                                                    │
    │  Enter Password: [••••••••••••]  [Show] [Analyse]  │
    │                                                    │
    │  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░  3/4 Strong        │
    │                                                    │
    │  ┌──────────────────────────────────────────┐      │
    │  │  PASSWORD STRENGTH ANALYSIS REPORT       │      │
    │  │  Length: 15    Entropy: 89.2 bits        │      │
    │  │  NOT found in common password list       │      │
    │  │  Score: 3/4 Strong                       │      │
    │  └──────────────────────────────────────────┘      │
    └────────────────────────────────────────────────────┘
    
### GUI — Wordlist Generator Tab
    text
    
    ┌────────────────────────────────────────────────────┐
    │  [Password Analyser]  [Wordlist Generator]         │
    │                                                    │
    │  Name(s):      [John Smith, Jane        ]          │
    │  Pet name(s):  [Fluffy, Rex             ]          │
    │  DOB:          [1990-03-15              ]          │
    │  Extra:        [Yankees, pizza          ]          │
    │                                                    │
    │  [x] Leetspeak  [x] Years  [x] Combine tokens     │
    │  Min: [4]  Max: [64]                               │
    │                                                    │
    │  [Generate Wordlist]  [Export .txt]                 │
    │  Status: 48,231 candidates generated               │
    └────────────────────────────────────────────────────┘
    
### Requirements

    Package	Version	Purpose
    Python	3.8+	Runtime
    zxcvbn-python	>= 4.4.24	Pattern-based password scoring
    nltk	>= 3.8.1	Natural language processing support
    tkinter	Built-in	GUI framework (included with Python)

### Install All Dependencies
    Bash
    
    pip install -r requirements.txt
    
### Note for Linux Users
If tkinter is not available:

    Bash
    
    # Ubuntu/Debian
    sudo apt install python3-tk
    
    # Fedora
    sudo dnf install python3-tkinter
    
    # Arch
    sudo pacman -S tk
    
### Disclaimer
    This tool is intended for educational purposes and authorized security testing only.
    
    Use this tool only on systems you own or have explicit written permission to test.
    Do not use generated wordlists for unauthorized access to any system.
    The common password database is sourced from publicly available breach analyses for educational awareness.
    The author is not responsible for any misuse of this tool.
    Always follow applicable laws and regulations regarding cybersecurity testing in your jurisdiction.

### License
    This project is licensed under the MIT License. See LICENSE for details.

## Author

    Harsh Soni
    
    - GitHub: [@harshhhhh10](https://github.com/harshhhhh10)
