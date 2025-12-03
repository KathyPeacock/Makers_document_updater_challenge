1. **Example 1 - Droplist blocks originals**

Using surname: Anderson
Created: test_example_1_droplist_blocks_originals/originals/Anderson
Created droplist containing: Anderson
EXPECTED: Anderson should NOT appear in finals
Run with: python document_updater.py test_example_1_droplist_blocks_originals

OBSERVED: Originals contains Parry, Anderson. No Updates. Droplist contains Anderson. Finals contains Parry (address as expected from originals).
`PASS`


2. **Example 2 - Updates supersedes allowlist**

Using surname: Richardson
Created: test_example_2_updates_wins/originals/Richardson
Created: test_example_2_updates_wins/updates/Richardson
Created allowlist containing: Richardson
EXPECTED: Richardson from UPDATES folder in finals (not originals version)
Run with: python document_updater.py test_example_2_updates_wins

OBSERVED: Originals contains Owen, Richardson. Updates contains Owen, Richardson (different addresses as expected). Allowlist contains Richardson. Finals contains Owen (address from updates), Richardson (address as expected from updates). 
`PASS`


3. **Example 3 - Droplist irrelevant for updates-only files**

Using surname: Owen
Created: test_example_3_droplist_irrelevant/updates/Owen
Created droplist containing: Owen
EXPECTED: Owen from updates SHOULD appear in finals (droplist has no effect)
Run with: python document_updater.py test_example_3_droplist_irrelevant

OBSERVED: No Originals. Updates contains Jones, Owen. Droplist contains Owen. Finals contains Jones, Owen (addresses as expected from Updates.) 
`PASS`


4. **Example 4 - Droplist doesn't mention file**

Using surnames: Bennett and Hardy
Created: test_example_4_droplist_nomatch/originals/Bennett
Created droplist containing: Hardy (NOT Bennett)
EXPECTED: Bennett SHOULD appear in finals (not blocked by droplist)
Run with: python document_updater.py test_example_4_droplist_nomatch

OBSERVED: Originals contains Bennett, Smith. No Updates. Droplist contains Hardy. Finals contains Bennett, Smith (addresses as expected from Originals.)
`PASS`



## (Priority 2.1)

5. **Example 5 - Multiple files - mixed scenario**

Surnames:
  - Turner: Only in originals (NOT in allowlist)
  - Smith: Only in updates
  - Howell: In BOTH originals and updates
  - Holmes: In originals + in allowlist
  - Smith: In originals but NOT in allowlist
Created: test_example_5_mixed_scenario/originals/Turner
Created: test_example_5_mixed_scenario/originals/Howell
Created: test_example_5_mixed_scenario/originals/Holmes
Created: test_example_5_mixed_scenario/originals/Smith
Created: test_example_5_mixed_scenario/updates/Smith
Created: test_example_5_mixed_scenario/updates/Howell

Allowlist contains: Holmes, Howell

EXPECTED in finals:
  ✓ Smith (from updates)
  ✓ Howell (from updates, supersedes originals)
  ✓ Holmes (from originals via allowlist)

EXPECTED NOT in finals:
  ✗ Turner (not in allowlist)
  ✗ Smith (not in allowlist)

Run with: python document_updater.py test_example_5_mixed_scenario

OBSERVED: Originals contains Holmes, Howell, Smith, Turner. Updates contains Howell, Smith (addresses different as expected). Allowlist contains Holmes, Howell. Finals contains Howell (address as expected from updates), Smith (address as expected from updates). 
Finals DOES NOT contain Holmes, as we expect via allowlist.
`FAIL`
`**BUG**`


6. **Example 6 - Empty list files** 
- Allowlist exists but is empty
- OR droplist exists but is empty
*Expected: How does program handle this?*
Run with: python document_updater.py test_example_6_empty_list

Originals contains: Cunningham
Updates empty.
Allowlist empty.
EXPECTED: Empty finals list.
OBSERVED: Program not run, error recieved:

Traceback (most recent call last):
  File "/Users/kathypeacock/Projects/extending-testing-resources/unit2/03_resources/document_updater.py", line 40, in <module>
    line = list_data[0] if listfiletype == 'allow' else list_data
           ~~~~~~~~~^^^
IndexError: list index out of range

`FAIL`

Originals contains: Cunningham
Updates contains: Cunningham (different address)
Allowlist empty.
EXPECTED: finals to contain Cunningham, address from updates.
OBSERVED: same error as above.

Traceback (most recent call last):
  File "/Users/kathypeacock/Projects/extending-testing-resources/unit2/03_resources/document_updater.py", line 40, in <module>
    line = list_data[0] if listfiletype == 'allow' else list_data
           ~~~~~~~~~^^^
IndexError: list index out of range

`FAIL`

