1: **Example 1 - Droplist blocks originals**

Using surname: Anderson
Created: test_example_1_droplist_blocks_originals/originals/Anderson
Created droplist containing: Anderson
EXPECTED: Anderson should NOT appear in finals
Run with: python document_updater.py test_example_1_droplist_blocks_originals

OBSERVED: Originals contains Parry, Anderson. No Updates. Droplist contains Anderson. Finals contains Parry (address as expected from originals).
`PASS`


2: **Example 2 - Updates supersedes allowlist**

Using surname: Richardson
Created: test_example_2_updates_wins/originals/Richardson
Created: test_example_2_updates_wins/updates/Richardson
Created allowlist containing: Richardson
EXPECTED: Richardson from UPDATES folder in finals (not originals version)
Run with: python document_updater.py test_example_2_updates_wins

OBSERVED: Originals contains Owen, Richardson. Updates contains Owen, Richardson (different addresses as expected). Allowlist contains Richardson. Finals contains Owen (address from updates), Richardson (address as expected from updates). 
`PASS`


3: **Example 3 - Droplist irrelevant for updates-only files**

Using surname: Owen
Created: test_example_3_droplist_irrelevant/updates/Owen
Created droplist containing: Owen
EXPECTED: Owen from updates SHOULD appear in finals (droplist has no effect)
Run with: python document_updater.py test_example_3_droplist_irrelevant

OBSERVED: No Originals. Updates contains Jones, Owen. Droplist contains Owen. Finals contains Jones, Owen (addresses as expected from Updates.) 
`PASS`


4: **Example 4 - Droplist doesn't mention file**

Using surnames: Bennett and Hardy
Created: test_example_4_droplist_nomatch/originals/Bennett
Created droplist containing: Hardy (NOT Bennett)
EXPECTED: Bennett SHOULD appear in finals (not blocked by droplist)
Run with: python document_updater.py test_example_4_droplist_nomatch

OBSERVED: Originals contains Bennett, Smith. No Updates. Droplist contains Hardy. Finals contains Bennett, Smith (addresses as expected from Originals.)
`PASS`



## (Priority 2.1)

5: **Example 5 - Multiple files - mixed scenario**

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


6: **Empty list files** 
- Allowlist exists but is empty
- OR droplist exists but is empty
*Expected: How does program handle this?*


Originals contains: Cunningham
Updates empty.
Allowlist empty.
Finals contains 