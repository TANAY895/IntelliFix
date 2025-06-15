import tkinter as tk
from tkinter import scrolledtext
import difflib
import autopep8
import re
import tokenize
import io
import builtins

# ------------------------------
# SET OF PYTHON BUILT-IN NAMES
# ------------------------------
BUILTINS = set(dir(builtins)) | {
    "print", "input", "return", "len", "range", "int", "str", "float", "list", "dict", "set", "tuple",
    "type", "bool", "any", "all", "sum", "max", "min", "open", "enumerate", "abs", "round", "map", "filter"
}

# ------------------------------
# FIX TYPOS IN BUILTIN NAMES
# ------------------------------
def fix_builtin_typos(code):
    changes = []
    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(code).readline))
        new_tokens = []

        for toknum, tokval, start, end, line in tokens:
            if toknum == tokenize.NAME and tokval not in BUILTINS:
                match = difflib.get_close_matches(tokval, BUILTINS, n=1, cutoff=0.7)
                if match:
                    changes.append(f"Fixed typo: {tokval} → {match[0]}")
                    tokval = match[0]
            new_tokens.append((toknum, tokval))
        
        fixed_code = tokenize.untokenize(new_tokens)
        return fixed_code, changes
    except Exception as e:
        return code, [f"Typo fix failed: {str(e)}"]

# ------------------------------
# FIX STRUCTURAL ISSUES (print, def)
# ------------------------------
def fix_structure(code):
    changes = []
    lines = code.splitlines()
    fixed_lines = []
    for line in lines:
        orig = line
        # Fix function def without parentheses
        if re.match(r'^\s*def\s+\w+\s+[^\(:]+', line):
            parts = re.split(r'\s+', line.strip(), maxsplit=2)
            if len(parts) >= 3:
                fn_name, args = parts[1], parts[2]
                line = f'def {fn_name}({args}):'
                changes.append(f"Fixed function definition: {orig.strip()}")

        # Fix print statements
        line = re.sub(r'(\bprint)\s+"([^"]+)"', r'\1("\2")', line)
        line = re.sub(r"(\bprint)\s+'([^']+)'", r"\1('\2')", line)

        # Balance parentheses if unbalanced
        if line.count('(') > line.count(')'):
            line += ')' * (line.count('(') - line.count(')'))
            changes.append(f"Balanced missing parentheses: {orig.strip()}")

        fixed_lines.append(line)
    return "\n".join(fixed_lines), changes

# ------------------------------
# FIX LOGIC (assignment vs equality)
# ------------------------------
def fix_logic(code):
    changes = []
    code, count1 = re.subn(r'\bif\s+([^\n=]+)=(?!=)', r'if \1==', code)
    if count1:
        changes.append("Replaced '=' with '==' in if condition")
    code, count2 = re.subn(r'\bwhile\s+([^\n=]+)=(?!=)', r'while \1==', code)
    if count2:
        changes.append("Replaced '=' with '==' in while loop")
    return code, changes

# ------------------------------
# FIX MISSING COLONS
# ------------------------------
def fix_colons(code):
    pattern = r"(?m)^(\s*(if|elif|else|for|while|try|except|finally|with|def|class)[^\n:]*)(\s*)(#?.*)$"
    fixed, count = re.subn(pattern, r"\1:\3\4", code)
    return fixed, [f"Added missing colons ({count}x)"] if count else []

# ------------------------------
# AUTO FORMAT CODE
# ------------------------------
def format_code(code):
    try:
        return autopep8.fix_code(code), ["Formatted with autopep8"]
    except:
        return code, []

# ------------------------------
# MASTER FIX FUNCTION
# ------------------------------
def correct_code(code):
    all_changes = []

    code, c1 = fix_structure(code)
    all_changes += c1

    code, c2 = fix_colons(code)
    all_changes += c2

    code, c3 = fix_logic(code)
    all_changes += c3

    code, c4 = fix_builtin_typos(code)
    all_changes += c4

    code, c5 = format_code(code)
    all_changes += c5

    return code.strip(), all_changes

# ------------------------------
# OUTPUT WINDOW
# ------------------------------
def show_output(orig, corrected, changes):
    out = tk.Toplevel()
    out.title("Corrected Code Output")
    out.geometry("1000x700")

    tk.Label(out, text="Original Code").pack()
    orig_box = scrolledtext.ScrolledText(out, height=10)
    orig_box.insert(tk.END, orig)
    orig_box.config(state=tk.DISABLED)
    orig_box.pack()

    tk.Label(out, text="Corrected Code").pack()
    corr_box = scrolledtext.ScrolledText(out, height=10)
    corr_box.insert(tk.END, corrected)
    corr_box.config(state=tk.DISABLED)
    corr_box.pack()

    tk.Label(out, text="Corrections Applied").pack()
    log_box = scrolledtext.ScrolledText(out, height=10)
    log_box.insert(tk.END, "\n".join(changes) or "No corrections applied.")
    log_box.config(state=tk.DISABLED)
    log_box.pack()

# ------------------------------
# MAIN UI WINDOW
# ------------------------------
def launch_app():
    root = tk.Tk()
    root.title("Python Code Corrector")
    root.geometry("1000x650")

    tk.Label(root, text="Enter Python Code Below:").pack()
    input_box = scrolledtext.ScrolledText(root, height=20, width=120)
    input_box.pack()

    def correct_and_show():
        code = input_box.get("1.0", tk.END).strip()
        corrected, changes = correct_code(code)
        show_output(code, corrected, changes)

    tk.Button(root, text="Correct Code", command=correct_and_show).pack(pady=10)
    root.mainloop()

if __name__ == "__main__":
    launch_app()
