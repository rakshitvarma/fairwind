"""Zero-token deterministic solvers.

These only answer when they can be *sure* they're correct — anything
ambiguous falls through to the Fireworks batch. Wrong free answers are
worse than costing a few tokens, since a single accuracy-gate failure
takes the whole submission off the leaderboard.
"""
import ast
import operator
import re
from typing import Optional

_ALLOWED_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

_EXPR_RE = re.compile(r"[-+]?\d+(?:\.\d+)?(?:\s*[-+*/^%]\s*[-+]?\d+(?:\.\d+)?)+")


def _safe_eval(node):
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPS:
        return _ALLOWED_OPS[type(node.op)](_safe_eval(node.left), _safe_eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPS:
        return _ALLOWED_OPS[type(node.op)](_safe_eval(node.operand))
    raise ValueError("unsupported expression")


def _format_result(result):
    if isinstance(result, float):
        result = round(result, 6)  # clear binary float noise (e.g. 46.800000000000004)
        if result.is_integer():
            result = int(result)
    return str(result)


def try_solve_math(prompt: str) -> Optional[str]:
    """Solve prompts that are *just* a bare arithmetic expression.

    Deliberately conservative: word problems ("if a shirt costs $50 and is
    discounted 20%...") need real language understanding to extract the
    right operation, so they're left to Fireworks rather than risking a
    wrong local answer.
    """
    text = prompt.strip().rstrip("?.! ")
    # Strip common lead-ins like "What is" / "Calculate" / "Solve:"
    text = re.sub(r"^(what is|calculate|compute|solve|evaluate)\s*:?\s*", "", text, flags=re.I)

    match = _EXPR_RE.fullmatch(text.replace("^", "**").replace(" ", ""))
    if not match:
        return None
    return evaluate_expression(text)


def evaluate_expression(expr: str) -> Optional[str]:
    """Safely evaluate a bare arithmetic expression string (numbers and
    +-*/^%() only). Used both for prompts that are already a bare
    expression, and for expressions a local model extracted from a word
    problem - in the latter case the model's output is trusted for
    *extraction only*; the actual arithmetic is still done here, in code,
    so a small model's well-known weakness at doing the arithmetic itself
    can't produce a wrong answer.
    """
    text = (expr or "").strip()
    # Models sometimes append "= <their own computed value>" despite being
    # told not to - discard that and evaluate only the expression part
    # ourselves, since trusting the model's own arithmetic is exactly what
    # this function exists to avoid.
    text = text.split("=")[0]
    text = text.replace("^", "**").replace(",", "").replace(" ", "").rstrip("?.!")
    if not text:
        return None
    try:
        tree = ast.parse(text, mode="eval")
        result = _safe_eval(tree.body)
    except Exception:
        return None
    return _format_result(result)


# Code debugging / generation deliberately have no local deterministic
# *answering* path: verifying arbitrary submitted code needs sandboxed
# execution and inferred test cases, which is high-effort and unreliable to
# build correctly under time pressure. Both categories are always routed to
# the Fireworks batch. We do, however, cheaply verify the syntax of what
# comes back (zero tokens) so an obviously broken answer can trigger one
# corrective call instead of silently failing the accuracy gate.

_PY_HINT_RE = re.compile(r"\bdef \w+\(|\bpython\b|\breturn\b", re.I)
_OTHER_LANG_RE = re.compile(
    r"\bpublic (class|static)\b|#include|\bfunction\s*\w*\s*\(|\bconsole\.log\b|"
    r"\bSystem\.out\b|\bvar \w+\s*=|\blet \w+\s*=", re.I
)


def looks_like_python(text: str) -> bool:
    return bool(_PY_HINT_RE.search(text)) and not _OTHER_LANG_RE.search(text)


def strip_code_fence(code: str) -> str:
    """Remove a leading/trailing markdown code fence. The model is asked
    for "code only," but often wraps it in ```python ... ``` anyway - if
    the returned answer text still has that fence, anything that tries to
    exec() it literally hits a SyntaxError on the fence markers themselves,
    even though the code inside is fine."""
    return re.sub(r"^```(python)?\s*|\s*```$", "", code.strip(), flags=re.I)


def python_syntax_error(code: str) -> Optional[str]:
    """Return None if `code` parses as valid Python, else the error message."""
    try:
        ast.parse(strip_code_fence(code))
        return None
    except SyntaxError as exc:
        return str(exc)
