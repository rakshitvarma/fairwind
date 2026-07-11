export const EXAMPLES: { category: string; label: string; prompt: string }[] = [
  { category: "math", label: "Math", prompt: "A store marks up a $40 item by 30% and then offers a 10% discount on the marked-up price. What is the final price?" },
  { category: "factual", label: "Factual", prompt: "Explain what a black hole is in simple terms." },
  { category: "sentiment", label: "Sentiment", prompt: "Classify the sentiment: 'The food was okay, nothing special, but the service was excellent.'" },
  { category: "summarization", label: "Summary", prompt: "Summarise the following in one short sentence: Researchers found that participants who slept less than six hours a night for a week showed slower reaction times and reduced memory recall compared to a control group that slept eight hours." },
  { category: "ner", label: "NER", prompt: "Extract all named entities from: 'Marie Curie won the Nobel Prize in Physics in 1903 while working in Paris.'" },
  { category: "code_debug", label: "Code debug", prompt: "Find and fix the bug: ```def is_even(n):\n    return n % 2 == 1```" },
  { category: "code_gen", label: "Code gen", prompt: "Write a Python function is_palindrome(s) that returns True if a string reads the same forwards and backwards, ignoring case and spaces." },
  { category: "logic", label: "Logic", prompt: "Three boxes are labeled 'Apples', 'Oranges', and 'Mixed', but all labels are wrong. You may pick one fruit from one box to determine the correct labels. Which box should you pick from, and why?" },
];