**(Now I want to check it runs as expected with allowlist with data, so I know it's not an error with my directory setup.)**

Originals contains: Cunningham
Updates contains: Cunningham (different address)
Allowlist contains: Cunningham
EXPECTED: Finals contains Cunningham (address from originals)
OBSERVED: as expected
`PASS`

**Quick test add droplist as well so both lists present on otherwise passing scenario**
**different name droplist**

Originals contains: Cunningham
Updates contains: Cunningham (different address)
Allowlist contains: Cunningham
Droplist contains: Todd
EXPECTED: error
OBSERVED: as expected error message:
'ERROR: both droplist and allowlist found in target directory'
`PASS`
**same name droplist**
same error message
`PASS`
**empty droplist**
same error message
`PASS`

**now test with empty droplist only (no allowlist) just to check not different behaviour**

Originals contains: Cunningham
Updates contains: Cunningham
Droplist empty
EXPECTED: finals to contain Cunningham, address from updates.
OBSERVED: as expected
`PASS`

Originals contains: Cunningham
Updates empty
Droplist empty
EXPECTED: finals to contain Cunningham, address from originals.
OBSERVED: as expected
`PASS`

Originals empty
Updates contains: Cunningham
Droplist empty
EXPECTED: finals to contain Cunningham, address from updates.
OBSERVED: as expected
`PASS`

`**BUG**`
Program handles empty droplist but crashes on empty allowlist.


7. **Example 7 - All files from updates only**

- Originals folder is empty
- Updates has multiple files
*Expected: All updates files in finals*

(forgot to add address to name Todd in updates file) Error message:
ERROR: document " Todd " doesn't contain an appropriately formatted address
Shows 'appropriately formatted' error as expected

OBSERVED: as expected
`PASS`


## Priority 3: Edge Cases (IF TIME PERMITS)

8. **Example 8 - Different first names, same surname**

- eg originals/Smith: "John Smith..."
- eg updates/Smith: "Sarah Smith..."
*Expected: Does it care about first names or just match on surname?*


In originals: John Smith
In updates: Sarah Smith
In allowlist: Smith
EXPECTED: Sarah Smith from updates in finals
OBSERVED: as expected 
`BUT`
If that Smith from allowlist was supposed to be the John Smith, then that should be in finals, as well as the updates-only Sarah Smith.
`**BUG**`

**changed allowlist to droplist and observed same as above**

`**BUG**`
Tried to add the other Smith to updates (a different person) but won't allow me to add filename that's the same as existing.
Dataset can't have multiple people with same surname by following this filename naming convention.
screenshot1.png

**trying now: changing surname in one of the files (ie doesn't match filename) - expected to take only filename**

John Smith in both originals and updates with the update file (incorrectly) named Jones.
OBSERVED: Updates John Smith (under Jones) ends up in finals with filename Jones as expected. Program takes only filename, not name in body of data.

**changing back to the two Smiths with different first names, one in each folder, and adding two Smiths to allowlist**
EXPECTED: both Smiths in finals.
OBSERVED: only updates Smith in finals.

**changed allowlist to include 'John Smith' ie full name of originals Smith.**
OBSERVED: Only updates Smith in finals. Does not recognise full name. I imagine allowlist data has to match filenames exactly.

**changed filename to John Smith to match**
Now it puts John Smith through to finals as well as Sarah Smith (as Smith) from Updates. But as JohnSmith (no space) as file name. Contents intact.
screenshot2.png

**combo of full and surnames on droplist**

In originals: John Smith, Smith
In updates: Carter
In droplist: Smith, John Smith
EXPECTED: Carter in finals
OBSERVED: as expected 


9. **Example 9 - Case sensitivity test**

- File named "<Name>" in originals (uppercase, standard)
- Allowlist contains "<name>" (lowercase)
*Expected: Does it match?*

File named John in originals, john in allowlist. Not in finals.

10. **Example 10 - surname edge cases**
- Surnames like "O'Leary" or "Smith-Jones"
- Extra Whitespace in file matches with surname file name?
OBSERVED: File names in final omit the special characters.
screenshot3.png

`**BUG**`

## Automation with first and surnames

1. **TEST: Full name with space in allowlist**

Created: test_fullname_allowlist/originals/John Smith
Allowlist contains: 'John Smith'
Run: python document_updater.py test_fullname_allowlist
EXPECTED: File 'John Smith' in finals
`FAIL`
`**BUG**`
appears as JohnSmith in finals

2. **TEST: Full name in updates**

Created: test_fullname_updates/updates/Sarah Jones
Droplist contains: 'Sarah Jones'
Run: python document_updater.py test_fullname_updates
EXPECTED: File 'Sarah Jones' in finals (droplist irrelevant)
`FAIL`
`**BUG**`
appears as SarahJones in finals

3. **TEST: Full name in BOTH folders**
Created: test_fullname_both/originals/Emma Brown
Created: test_fullname_both/updates/Emma Brown
Allowlist contains: 'Emma Brown'
Run: python document_updater.py test_fullname_both
EXPECTED: Updates version of 'Emma Brown' in finals
`FAIL`
`**BUG**`
appears as EmmaBrown in finals

4. **TEST: Mixed surname-only and full names**
Created originals/Knight (surname only format)
Created: test_mixed_formats/updates/James Wilson
Allowlist contains: 'Knight' and 'James Wilson'
Run: python document_updater.py test_mixed_formats
EXPECTED: Both files in finals
`FAIL`
`**BUG**`
Knight, JamesWilson in finals


5. **TEST: Format mismatch - filename vs allowlist**
Created: test_mismatch_format/originals/Oliver Taylor
Filename: 'Oliver Taylor'
Allowlist contains: 'Taylor'
Run: python document_updater.py test_mismatch_format
EXPECTED: ???
OBSERVED: Allowlist has to match filename in full.



