"""Standalone eval harness for the bundled local LLM tiers.

Run inside the container (needs llama_cpp + the GGUF weights, which only
exist in the Linux image, not the Windows dev machine):
    docker run --rm --entrypoint python <image> -m router.eval_local

Deliberately uses different phrasing/domains than sample_input/*.json so
this measures generalization, not memorization of the dev examples -
matching the org's own warning that final scoring uses randomized prompts.
"""
from router import local_llm
from router.solvers import looks_like_python, python_syntax_error

CASES = [
    ("sentiment", "How would someone likely feel reading this comment: 'Absolutely blown away by the customer support, they went above and beyond.'"),
    ("sentiment", "Tag the emotional tone of this restaurant review: 'Service was slow and the waiter seemed annoyed the whole time.'"),
    ("sentiment", "Rate the tone as positive, negative, or neutral: 'The package arrived on time.'"),
    ("sentiment", "What's the overall attitude expressed here? 'I guess it works, but I expected more for the price.'"),
    ("sentiment", "Determine the sentiment: 'Honestly one of the worst experiences I've had with an airline.'"),

    ("ner", "Pull out any people, companies, places, or dates mentioned: 'Sundar Pichai spoke at the Google I/O conference in Mountain View on May 14th.'"),
    ("ner", "Who and what organizations are named in this sentence? 'Serena Williams signed a sponsorship deal with Nike in 2003.'"),
    ("ner", "Identify entities: 'The meeting between Angela Merkel and Emmanuel Macron took place in Berlin last November.'"),
    ("ner", "What locations and dates appear here? 'The festival runs from July 4th to July 10th in Austin.'"),
    ("ner", "Tag the named entities in: 'Jeff Bezos stepped down as Amazon CEO in 2021.'"),

    ("factual", "In simple terms, why is the sky blue?"),
    ("factual", "What causes seasons to change on Earth?"),
    ("factual", "Briefly, what is DNA?"),
    ("factual", "Why do we have leap years?"),
    ("factual", "What's the difference between weather and climate?"),

    ("summarization", "Condense to one sentence: The regional water authority announced Tuesday that a new filtration plant would begin operations next spring, aiming to reduce turbidity complaints that have persisted since last year's flooding damaged the original treatment facility."),
    ("summarization", "Summarise in exactly 2 sentences: A mid-sized software firm laid off 12% of its staff on Thursday, citing slower-than-expected enterprise contract renewals. The CEO said the company would redirect savings toward its AI product line, which has seen strong early customer interest despite not yet being profitable."),
    ("summarization", "Give a one-sentence summary: Archaeologists uncovered a previously unknown burial chamber beneath a temple complex, containing pottery and tools dated to roughly 3,000 years ago, suggesting the site was inhabited far earlier than historians had assumed."),

    ("code_debug", "Fix the bug: ```def factorial(n):\n    if n == 0:\n        return 0\n    return n * factorial(n-1)```"),
    ("code_debug", "This has an off-by-one error, fix it: ```def last_index(lst):\n    return len(lst)```"),
    ("code_debug", "Find and correct the bug: ```def average(nums):\n    return sum(nums) / len(nums) + 1```"),

    ("code_gen", "Write a Python function reverse_words(s) that reverses the order of words in a string."),
    ("code_gen", "Write a Python function count_vowels(s) that returns the number of vowels in a string."),
    ("code_gen", "Write a Python function is_prime(n) that returns True if n is a prime number."),
]


def main():
    print(f"general model available: {local_llm.available('sentiment')}")
    print(f"code model available: {local_llm.available('code_gen')}\n")
    for category, prompt in CASES:
        ans = local_llm.answer(category, prompt)
        status = "OK" if ans is not None else "REJECTED (sanity check or unavailable)"

        if ans is not None and category in ("code_debug", "code_gen") and looks_like_python(ans):
            err = python_syntax_error(ans)
            if err:
                status = f"SYNTAX ERROR: {err}"

        print(f"[{category}] {status}")
        print(f"  Q: {prompt}")
        print(f"  A: {ans}")
        print()


if __name__ == "__main__":
    main()
