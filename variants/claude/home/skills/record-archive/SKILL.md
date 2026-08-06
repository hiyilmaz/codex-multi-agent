---
name: record-archive
description: Check and compact project governance records only on declared archive events.
---

# Record Archive

Run a read-only archive check when a deferred finding completes, an experiment
becomes terminal, a new changelog date is created, or the user requests it.
Apply compaction only when the current task owns the relevant record changes.
Preserve full records without loss, duplication, or summarization.
