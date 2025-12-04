# Makers_document_updater_challenge - Process Reflection 👾

## Overview

This challenge involved testing a Python document management program that processes files from `originals` and `updates` directories according to `allowlist` or `droplist` rules. The focus was on demonstrating systematic testing process and providing actionable feedback to developers, rather than exhaustive bug hunting. I also wanted to demonstrate plenty of scripted test data generation, as I enjoyed learning about this earlier in the week, and I'm excited about the potential to combine automated testing, scenario set-up, and test data generation in creative ways. The challenge required focus on the Faker tool for this; I wanted to dive deeper into its functionality and learn more about seeding and reseeding in a more complex test planning and execution context.

**This repo contains:**
- `bug_reports.md` = 5 bug reports with comprehensive reproduction steps
- multiple Test data generation scripts using Faker (preparing for automated, manual and hybrid testing)
- Process documentation including brief planning of important scenarios to cover, product decision-flow map, test notes and screenshot evidence.
- `document_updater.py` = program being tested (+ data example provided)

---

## Approach & Methodology

### 1. Understanding Before Testing

Rather than diving straight into execution, I began by thoroughly analyzing the program requirements. The description was complex with multiple conditional paths, so I created a visual decision tree in Excalidraw to map out the logic. I wish I'd done this earlier, as I spent quite a while trying to wrap my head around it from the 'spec' description.

The diagram actually became my testing touchstone. As this was done across 2 working days and was a complex scenario, I found that even with my clear planning notes with expectations listed, I had to constantly refer back to make sure I was understanding the product expectations properly.

### 2. Test Data Generation

I used Python's Faker library with UK locale to generate realistic test data.
I spent a lot of time creating scripts to set up test scenarios, starting with the 4 main simple examples given in the challenge.
I began by replicating the data generation methods from previous exercises, and built up functionality from there.
This was very much a 'learn as I go' situation, with plenty of trial and error... 

**Here are some of the knots I got myself into and untangled..!:**

- Initial script created files named "Smith" containing addresses for "Jones." Fixed using Faker's seed feature to ensure filename surname matched document content:
```python
Faker.seed(hash(surname))  # Same surname = same first name
Faker.seed(hash(surname + folder_path))  # Different addresses per folder
```

- `fake.street_address()` sometimes returned multi-line results (eg. "Flat 50\n123 Street"). Solved by using building_number and street_name separately to ensure consistent 4-line format as a baseline for these early tests. (I had planned to come back to this and do some tests of different address formats to test the 'correct format' requirement, but time didn't allow.)

- I was able to create reusable test generation functions that produced coherent, realistic test scenarios showing same person with updated addresses across folders as a base line for data generation.

### 3. Test Scenario Design

I really enjoyed automating scenario set-ups as well as data, something which I hadn't considered before this challenge. This made the testing process much less overwhelming (we were given a suggested 2 hour limit for actual testing). I actually wish I'd done more of this, ie more than the first 5 basic tests, as manual creation of scenario directories with the specific data for my different edge-case tests proved much more time consuming than I thought, and more prone to human error.

I particularly liked being able to print expected results and method-specific program running instructions in the actual output of the scenario generation. I wondered at the beginning if I was doing too much commenting and printing, but it actually was a life-saver when it came to quickly running a lot of different tests and keeping track of expectations. I could copy and paste automated expectations and commands into the terminal = quicker and less errors in test execution. 

If I had more time I'd code in asserts to cut down even more on the manual side of things. Even with my automated scenarios, I had to manually check each result, which was time consuming.

NB: it may be a side-effect of my ADHD, but I certainly found devoting more time to automation in all areas led to a more efficient, accurate (and enjoyable) test session as the data started to blur into one and become repetetive (very much same but different) with time...

My edge cases balanced automation with manual exploratory testing and ad-hoc manual data creation. Manual worked best with these very specific edge cases where lots of data was not the priority, just specificity. Also, once a few special characters were tested, for example, with limited time to test it was prudent to avoid as much equivalence testing as possible.


## Testing Techniques Demonstrated include...
- Decision path testing (each branch of logic tree)
- Equivalence partitioning (files in originals only, updates only, both)
- Exploratory testing (edge cases like apostrophes in surnames, and ad hoc ideas)
- Data-driven testing
- Automated test data and scenario generation with varying complexities and helpful print formatting
- Bug reporting 
- Communication with awareness of developer and stakeholder contexts


## Technical Skills Demonstrated include...
**Python & Faker:**
- Locale-specific data generation (`en_UK`)
- Using `seed()` for reproducible varied data
- Combining Faker methods for custom formats
- File and directory management with `os` module

**Git version control**


## Reflection & Learning

### What Went Well
- Visual analysis (decision tree) clarified complex logic before testing
- Iterative problem-solving with test data (addressed issues as they arose)
- Found significant bugs including architectural flaw
- Professional documentation suitable for real-world feedback

### What I'd Improve
- Could have discovered the filename issues earlier by testing full names in Priority 1
- Spent over 2-hour testing limit (good learning about time boxing). Too much fun being had! (Plus inexperience with manual testing time requirements and VS code direcory structure quirks)
- Could have added assertions to my automated test generations for further efficiency and accuracy, now I've discovered how much printing with dynamic data specific to each method-call helps my organisation!
- With more time I would have liked to have less equivalence and more coverage on the 'basic' tests before diving into edge cases. I didn't test with large numbers of files, or do as much as I'd have liked with the address data (such as different formats, and combing through the data accuracy in finals etc).
- The time spent creating the decision tree diagram proved invaluable throughout testing - I'd prioritise this before any test planning, and really comb through the spec, being more confident to have an 'off the record' play with functionality to inform my test planning.

---

## ... to conclude!

This challenge demonstrated systematic testing process, varied use of automation, and professional communication skills. The focus on understanding requirements first, combined with hybrid testing approaches, led to discovery of both surface bugs and fundamental design issues. I've become far more confident (and creative) with automating test data, and the documentation is tailored as real-world early feedback to a development team as well as stakeholders.

**Most valuable learning point...** Knowing when to stop testing and start documenting! Quality feedback with clear reproduction steps is more valuable than an exhaustive bug list without context.

:)
