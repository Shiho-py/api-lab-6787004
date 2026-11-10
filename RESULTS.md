# API lab results

## Run information

- Date: 10 November 2026 (Asia/Bangkok).
- Target: https://quickpizza.grafana.com.
- Environment: Windows, Python 3.15.0, pytest 9.2.0, requests 2.34.2,
  pytest-html 4.2.0, curl 8.21.0.
- Scope: Part 0, Steps 0.1–0.16, including the optional Step 0.12 experiment.
- Final command:

  ```powershell
  .\.venv\Scripts\python.exe -m pytest -v -rx --html=report.html --self-contained-html
  ```

- Final result: **16 passed, 1 xfailed in 19.18 seconds**, exit code 0.
- HTML report: [report.html](report.html). Its embedded results were checked:
  17 cases, comprising 16 Passed and 1 XFailed. Opening the local file with
  the browser tool was blocked by its URL policy, so visual inspection of the
  report remains pending. Open it locally in a browser to review the layout.
- No commit or push was performed during this Part 0 task.

## Part 0

### Steps 0.1–0.5: curl and Python requests

| Step | Observed result |
| --- | --- |
| 0.1 | `GET /api/names`: 18 pizza names; the first is `Americana`, and the list includes `Margherita`. |
| 0.2 | HTTP/1.1 200 OK, `Content-Type: application/json`, and `Set-Cookie` headers for `AWSALB` and `AWSALBCORS`. The observed HTTP version differs from the example's HTTP/2; the request succeeds. |
| 0.3, no token | `GET /api/tools`: 401 Unauthorized and `{"error":"authentication failed"}`. |
| 0.3, public practice token | 200 and `{"tools":["Knife","Pizza cutter","Scissors"]}`. |
| 0.4 | `POST /api/pizza` with `veg.json`: 200, pizza named `The Soft Siciliana`, and every ingredient marked vegetarian. |
| 0.5 | Repeated the names/tools/vegetarian requests using Python requests: all returned 200. Parsed names as a Python `dict`, counted 18 names, and read `application/json`. The Python pizza was named `A Tender Funghi`. |

Pizza recommendations are random, so names may change on later requests.
The public token in `auth.txt` was used only to read tools or request pizza
recommendations, never to create, change or delete ratings.

### Steps 0.6–0.8: first tests and deliberate failure

- The initial `Margherita` test passed: **1 passed**.
- Changed the expected name to `Pineapple Supreme` and ran the test:
  **1 failed**, with an AssertionError because the name was absent.
- Restored `Margherita`. The restored names test, tools test, vegetarian test,
  request-without-token test and new-user test passed together: **5 passed**.
- Final pizza tests check the response fields and every ingredient's
  `vegetarian` value, as well as the exact 401 error for a missing token.

### Steps 0.9–0.11: sessions, users and fixtures

- Created the made-up user `lab-51f3e06f6d0e`: 201.
- Logged in through the same `requests.Session`: 200.
- Read that user's ratings: 200 and `{"ratings":[]}`.
- The session retained the `AWSALB` and `AWSALBCORS` cookies.
- `api` is a session-scoped fixture. `auth` creates and logs in a fresh user
  for each test that requests it, using `log_in_new_user(api)`.
- This preserves the load balancer cookies across registration and login.
  Each authenticated test gets its own identity and rating data.

### Step 0.12: three runs without a session (optional)

Ran `pytest -v test_no_session.py --tb=short` three times:

| Run | Result | Observation |
| --- | --- | --- |
| 1 | 1 passed | Registration returned 201; login returned 200. |
| 2 | 1 failed | Registration returned 201; login returned 401 instead of 200. |
| 3 | 1 failed | Registration returned 201; login returned 401 instead of 200. |

The same code passed once and failed twice. This is consistent with the
handout's explanation that requests without retained load balancer cookies
may reach a different server. These three runs do not establish a general
failure rate or independently identify the server that handled each request.
Removed `test_no_session.py` after the experiment so the flaky test is not
part of the final suite.

### Steps 0.13–0.15: ratings and refused requests

