# AI_Prompts.md

This file documents the use of AI (Claude Sonnet 4.6, Anthropic) during the development of this project

---

## Model Used

**Claude Sonnet 4.6** — via [claude.ai](https://claude.ai)

---

## Most Relevant Prompt

### Auditing the repository against the lab guidelines

**Context:** We needed to assess the current state of our GitHub repository against the ING8100 Lab 3 reproducibility requirements, identify what was already done, what was missing, and what still needed to be completed.

**Prompt used:**
> This repo https://github.com/mathisors/spine-B0-homogeneity-at-7T should follow this lab guidelines: https://reproducible-research.polymtl.ca/fr/lab3/, review the requirements and tell me what is well done, what is not, and what need to be done to complete it. 

**Why it was effective:**
The prompt is effective because it provides: the exact repository URL and the exact guidelines URL. This gives the model two clear and verifiable sources. The instruction "tell me what is well done, what is not, and what needs to be done" imposes a three-part output structure (done / not done / to do) that maps directly onto a grading review. Finally, the prompt is deliberately open-ended about the way to present the results, which lets the model choose the most useful format as a table or categorized list.

**Output:** A structured audit of the repository covering all graded criteria from the lab (README, LICENSE, CONTRIBUTING, code of conduct, branch protection, issues, folder structure, virtual environment, scripts, report, `.gitignore`, Git workflow, and AI prompt documentation), with a clear distinction between what was already in place, what was partially done, and what remained to be added.