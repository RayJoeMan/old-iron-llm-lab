# Fleet Dashboard (R25-D) — Build Report

**Status: LIVE — Opus check closed at PASS WITH FIXES, all required fixes landed and verified; one open owner condition (S10, below).**
**Built/verified:** 2026-11-13 (finished ~13:25 CT)
**Spec:** `SPEC.md` in this folder.

## Live URL

**http://100.103.255.114:8642** — Fortress tailnet address only. The server binds
exclusively to the tailnet IP (binds are validated against the Tailscale ranges
100.64.0.0/10 and fd7a:115c:a1e0::/48; anything else is a fatal startup error) and
enforces a Host allowlist (tailnet IP + `fortress.tail0de6a2.ts.net`; other Host
headers get 403). Not reachable from the LAN or the public internet. Verified
live from off-box through the tailnet on 2026-11-13.

## Architecture as deployed

Three tiers, all read-only, no component can write to any record file:

1. **Producer** (this VM, `~/workspace/fleet-dashboard/producer/producer.py`,
   plain nohup process via `run-producer.sh`, PID in `producer.pid`, log in
   `producer.log`). Every 60 s it:
   - SSH-probes the Mint (one batched remote command: host/uptime/load/mem/disk,
     `nvidia-smi`, Ollama service state, `/api/ps`, `/api/tags`, top processes —
     process listing is `comm`-only on both machines, never argv);
   - parses the record files from VM-side copies: Mint `QUEUE.md`, `TUNING.md`,
     `mint-queue-log.md`; Fortress `FORTRESS-QUEUE.md`, `FORTRESS-TUNING.md`;
   - builds `digest.json` (including per-source `sources` = {mtime, ok, error})
     and pushes it to Fortress `~/fleet-dashboard/state/digest.json` with an
     atomic rename — primary route direct over the tailnet, fallback via the
     Mint direct-link jump (`ssh_fortress_fallback.conf`, host `fortressdirect`).
2. **Collector** (Fortress **user** service `fleet-collector.service`, 30 s
   cycle, `~/fleet-dashboard/collector.py`). Probes Fortress itself:
   `nvidia-smi` by PCI bus (expected buses 05:00.0 / 06:00.0 / 41:00.0 render as
   MISSING rows if absent), systemctl service states, Ollama `/api/ps` +
   `/api/tags`, Tailscale peers, disk, top processes → `state/fortress.json`
   plus a capped `probe-events.jsonl`. A fatal collector error writes nothing —
   the last good file ages into STALE rather than a failure being stamped fresh.
3. **Web** (Fortress **user** service `fleet-web.service`,
   `~/fleet-dashboard/app/server.py` + `index.html`). Serves the page at `/` and
   merged state at `/api/state` (fortress.json + digest.json +
   server-stamped `digest_received_at` + merged probe events). Read-only:
   every non-GET/HEAD request and every unknown path returns 404. Security
   headers set (nosniff, X-Frame-Options DENY, Referrer-Policy, CSP — the CSP
   keeps `'unsafe-inline'` for the single-file inline script/style; disclosed
   residual, accepted in review). Handler timeout 10 s. The Dockerfile in
   `app/` was **not** used: the unit file records why — Docker bridge
   forwarding on Fortress is impaired; the host user-service is the deployed
   route. Both units are enabled with linger=yes, so the dashboard survives
   reboots and logouts.

The page auto-refreshes (10 s fetch timeout with a sequence guard against
out-of-order responses) and renders three machine cards (Fortress, Mint, VM)
plus panels: Mint Queue, Recent Verdicts (Mint TUNING + Fortress record,
tracked independently), Fortress Queue, Queue Session Log, Probe Events.

