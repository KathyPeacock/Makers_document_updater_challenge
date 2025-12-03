# Bug Reports - Document Updater

**Date:** 3/12/25
**Tester:** Kathy Peacock
**Test Environment:** macOS, Python 3.11.2

This early testing phase has identified 5 significant issues that need to be addressed before the document management system can be used in production. These issues will require additional development time before the system can proceed to user acceptance testing.

## Bug Report #1: System Cannot Handle Multiple People with Same Surname/Same filename

**Severity:** CRITICAL q
**Priority:** CRITICAL

### Summary
The current filename-based system cannot handle multiple people with the same surname. Since filenames are used as unique identifiers and the system is designed to use surnames (with full names also accepted) as filenames, it is impossible to store documents for two different people named "Smith" in the same directory.

This also impacts scenarios with different people with the same surname existing in different directories, as subsequent listing and filtering is not effective/comprehensive.

### Impact

- **For Developers:** Fundamental design flaw - filename-based identification doesn't support real-world naming scenarios
- **For Stakeholders:** System is unusable in any organization with more than a few people, as surname collisions are inevitable and full name collisions likely.

### Further context:

Surname "Smith" is held by approximately 1% of the population (~700,000 people). Other common surnames (Jones, Williams, Taylor, Brown) each represent hundreds of thousands of people. In any organization with >50 people, surname collisions are virtually guaranteed, especially in contexts with concentrated demographics.

### Steps to Reproduce

Attempt to create two files with the same surname in the originals directory:

```
   test_directory/
   ├── originals/
   │   ├── Smith     (John Smith's address)
   │   └── Smith     (Sarah Smith's address) ← Cannot create!
```

Operating system prevents creating second file named "Smith"
Cannot test or use the system with realistic datasets

### Expected Result
System should be able to handle multiple people with the same name.

### Actual Result

Cannot create files with duplicate filenames. System design assumes surnames are unique identifiers.
(No way to distinguish between John Smith and Sarah Smith, even if they were both allowed to be stored in same directory.)

screenshot_1.png shows error when trying to add second Smith.


### Further Notes:

