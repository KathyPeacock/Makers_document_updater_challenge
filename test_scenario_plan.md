# Test Scenario Plan

## Priority 1: The 4 Given Examples in spec (MUST TEST)


1.1: **Example 1 - Droplist blocks originals**

- File in originals
- Same file listed in droplist
*Expected: NOT in finals*


1.2: **Example 2 - Updates supersedes allowlist**

- File in originals (listed in allowlist)
- Same file in updates (different address)
*Expected: Updates version in finals*


1.3: **Example 3 - Droplist irrelevant for updates-only files**

- File NOT in originals
- File in updates
- File listed in droplist
*Expected: Updates version in finals (droplist has no effect)*


1.4: **Example 4 - Droplist doesn't mention file**

- File in originals
- Droplist exists but doesn't mention this file
*Expected: File from originals in finals*



## Priority 2: Core Logic Tests (HIGH VALUE)


2.1: **Multiple files - mixed scenario**

- Some files only in originals
- Some files only in updates
- Some files in both
- Allowlist mentions some from originals
*Expected: Correct selection from each category*

2.2: **Empty list files**

- Allowlist exists but is empty
- OR droplist exists but is empty
*Expected: How does program handle this?*

2.3: **All files from updates only**

- Originals folder is empty
- Updates has multiple files
*Expected: All updates files in finals*



## Priority 3: Edge Cases (IF TIME PERMITS)


3.1: **Different first names, same surname**

- eg originals/Smith: "John Smith..."
- eg updates/Smith: "Sarah Smith..."
*Expected: Does it care about first names or just match on surname?*


3.2: **Case sensitivity test**

- File named "<Name>" in originals (uppercase, standard)
- Allowlist contains "<name>" (lowercase)
*Expected: Does it match?*


3.3: **Special characters in surnames**

- Surnames like "O'Leary" or "Smith-Jones"
*Expected: Does it handle them correctly?*



## Priority 4: Error Handling - (VERIFY ERROR IF TIME (not message))


4.1: **Neither allowlist nor droplist exists**

- Only originals and updates folders
*Expected: Should error (challenge says it expects one or the other)*

4.2: **Both allowlist AND droplist exist**

*Expected: Should error (challenge says expects "either... or")*

4.3: **Inconsistent address formats**

- Some with 4 lines, some with 5 lines (eg Flat 50 on separate line as per fake.address examples)
*Expected: Does validation catch this? Should error. (Challenge mentions "correctly formatted addresses")*

4.4: **Extra whitespace in list files**

- Allowlist has "<Name >" (with trailing space)
*Expected: Does it still match "<Name>"?*