**Freshness model (the honest-state core):** every surface distinguishes
*read freshness* (when the reading arrived — Fortress clock for digest data via
`digest_received_at`) from *record age* (when the source file last changed,
informational only, never badged). Past the stale bound (120 s Fortress, 180 s
digest/Mint) a surface renders STALE; unread fields render as `—`/“unread”,
never as plausible-looking zeros. Unknown age renders “STALE — AGE UNKNOWN”.

## Data sources wired

- Fortress live probe (collector): GPUs by bus, services, Ollama resident
  models + model list, Tailscale peers, disks, top processes.
- Mint live probe (producer SSH): same shape, incl. GTX 960M at bus 01:00.0.
- Mint `QUEUE.md` (queue panel + session log from `mint-queue-log.md`).
- Mint `TUNING.md` → recent verdicts + `mint_backlog` source key.
- Fortress `FORTRESS-QUEUE.md` (queue panel), `FORTRESS-TUNING.md` (verdicts).
- VM self-probe (hostname, load, root disk).

Known v1 gap, stated plainly: the digest carries `mint_backlog_next` (parsed
TUNING backlog) but no panel renders it yet — data wired, display not built.

## Verification performed (2026-11-13, first-hand)

- Live fetches of `/` and `/api/state` through the tailnet: real data for all
  three machines, correct GPUs on both, verdicts matching the record files
  read directly (#283 PROPOSED, #282/#281 BAR NOT MET, #280 UNKNOWN,
  #279 BAR MET, #278 CERTIFIED; F-64…F-59 CERTIFIED).
- **Drill 1 — collector stopped:** `fortress.json` froze; at 151 s age vs the
  120 s bound the Fortress card rendered STALE; restart recovered fresh.
- **Drill 2 — producer killed:** digest receive age reached 266 s vs the 180 s
  bound → Mint card + all record panels STALE, while the Fortress card stayed
  fresh at 9 s (tiers fail independently). Producer restarted, recovered.
- **Drill 3 — Mint unreachable** (drill driver pointed the probe at a dead
  address after one good cycle): the Mint reading was carried with its
  ORIGINAL timestamp, `ok=false`, `carried=true`, failure reason attached;
  at 218 s vs the 180 s bound the Mint card rendered STALE while the digest
  kept arriving fresh (38 s) and Fortress stayed fresh (3 s). Recovery clean.
- Host-header check: bogus Host → 403; MagicDNS Host → 200.
- Fallback push route proven live end-to-end after hardening (below).

## Opus check (Joe's build pattern — Claude Opus 5.5 as checker)

Four rounds; full texts archived in this folder (`opus-review.md`,
`opus2-review.md`, `opus3-review.md`, `opus4-review.md`).

- **Round 1: FAIL** — 5 blockers (B1 process argv could leak credentials into
  state; B2 failure defaults rendered as real measurements; B3 failed probes
  stamped fresh, errors never displayed; B4 panel freshness aged from digest
  build time instead of source age; B5 GPU probe failure silently removed
  GPUs) + S1–S12, N1–N8. Verified clean even then: read-only surface,
  exact-match routing, DOM safety (all text via `textContent`), constant
  remote command string, JSON via `json.loads` only. All blockers fixed.
- **Round 2: FAIL — one blocker left.** B4 hole: a missing record file's error
  was discarded and the panel fell back to the fresh digest time; freshness
  still conflated record age with reading staleness; producer death hideable
  for up to 6 h. S5 (verdict matching) incomplete; new items S-new-1…4,
  N-new-1…3. All fixed: per-source errors independent of mtime; two-fact
  freshness (receive-time STALE badge + informational record age); verdict
  matcher rebuilt (below); Mint probe error accumulation + expected-GPU row;
  TOP header regression fixed; resident-model null vs [] distinguished;
  nvidia-smi stdout parsed on non-zero exit; write-failure events; disk pct
  null at total 0; per-column verdict-source errors.
- **Round 3: PASS WITH FIXES** — B4 verified closed; F1–F10 issued (Mint probe
  event claiming success on partial reads; carried-reading clock rule; the
  Fortress verdict parser able to show failures as green; S10 evidence gaps;
  segment selection by index; negation guard covering only PROPOSED; empty
  nvidia-smi output skipping the MISSING row; unguarded `probe_vm`; merged
  verdict-age header; backlog sharing the tuning source key). All ten landed.
- **Round 4 (final confirmation): PASS WITH FIXES** — F1–F10 all confirmed.
  One narrow required fix, **R1**: markdown emphasis / extra whitespace could
  defeat the negation guard (`NOT **CERTIFIED**` reading as CERTIFIED).
  Closed by the builder with test evidence (Opus's prescribed closure — no
  further full round): both parsers now normalize via `strip_md` before
  scanning (also extended to single-asterisk emphasis, which testing showed
  was a live false-green path), and the R1 synthetics return NOT CERTIFIED
  on both parsers with live-file outputs unchanged. One sub-case is
  dispositioned by rebuttal evidence: a `**` pair *inside* a Mint header's
  own bold span terminates the header capture itself, so the verdict word is
  never scanned and the entry fails **safe** to UNKNOWN (grey) — the
  false-green direction R1 exists to prevent cannot occur through that path.
  **S1** (client stamping a fresh age on no-data failures) also landed:
  read_at overrides now require an existing reading, and the VM card renders
  `probe_vm` errors visibly (the Mint/Fortress card already rendered ok=false
  with probe errors / last_error — confirmed in code for the reviewer).

**Verdict matching, as shipped:** Mint TUNING headers follow
`#N — date — <subject> — <DISPOSITION>: <read>`; the parser selects the
disposition segment by shape (first segment whose pre-colon head carries a
verdict token), bar phrases and negations dominate the filing label inside it
(`PROPOSED: BAR NOT MET` → BAR NOT MET), any positive-verdict match directly
preceded by NOT / NOT YET is discarded, and no match renders UNKNOWN — never
a default green/amber. The Fortress parser uses failure-first priority
(NOT-forms, FAILED, VOID, then CERTIFIED/COMPLETED/PROPOSED). Fitted to the
fleet's own header conventions and covered by a synthetic battery +
live-file runs (all passing, outputs in the round-4 prompt/response record).

### OPEN OWNER CONDITION — S10 (not closed by the builder)

Per the reviewer's prescription this stays an **open condition on the
verdict**, for Joe's decision:

- The fallback route's *configuration* is now fully evidenced and hardened:
  both hops (`mintjump`, `fortressdirect`) run BatchMode + IdentitiesOnly
  with pinned known-hosts files and StrictHostKeyChecking **yes** (the
  mintjump stanza was tightened from `ask` in this build and the route
  re-proven live).
- The residual is key policy: the producer authenticates with the fleet's
  standard agent key (`~/.ssh/id_ed25519`) — the same key used for all
  administration of both boxes, i.e. full shell on Mint + Fortress. A
  dedicated forced-command key restricted to the probe/push commands would
  be a fleet-wide key-policy change. **The deploy record states: the
  producer runs on the standard key pending the owner's acceptance.** If
  declined, this reopens as a required change: dedicated key, restricted
  via `authorized_keys` to the push/probe commands.

## Tandem-build ledger

The spec called for DeepSeek + Muse Spark tandem drafting with Opus
checking. Ledger honesty: **no per-lane attribution is recoverable from the
code or logs** — no authorship markers exist in the artifacts, so this report
does not attribute specific files or functions to a lane. What is on record:
the integrated codebase was completed and deployed by the owning agent; the
Opus check ran four rounds as above with every finding fixed or rebutted
with evidence.

## Round 4 — loaded models from both runtimes (2026-11-13)

**Joe's request:** the Fortress card must show loaded models from BOTH
runtimes, not just Ollama. Diagnosis (verified first-hand): the collector
sourced "loaded models" only from Ollama `/api/ps`, but the experiment
chains launch `llama-server` directly — so the card showed nothing loaded
while the box was mid-generation (Ollama `/api/ps` = `{"models": []}` was
accurate; llama.cpp was the blind spot).

**Collector (Fortress) — new `llama_servers` probe.** Scans
`/proc/<pid>/cmdline` for processes whose argv[0] basename contains
`llama-server` and extracts ONLY whitelisted fields via token parsing:
`{model (basename of -m/--model), port (--port), ngl (-ngl /
--n-gpu-layers / --gpu-layers), pid}`. Raw argv is never copied anywhere —
the same doctrine as the comm-only `top_processes` probe (unit-tested: an
argv containing `--api-key SECRET-VALUE-123` yields exactly the three
fields, the secret nowhere). Semantics match the other probes: success →
a list (an empty list is a TRUE empty — no servers), failure → `null` +
`probe_errors: ["llama_servers"]`, rest of the record intact.

**Ollama-runner exclusion (found during testing, load-bearing).** Ollama
itself spawns a `llama-server` child per loaded model whose `-m` is an
opaque blob hash (`sha256-…`). Without filtering, the Mint's only
llama-server — Ollama's runner for `qwen3:4b`, already reported via
`ollama_resident` — would have appeared as a bogus duplicate. Both probes
therefore skip llama-server processes whose parent comm is `ollama`;
only independently launched servers (the chains') are listed. Verified
live on Fortress: Ollama's `qwen3:4b` runner (ephemeral port) is excluded
while two chain servers (parent `python3`) are listed.

**Mint — SHIPPED (not Fortress-only).** The producer's batched SSH probe
appends a block that parses `/proc` ON the Mint and emits only
`pid|model-basename|port|ngl` per server — raw argv never crosses the
wire. A leading `ok` sentinel distinguishes a true empty from an unread
(the block ran and found none → `[]`; no sentinel → `null` + probe error).
At deploy time the Mint read `[]` — a true empty: its only llama-server
was Ollama's runner, correctly excluded. The field populates whenever the
Mint's standalone llama lane runs.

**Display.** The card section is now **Loaded Models**: Ollama-resident
entries tagged `OLLAMA` (name + VRAM, as before) and llama-server entries
tagged `LLAMA.CPP` with model basename + lane hint (`CPU` when ngl = 0,
`GPU · ngl N` when ngl > 0) + `:port`. Both runtimes unread → `— (unread)`;
readable-and-empty → `none loaded` (or `none loaded (one runtime unread)`
when only one side read). Round-2 layout/drag/expand and round-3 CPU
sections untouched.

**Deploy.** `collector/collector.py` + `app/index.html` copied to
Fortress; `fleet-collector` + `fleet-web` restarted; producer restarted
on the VM (server.py needed no change — state passes through). Experiment
lanes untouched: the running llama-servers (pids 131362, 134969 at deploy
time) were identical before and after the restarts.

**Verification (first-hand).**
- `/api/state` fingerprint: 131 → 136 key paths; ADDED is exactly
  `fortress.llama_servers[].{model,ngl,pid,port}` +
  `digest.mint.llama_servers[]`; REMOVED: none.
- First after-read: `fortress.llama_servers` =
  `[{llama3.2-3b.gguf, port 8500, ngl 0, pid 131362},
  {Qwen3.8-9B-Q4_K_M.gguf, port 8810, ngl 99, pid 134969}]` — matching a
  simultaneous `ps` read field-for-field; `fortress.ok = true`,
  `probe_errors = []`; `digest.mint.llama_servers = []`,
  `digest.mint.ok = true`.
- Live URL: `GET /` → 200 (on-box, tailnet).
- Screenshot `dashboard-r4-1920x1080.png` (this folder): Fortress card
  shows `OLLAMA qwen3:4b (5.3 GB VRAM)` + `LLAMA.CPP llama3.2-3b.gguf ·
  CPU · :8510` + `LLAMA.CPP llama3.2-3b.gguf · CPU · :8511`, cross-checked
  against the simultaneous `ps` (pids 141932/141933; Ollama `/api/ps` =
  `qwen3:4b`). Taken with headless Firefox on Fortress itself — the
  VM-side Playwright route failed this round (the venv's pinned Chromium
  build had been pruned from the browser cache and the fallback builds
  hit `ERR_EMPTY_RESPONSE` through the forward); a future round should
  re-provision the venv's browser or reuse the on-box route.

## Restart / update instructions

- **Web / collector (Fortress):** `systemctl --user restart fleet-web.service
  fleet-collector.service` (as `general`; reachable via
  `ssh -F /tmp/fortress_jump.conf fortress-link` or the tailnet recipe in
  `~/TOOLS.md`). Status: `systemctl --user status fleet-web fleet-collector`.
  State files: `~/fleet-dashboard/state/` on Fortress.
- **Producer (this VM):** stop `kill $(cat
  ~/workspace/fleet-dashboard/producer/producer.pid)`; start
  `nohup ~/workspace/fleet-dashboard/producer/run-producer.sh >/dev/null 2>&1 &`.
  Log: `producer/producer.log`.
- **Updating code:** edit in `~/workspace/fleet-dashboard/` (source of truth),
  then copy `app/index.html` / `app/server.py` / `collector/collector.py` to
  Fortress `~/fleet-dashboard/` (note: the collector deploys as
  `~/fleet-dashboard/collector.py`) and restart the matching unit; producer
  changes need only a producer restart on the VM.
- **Do not disturb:** the Ollama system service and the other dashboards
  (Netdata 19999, Uptime Kuma 3001, Open WebUI 8080) — the fleet units are
  independent user services.

## Round 5 — "Current Job" on every card + producer self-healing (2026-11-13, ~17:14–17:30 CT)

Joe's ask (~17:11 CT): each device card should say what the device is
currently working on. Mid-build he added the outage below (he had noticed
the Mint card looked stale/idle — it was: the producer was dead).

### New field: `jobs` on all three machine records

`jobs` = a list of `{"label", "detail"}` (detail null when there is none),
capped at 5, rendered as a "CURRENT JOB" section at the top of each card
(above Load). Honest-state semantics match the other probes: `jobs: null`
+ a `"jobs"` entry in `probe_errors` when the probe could not read the
box renders `— (unread)`; an empty list means the probe DID read the box
and found nothing, and renders `idle`.

- **Fortress (collector, new `probe_jobs`/`classify_jobs` over a `/proc`
  scan):** same whitelist doctrine as round 4's llama_servers probe —
  argv is used ONLY to extract a script path and the values of a few
  known flags; raw command lines never reach the state file (unit-tested
  with a planted `--api-key SECRET-VALUE-123`: neither value nor flag
  name appears in the output, and no absolute paths either). Rules,
  generic by directory/process convention rather than today's job names:
  `gpu_detect*.py` under a python interpreter → `YOLO detection` (detail:
  output-dir basename + `W###` from `--source`); `run_ab.py` →
  `Fleet Bus A/B` (detail from `--arm`/`--run`); a python script under
  `~/flane/<area>/` → the area's display name (`funnel` → Funnel,
  `r24w` → R24-W, `trials` → Model trial, `yolo` → YOLO, `rvision` →
  R-VISION, `rpool` → R-POOL, `chain` → Chain; an unmapped area shows
  its directory name) with the script stem as detail; anything under
  `~/fleet-bus-ab/` other than `run_ab.py` is an A/B worker and folds
  into the `run_ab` job; leftover direct-launched llama-servers group as
  `llama.cpp · <model>` (×N), with Ollama's own runner children excluded
  by the round-4 parent check. Two structural rules carry the design:
  (1) **ancestor suppression** — a process under an already-classified
  process is part of that job (a funnel driver owns its llama-servers;
  that is why the 16:32 "8 models on CPU" moment reads as one Funnel
  job, not nine); (2) **bash chain drivers are not jobs** — lane scripts
  and `yolo_lane.sh` are wrappers, so their python workers classify on
  their own; a live lane driver with NO classified worker descendant
  yields `Lane X chain · between steps` rather than silence. Gated
  annotation: when a job's owning lane log tail matches /gated|waiting/i,
  ` · gated` is appended to its detail — only the state word crosses
  over, never log text. (Freshness window is 6h: fw2's heartbeats land
  ~hourly; liveness of the job process itself is the real freshness
  proof. The first cut used 20 min and dropped the annotation on a live
  gated job — caught in live verification and fixed same-round.)
  Classifier unit tests: 16 synthetic-snapshot checks incl. the secret
  test, the funnel-owns-servers case, the A/B worker fold, the lane
  fallback, and empty-snapshot → `[]`.
- **Mint (producer):** the batched SSH probe gained a `REMOTE_MINT_JOBS`
  block in the round-4 LSV pattern — the box itself emits only
  `pid|script-path|cwd` rows for python processes (flag values never
  cross the wire; the script token AND the working directory are both
  needed because experiment drivers are often invoked by relative path).
  The leading `ok` sentinel proves the block ran, so an empty result is
  a true idle. Producer-side classifier (generic): a script path or cwd
  under `mint-experiments-*/e<NNN>/` (or a `run_e<NNN>.py` basename) →
  `Experiment E<NNN>`, deduped across driver + children; `gpu_detect*.py`
  → `YOLO detection`; everything else (verdict servers, desktop applets)
  is infrastructure, not a job. After classification, `build_digest`
  enriches an experiment's detail from the TUNING backlog text for that
  id when one exists (today E270 has no backlog line, so it renders
  bare). The daytime-queue drafting case needs no special rule: those
  workers run as python scripts and would need a Mint-side convention to
  name — none exists yet, so an unrecognized worker truthfully yields no
  entry rather than a guess; if the queue's driver gains a stable script
  path, add one classifier line.
- **VM (producer):** `probe_vm` has no honest source for scheduled-job
  names on this VM (no cron daemon, no systemd user bus, and the
  platform scheduler's state is not readable from inside the VM), so the
  card reports the one job the probe can prove by construction:
  `Fleet Dashboard producer · digest every 60 s` — probe_vm runs inside
  the digest cycle, so the producer is running whenever this record
  exists. Agent activity is deliberately NOT inferred.

### The producer outage (found by Joe, fixed this round)

- **Window:** last successful push 16:00:37 CT; producer found dead
  ~17:14 CT; pushes resumed 17:21 CT. ~74 minutes of stale Mint/VM data;
  the Fortress card stayed live throughout (collector self-probes), which
  is why only the Mint card looked wrong.
- **Cause (as evidenced):** a VM runtime restart at ~16:00–16:01 CT
  killed the bare `nohup` producer (pid 58434, started in an earlier
  round, nothing supervised it). The 16:01 cycle's log line shows both
  push routes failing mid-restart; the process never wrote again. The
  same restart killed another background job (the Firebase audit's first
  run). Debris: `digest.json.tmp.40476` (13:03) in the Fortress state
  dir — an interrupted one-off probe push from the morning, removed
  this round.
- **Hardening (three layers):** (1) `run-producer.sh` is now a
  SUPERVISOR — it runs producer.py in the foreground and restarts it on
  any exit after 5s (`producer.pid` now names the supervisor; the TERM
  trap kills the child, so the old stop recipe still works and never
  orphans a second producer). (2) New `ensure-producer.sh` (flock +
  pid/cmdline check) starts the supervisor iff it is not running.
  (3) Platform cron job **`fleet-producer-watchdog`** runs the ensure
  script every 10 minutes and stays silent unless the producer is still
  down afterwards — the platform scheduler lives outside the VM, so this
  layer survives VM restart/replacement; the VM itself has no cron
  daemon or systemd user bus to do the job locally.
- **Kill-tested live:** producer child killed → supervisor logged
  `exited (rc=143)` and relaunched it in 5s; supervisor killed → trap
  took the child with it, no orphan; ensure script → new supervisor +
  producer up and pushing within seconds. Post-restart pushes verified
  at 17:21, 17:22, 17:22, 17:24 CT (`digest.json` mtime advancing on
  Fortress, all `pushed via tailnet-direct`).

### Fingerprint + live verification

- `/api/state` key paths: **130 → 136; added exactly**
  `fortress.jobs[].label`, `fortress.jobs[].detail`,
  `digest.mint.jobs[].label`, `digest.mint.jobs[].detail`,
  `digest.vm.jobs[].label`, `digest.vm.jobs[].detail`; **removed: none.**
  (Round 4's report counted 136 with a different counter; this round's
  before/after were both taken with the same counter, and the delta is
  the contract.)
- Live-truth check at ~17:25 CT, card vs simultaneous ground truth:
  Fortress card `R24-W · fw2 · gated` + `Fleet Bus A/B · arm B · run 1` +
  `Lane A chain · between steps` vs `ps`: fw2.py (pid 165894) under
  lane_b.sh with lane_b.log's tail = the fw_2 gated heartbeat; run_ab.py
  `--arm B --run 1` (pid 193689); lane_a.log tail = `+ sleep 600`
  (filler gap — between steps is literal truth). Mint card `Experiment
  E270` vs `ps`: `run_e270.py` (pid 1171206) + its `mint_ask_local.py`
  child on qwen3:4b; card also showed CPU 52% + qwen3:4b resident, and
  the root disk at 21/228 GB (91%) — the post-prune numbers, i.e. the
  freshness Joe found missing is restored. VM card `Fleet Dashboard
  producer · digest every 60 s` vs the supervised producer verified
  pushing in the same minutes. `probe_errors` empty on all three.
- Screenshot `dashboard-r5-1920x1080.png` (this folder): all three cards
  show their CURRENT JOB sections with the values above. Taken with
  headless Firefox on Fortress; two route notes for future rounds —
  Firefox is the SNAP build: it cannot see the SSH session's /tmp, and
  the default profile is locked by the desktop's running Firefox, so use
  a throwaway profile AND the screenshot path under `$HOME`
  (`--profile $HOME/ff-r5-profile --screenshot=$HOME/dashboard-r5.png`),
  then scp it down.
- Restarts this round: `fleet-collector.service` + `fleet-web.service`
  (brief, verified active + fresh `fortress.json` after); the VM producer
  was restarted under its new supervisor as part of the outage fix. No
  chain, experiment, A/B, or backup work was touched; protected processes
  (lane_a.sh, lane_b.sh, fw2.py, run_all.sh/run_ab.py, Ollama, SwarmChat)
  all verified still running at their pre-round pids in the final check.
- Backups of the replaced on-box files: `~/fleet-dashboard/collector.py.bak-r4`
  and `~/fleet-dashboard/app/index.html.bak-r4` on Fortress.

### Restart / update instructions — CHANGED by this round

- **Producer (this VM):** it is supervised now. Normal state: supervisor
  `run-producer.sh` (pid in `producer.pid`) + platform cron
  `fleet-producer-watchdog` ensuring it every 10 min. Stop: `kill $(cat
  ~/workspace/fleet-dashboard/producer/producer.pid)` (the trap stops the
  producer child too) — and know the watchdog will relaunch it within
  ~10 min; disable the cron job first for a deliberate long stop. Start
  manually: `~/workspace/fleet-dashboard/producer/ensure-producer.sh`.
  Log: `producer/producer.log` (supervisor + ensure lines included).