Using full names helps but has issues (see below, Bug #2, inconsistent formatting)
This issue requires a fundamental redesign of filename handling and identifier requirements.


## Bug Report #2: Spaces Removed from Filenames in Finals Directory

**Severity:** HIGH  
**Priority:** HIGH

### Summary
When processing files with spaces in filenames (e.g., "John Smith"), the program removes spaces when copying to the finals directory, resulting in concatenated filenames (e.g., "JohnSmith").

### Impact
- **For Developers:** File handling logic incorrectly processes filenames containing spaces, leading to corrupted filenames in generated finals folders.
- **For Stakeholders:** Document naming convention is corrupted; files become harder to identify and have knock-on effects for future data processing systems expecting properly formatted names. If this system is used in production, document retrieval and/or further data handling could fail due to filename mismatch.

### Steps to Reproduce
1. Create a test directory with the following structure:
   ```
   test_directory/
   ├── originals/
   │   └── John Smith    (file containing UK address for John Smith)
   ├── updates/
   └── allowlist         (containing text: "John Smith")
   ```

    Full test data used: 
    ```
    John Smith
    417 Mohammed fall
    Amberstad
    M79 1WF
    ```

2. Run the program:
   ```
   python document_updater.py test_directory
   ```

3. Check the finals directory:
   ```
   ls test_directory/finals/
   ```

### Expected Result
- Finals directory should contain a file named `John Smith` (with space preserved)
- (Filename should exactly match the original filename)

### Actual Result
- Finals directory contains a file named `JohnSmith` (no space)
- File contents remain correct (address data is intact)
- `screenshot_2.png` shows finals directory with "JohnSmith" filename
- Verified across multiple test scenarios:
  - Test: fullname_allowlist (originals only)
  - Test: fullname_updates (updates only)
  - Test: fullname_both (file in both directories)
  - Test: mixed_formats (mix of surname-only and full names)
- Issue occurs consistently regardless of whether file comes from originals or updates

### Additional Notes
- File content (address data) is NOT corrupted - only the filename is affected
- Issue occurs with any filename containing spaces
- This suggests the file reading/writing logic doesn't properly handle filenames with whitespace


## Bug Report #3: Special Characters Removed from Filenames

**Severity:** HIGH  
**Priority:** HIGH

### Summary
Similar to Bug #1, above ... Filenames containing special characters such as apostrophes (') or hyphens (-) have these characters removed when files are copied to the finals directory.

### Impact
- **For Developers:** File handling doesn't preserve special characters in filenames.
- **For Stakeholders:** Document naming convention is corrupted; files become harder to identify and have knock-on effects for future data processing systems expecting properly formatted names. If this system is used in production, document retrieval and/or further data handling could fail due to filename mismatch.

- Further context: This is particularly problematic for UK addresses where:
    - Irish surnames commonly contain apostrophes (O'Brien, O'Connor, O'Neill)
    - Double-barreled surnames contain hyphens (Smith-Jones, Wilson-Clarke)
    - According to UK naming conventions, these are valid and common surname formats. 
    - This bug could affect a significant portion of documents, as well as brand reputation.

### Steps to Reproduce
1. Create a test directory with filenames containing special characters:
   ```
   test_directory/
   ├── originals/
   │   ├── O'Leary       (file with apostrophe)
   │   └── Smith-Jones   (file with hyphen)
   ├── updates/
   └── allowlist         (containing: "O'Leary" and "Smith-Jones")
   ```
    
    Full test data used:
    ```
    Mabel O'Leary
    42 High Street
    London
    SW1A 1AA

    Sarah Smith-Jones
    07 Tina plains
    Jamesburgh
    SL50 2UH
    ```

2. Run the program:
   ```
   python document_updater.py test_directory
   ```

3. Check finals directory filenames:
    ```
    ls test_directory/finals/
    ```

### Expected Result
- Finals directory should contain files with original names preserved:
  - `O'Leary` (with apostrophe)
  - `Smith-Jones` (with hyphen)

### Actual Result
- Special characters are removed from filenames:
  - `OLeary` 
  - `SmithJones` 
- File contents remain intact

- screenshot_3.png shows finals directory with special characters omitted
- Issue occurs consistently


### Related Issue
This appears related to Bug #1 (spaces removed from filenames), suggesting a broader issue with filename character handling in the file copying logic.



## Bug Report #4: Allowlist Doesn't Filter Files from Originals, incorrectly ommitted from Finals.

**Severity:** HIGH  
**Priority:** HIGH

### Summary
In a mixed scenario with multiple files, the program fails to include files from originals that are listed in the allowlist (and not in updates). Only files from updates appear in finals, even when originals files should be allowed through via allowlist.

### Impact
- **For Developers:** Core allowlist logic is not functioning correctly in multi-file scenarios
- **For Stakeholders:** Documents that should be approved (via allowlist) are being excluded = potential for missing critical documents in final output.
- Documents may be lost or not processed when they should be included.

### Steps to Reproduce
1. Create a test directory with the following structure:
   ```
   test_directory/
   ├── originals/
   │   ├── Turner    (NOT in allowlist)
   │   ├── Howell    (in allowlist, also in updates)
   │   ├── Holmes    (in allowlist, NOT in updates) (KEY FILE)
   │   └── Smith     (NOT in allowlist, also in updates)
   ├── updates/
   │   ├── Howell    (different address)
   │   └── Smith     (different address)
   └── allowlist     (containing: "Holmes" and "Howell")
   ```

    Full test data used:
    ```
    Callum Holmes
    643 Davis turnpike
    Wrightbury
    LU2E 3QJ

    Raymond Howell
    70 Singh street
    East Lawrencechester
    M9W 2GT

    Clare Smith
    6 Mills parks
    North Phillipchester
    HA0E 2RF

    Iain Turner
    4 Gerard villages
    East Josephstad
    SG6M 8FW
    ```

2. Run the program:
   ```
   python document_updater.py test_directory
   ```

3. Check finals directory:
    ```
    ls test_directory/finals/
    ```

### Expected Result
Finals should contain:
- Howell (from updates - supersedes originals)
- Smith (from updates)
- **Holmes (from originals via allowlist)**
Finals should NOT contain:
- Turner (not in allowlist)

### Actual Result
Finals contains:
- Howell (from updates)
- Smith (from updates) 
- **Holmes MISSING** = INCORRECT

(The file "Holmes" which exists in originals and is listed in allowlist does NOT appear in finals.)

### Further Notes
The program correctly:
- Includes files from updates (Howell, Smith)
- Applies updates superseding logic (Howell from updates, not originals)
- Excludes Turner (not in allowlist)

The program incorrectly:
- Fails to include Holmes from originals despite being in allowlist

### Suggested Fix Area/Further Tests
Review the logic that processes files from originals directory when allowlist is present. The allowlist matching/filtering logic may not be executing correctly, particularly in multi-file scenarios.


## Bug Report #5: Program Crashes on Empty Allowlist File

**Severity:** MEDIUM  
**Priority:** MEDIUM

### Summary
The program crashes with an `IndexError` when the allowlist file exists but is empty. (However, an empty droplist file is handled correctly without error.)

### Impact
- **For Developers:** Inconsistent error handling between droplist and allowlist.
- **For Stakeholders:** System is unreliable, crashing instead of providing useful feedback when allowlist is accidentally left empty. Production system could crash during processing.

### Steps to Reproduce
1. Create a test directory with the following structure:
   ```
   test_directory/
   ├── originals/
   │   └── Cunningham    (file containing UK address)
   ├── updates/
   └── allowlist         (empty file - no content)
   ```
    
    Full test data used: 
    ```
    Gillian Cunningham
    33 Leon lights
    Lake Jill
    W2 5JD
    ```

2. Run the program:
   ```
   python document_updater.py test_directory
   ```

### Expected Result
- Program should handle empty allowlist gracefully
- Either: Process normally (empty allowlist = no files allowed from originals)
- Or: Display user-friendly error message: eg. "ERROR: allowlist file is empty"

### Actual Result
Program crashes with the following error:
```
Traceback (most recent call last):
  File "/Users/kathypeacock/Projects/extending-testing-resources/unit2/03_resources/document_updater.py", line 40, in <module>
    line = list_data[0] if listfiletype == 'allow' else list_data
           ~~~~~~~~~^^^
IndexError: list index out of range
```

Tested multiple scenarios with empty allowlist including:

**Originals only, empty allowlist**
- Result: as above

**Originals + Updates, empty allowlist**  
- Result: as above

**Same setup with empty droplist instead**
- Result: SUCCESS (no crash)

To confirm the issue was with allowlist specifically and not directory setup:
- Ran same test with allowlist containing "Cunningham": SUCCESS.
- This confirms directory structure was correct; only empty allowlist causes crash.


### Further observation
Line 40 in document_updater.py attempts to access `list_data[0]` without checking if list is empty.
Consider making behavior consistent between empty droplist and empty allowlist.
