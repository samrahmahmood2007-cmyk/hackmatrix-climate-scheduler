# Initial packet — start here — Sustainability & Climate Tech

Challenge version: 2026-11-04.v2
This initial packet contains your problem brief, starter, local checker and
public practice data. Read BRIEF.md and OBSERVATIONS.md, then your domain
API/schema documentation. Follow the saved event schedule in the portal.
The starter files to include when packaging the supplied solution are:
- solution.py

Use local_check.py and the practice/training data during development.
Build a separate submission ZIP containing your solution and its required
helpers/parameters; do not upload this whole initial packet.
Resources → Download sample submission ZIP provides the starter in the
accepted layout. It is a modest baseline, not a reference answer or a
promise of eligibility or a high score.

## Schedule flexible work when energy is cleaner and cheaper

A site has jobs that can be spread across the day, but each job has a deadline and the site can do only so much work at once. Electricity prices and the carbon intensity of the grid vary. Waiting for a better time can save cost, but waiting too long can leave work unfinished.

### What to build

Build a Python scheduler that decides how many units of each available job to run every half hour. Respect capacity and deadlines, use the known tariffs and imperfect carbon forecasts, and update decisions as new jobs and measurements arrive.

### How you do well

Complete the work while reducing the published combined electricity and carbon cost. Balance forecast uncertainty against deadline pressure. Deadline rules, forecasting and rolling optimisation are all possible approaches; future measurements and unreleased jobs are hidden.

### What you receive

You receive historical carbon estimates combined with a simulated workload, tariffs and forecasts, plus a starter and public replay checker. The score measures performance in this simulation, not verified real-world emissions savings. No energy API or model account is required.


## What to upload

Edit solution.py and include every helper and parameter file it imports or reads.
Keep the files directly at the ZIP root, not inside a folder. Remove __MACOSX,
.DS_Store, virtual environments and caches. README.md is optional.
Allowed extensions: .py, .json, .txt, .md. Maximum 100 files, 2 MiB per file,
16 MiB uncompressed total, 32 MiB uploaded ZIP. No links or subfolders.
Do not upload datasets, prediction CSVs, notebooks, pickle/joblib files or API keys.

## Execution contract

solution.py must expose decide(observation, state), returning exactly an action
dictionary and a state dictionary. Follow your domain's starter and observation
contract for the action fields. The platform imports this module and calls the
function; it does not simply run an arbitrary script from beginning to end.
State is JSON-compatible and resets for each case. Cleaning and feature
engineering needed at inference belong in your executable solution.

Code runs with 2 CPUs, 2 GiB memory, no direct network,
read-only /submission and /public, and temporary writable /tmp. Read your own
files relative to __file__; the working directory is /tmp. Released public data
is available under /public. The platform supplies evaluation observations;
private labels and grading logic are not mounted in your environment.
There is a 120-second response limit, 1200-second run limit and 1 MiB JSON frame
limit. Training is not automatically inferred from your files: load supported
saved parameters or explicitly implement permitted fitting within those limits.

## Required grading environment

Python 3.12.14. Your submitted Python code must use only the packages and versions listed here, the Python standard library, the supplied helpers and your own helper code. Do not bundle other third-party libraries or depend on additional packages. The grader does not install or upgrade dependencies; requirements.txt does not install anything.

| Package | Required version |
| --- | --- |
| numpy | 2.3.4 |
| pandas | 2.3.3 |
| scipy | 1.18.1 |
| scikit-learn | 1.7.2 |
| joblib | 1.6.0 |
| cloudpickle | 3.1.2 |
| python-dateutil | 3.0.0 |
| pytz | 2026.6 |
| tzdata | 2026.6 |
| six | 1.17.0 |
| threadpoolctl | 3.7.0 |

Import scikit-learn as sklearn and python-dateutil as dateutil. pip 25.0.1 is
present as image tooling; package installation during grading is not supported.
Use these versions locally to check compatibility. A missing package or an
incompatible import can fail execution even after the ZIP format is accepted.
Run a public practice submission early; practice uploads count against your
published practice limit. Available libraries do not change the allowed ZIP
formats: pickle/joblib model files are still not accepted.

Agentic AI: this restriction applies to the controller uploaded to the portal. Your separately hosted model gateway may use its own provider SDKs and frameworks. Your team supplies and pays for that hosting and model access; keep gateway code and provider keys outside the submission ZIP.


## After upload

Format accepted means the server checked the archive structure, allowed files,
size limits and presence of solution.py and saved a receipt. It does not prove
Python syntax, imports, dependencies, function behavior or task correctness.
Execution, eligibility and score are reported separately after grading.
An automatic quick compatibility check runs separately: imports and one decide
call on one public input, targeting feedback within 30–60 seconds after acceptance
when workers are available. Busy queues and infrastructure can delay feedback.
This check uses 1 CPU, 2 GiB and a 30-second execution limit. A timeout is
inconclusive and does not affect eligibility or marks. Passing confirms the
action/state JSON interface on that input, not correctness or a complete episode.
For Agentic, it does not call the model gateway. Full grading tests the full
controller and gateway separately, after compatibility checking resolves.
Your upload reserves one attempt while checked. A confirmed compatibility failure
uses no official or practice attempt, skips full grading, and lets you fix your ZIP
and start a new request while submissions are open. A passed check counts normally.
A quick-check timeout is inconclusive; after timeout or exhausted service retries,
full grading proceeds and the attempt counts. Failures during full grading count.
A format rejection creates no accepted receipt and uses no accepted attempt.
For a corrected ZIP, start a new upload request; retry an interrupted transfer
with the identical ZIP and saved request ID.

Each stage allows four official and four practice uploads, one evaluation
outstanding at a time. Initial validation contributes 20, post-twist validation
30, and private final testing 50. Final testing runs the selected frozen source
automatically after cutoff, with no new final upload. Final standings become
visible after your domain's evaluations finish; further submissions remain closed.