| Test | Checked behavior | Final result |
| --- | --- | --- |
| Create rating | 201, matching stars and pizza ID, integer rating ID | Passed |
| Read rating | 200 and all saved fields match | Passed |
| Update rating | 200 and updated stars equal 4 | Passed |
| Delete rating | DELETE returns 204, then GET returns 404 | Passed |
| Duplicate username | 400 and `{"error":"username already taken"}` | Passed |
| Wrong password | 401 and `{"error":"authentication failed"}` | Passed |
| Empty username | 400 and `{"error":"username field is empty"}` | Passed |

Also ran `pytest -v test_ratings.py::test_delete_rating --tb=short` alone:
**1 passed in 2.70 seconds**. It does not require an earlier test to run.

Rating creation and fixtures remove only ratings created with their own
test user's token. The API returns 400 with `rating ID <id> not found` when
cleanup deletes an already deleted rating. Cleanup accepts only that exact
missing-rating response or a successful 204; it does not ignore arbitrary
errors. The first standalone run exposed this cleanup assumption; after
correcting it, the standalone test and the complete suite passed.

### Step 0.16: excluded-tool input blocks

Characteristic: **how many of the three tools are excluded**.

| Block | Representative input (`excludedTools`) | Test | Observed result |
| --- | --- | --- | --- |
| 0 excluded | `[]` | `test_excluded_tool_is_not_used[excluded2]` | 200; returned tool is allowed |
| 1 excluded | `["Knife"]` and `["Scissors"]` | `test_excluded_tool_is_not_used[excluded0]`, `[excluded1]` | 200; returned tool is not excluded |
| 2 excluded | `["Knife", "Scissors"]` | `test_excluded_tool_is_not_used[excluded3]` | 200; returned tool is `Pizza cutter` |
| 3 excluded | `["Knife", "Pizza cutter", "Scissors"]` | `test_excluding_all_tools_is_refused` | 500 with an empty body; expected failure |

The original two inputs covered only the one-excluded block. The initial
suite passed **14 tests**. Adding the missing blocks produced **4 passed,
1 failed** in the excluded-tool file, with the three-excluded input returning
500. Moved that input into a separate test expecting 400 and a non-empty
JSON error message. It failed with `assert 500 == 400`, confirming the
requirements mismatch before adding the xfail mark.

The defect test uses `xfail(strict=True, raises=AssertionError)` with the
reason below. The correct 400/JSON assertions remain in the test. If the API
is fixed, strict XPASS makes the run fail so the mark can be removed. A
network exception is not accepted as this expected assertion failure.

## Defect report

- **ID:** Defect 1.
- **Title:** Excluding all available tools returns an internal server error
  with an empty body instead of a validation error.
- **Precondition:** QuickPizza is reachable; send a valid authentication
  header. pytest reproduced this using a newly registered user's token;
  curl independently reproduced it using the public recommendation token.
- **Request:** `POST https://quickpizza.grafana.com/api/pizza` with body
  `{"excludedTools":["Knife","Pizza cutter","Scissors"]}`.
- **Expected result:** HTTP 400 and a JSON error message explaining that no
  pizza can satisfy the restrictions, as specified by the product owner.
  The handout does not prescribe the exact message text.
- **Actual result:** HTTP 500 Internal Server Error, `Content-Length: 0`,
  and an empty response body (0 bytes).
- **curl confirmation:** 10 November 2026, 23:14:28 Asia/Bangkok
  (response Date: `Tue, 10 Nov 2026 16:14:28 GMT`).
- **Severity:** Medium. A validly authenticated, unsatisfiable restriction
  causes a server error and gives the client no actionable explanation.
  Other tested restrictions still work; no wider outage or data loss was
  observed.
- **Status:** Reproduced; retained as a strict expected failure. This task
  tests an external demo API and does not change its server implementation.

Reproduce in PowerShell from the repository folder:

```powershell
curl.exe -i -H "@auth.txt" -d "@excluded-all.json" https://quickpizza.grafana.com/api/pizza
```

## Evidence

`report.html` contains the final per-test results and expected failure.
Raw exploratory responses and intermediate test logs are in the ignored
`tmp/part0/` directory, including the curl headers, Python walkthrough,
three no-session logs, deliberate assertion failure, isolated delete test,
defect reproduction and final pytest output. No private user token was
written to these evidence files.

## Part A

Not started in this task.

## Part B

Not started in this task.
