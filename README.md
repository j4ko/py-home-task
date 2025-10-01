# Run the validation service with docker-compose

Follow these steps to build and run the validation service using Docker Compose. This will build the image defined by the `Dockerfile` and run the test suite inside a container.

1. Build and start the service with Docker Compose:

```bash
docker-compose up --build
```

2. The service runs `pytest -v` inside the container and prints test results to the container logs. To stop the service, press Ctrl+C or run:

```bash
docker-compose down
```

---

# Data Validation Solution (pytest)

## Overview

This solution uses Python and the `pytest` testing framework to perform a set of validations against a dataset located at `data/rt-feed-record`, which contains newline-delimited JSON (NDJSON) records.

The goal is to ensure integrity, completeness, and correct formatting of streaming analytics data.

## Validation Tests

The repository provides a single test file: `test_data_validation.py`, which implements three independent tests:

### 1. Unique Document Count (`test_count_unique_documents`)

- Purpose: Verify the total number of distinct documents in the data file.
- Process: The test reads the file line by line, extracts `RP_DOCUMENT_ID` from each JSON record and adds it to a `set` to ensure uniqueness. Finally, it asserts that the number of unique IDs is greater than zero and reports the count found.

### 2. Incomplete Analytics Detection (`test_find_documents_with_missing_analytics`)

- Purpose: Detect documents that have missing analytics parts.
- Process: The test groups records by `RP_DOCUMENT_ID`. For each document it compares the expected number of analytics (from the `DOCUMENT_RECORD_COUNT` field) with the actual ones found (by counting unique `DOCUMENT_RECORD_INDEX` values). If they don't match, the test fails and reports which documents are incomplete and which analytic indexes are missing.

### 3. RP_ENTITY_ID Format Validation (`test_rp_entity_id_format`)

- Purpose: Ensure the `RP_ENTITY_ID` field matches the expected format.
- Process: Based on prior analysis of the data, the expected format is a 6-character uppercase alphanumeric string. The test uses a regular expression (`^[A-Z0-9]{6}$`) to validate each `RP_ENTITY_ID` in the file. Any ID that doesn't match causes the test to fail and reports the invalid value and its line number.

## How to run the tests locally

From the project root directory, run:

```bash
python3 -m pytest -v
```

## Notes

- The repository contains a `Dockerfile` that installs `pytest` and copies the test and data into the container. The container runs the tests by default.
- The provided `docker-compose.yml` defines a single service named `rt-stream-validator` which builds the image using the included `Dockerfile`.

---

If you want, I can also run the tests inside the workspace and report the results, or help troubleshoot any failing tests.
