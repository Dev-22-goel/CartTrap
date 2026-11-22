# Codex G3 status — dataset tables

Implemented the approved plan v3 tables:

- `eval/genprops/product_types.json`: 30 ordered product types with concise natural search queries.
- `eval/genprops/variants.json`: 150 unique type/variant rows, with modality totals image 40, video 40, audio 40, text 10, none 20. Video flags total 70; the frozen set has 50 rows (9 image, 9 video, 9 audio, 3 text, and all 20 clean controls).
- `tests/test_genprops_tables.py`: checks type order and fields, variant schema and IDs, modality matrix and totals, frozen stratification, both reference modes per modality, and balanced hijacks.

Verification command:

```text
.venv\Scripts\python -m pytest -q -p no:cacheprovider --basetemp=.pytest_tmp_G3
```

Output:

```text
322 passed, 11 deselected in 5.45s
```

No Git commands or network access used.
