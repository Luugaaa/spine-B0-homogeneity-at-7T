## Review checklist for @Luugaaa @Yolaatar

### AI usage

- [x] I understand that:
  - AI may only be used for **non-substantive assistance** (e.g., grammar checking my review text, contextualizing public materials)
  - **All evaluative decisions**—including scoring, accept/reject recommendations, and assessments of correctness, quality, and reproducibility—must be made exclusively by me, not AI
  - I bear full responsibility for all judgments, recommendations, and technical claims in this review
  - I will disclose any AI assistance at the conclusion of my review

### Code of Conduct

- [x] The repository contains a Code of Conduct.
- [x] I confirm that I have read and will adhere to the Code of Conduct of the repository under review.

### General checks

- [x] **Repository:** Is the source code for this software available at [spine-B0-homogeneity-at-7T](https://github.com/mathisors/spine-B0-homogeneity-at-7T)?
- [x] **License:** Does the repository contain a plain-text LICENSE or COPYING file with an open-source license?
- [ ] **How to cite:** Does the repository provide instructions on how to cite the project? *No instructions regarding how to cite the project.*
- [x] **Repository organization:** Is the repository structure clear and easy to navigate? *Yes it's fully clear and easy to understand*. 
- [x] **README.md:** Does the repository contain a README describing the project and installation procedure in a sufficient but synthetic manner? *Yes it is described. We find it sufficient (aside for the missing dependency mentioned below) and synthetic enough.*
- [X] **Research artifacts:** Are research artifacts (code, data, documentation, notebooks, etc.) openly available? *All research artifacts are openly available, including the data (available on OpenNeuro).* 

### Reproducibility

- [ ] **Dependencies:** Are all required dependencies clearly documented? *The FSL dependency was missing (issue #24, PR #26). Moreover, the version of SCT was not given (issue #23, PR #25).*
- [X] **Functionality documentation:** Is the core functionality of the software documented to a satisfactory level (e.g., API method documentation)? *Yes. How to use it and the purpose of this project are sufficiently clear and well defined. The code is also sufficiently documented.*
- [X] **Example usage:** Do the authors provide working examples demonstrating how to run the software? *Yes they do provide examples demonstrating how their project works. These examples include how to download the data used in the example.*
- [X] **Functionality:** Does the software execute successfully following the documentation (without errors)? *Yes, aside from the dependency issue.*
- [x] **Correctness of claims:** Does the software behave as described and produce the expected outputs/results? *Yes. The advertised output and results are the same as what we found when running the code. There is only a very small non significant difference due to usual randomness instabilities. *
- [x] **Performance claims:** If performance claims exist, have they been verified? (If none exist, check this item.) *No performance claim in the repo. They do warn the user that the processing can take time. It does.*
- [X] **Reproducibility of results:** Can the project be reproduced using only the information provided in the repository? *Yes it can be, once the dependancies are fixed. Note that installing the correct depedancies was fairly easy, even before our review. Now it should be even more direct though.*

### Open-source development history

- [x] **Open development:** Does the repository show evidence of public and iterative development (issues, pull requests, commits)? *Yes. Before our review there were 9 closed issues and 12 PR. So there is stong evidence that this project is the result of continious work.* 

### Community guidelines

- [x] The repository includes guidelines for:
  1. Contributing to the software  
  2. Reporting issues or bugs  
  3. Seeking support or help

### AI Disclaimer

AI was used for non-substantive assistance, like identifying the source of an error and for simple grammar checks.