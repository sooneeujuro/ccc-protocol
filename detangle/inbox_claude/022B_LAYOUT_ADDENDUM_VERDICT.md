VERDICT: ok

# Addendum to TASK 022 - figure output layout

I saw the local plan update that makes B/remap the operator-selected direction and adds per-paper physical extraction folders.

Recommendation:

- Yes to per-paper extraction workspaces: `G:\fig_rebuild_v20260616\<pid>\`.
- For final corpus placement, prefer option (i): flat `articles/` with a pid-prefixed basename.
- Do not choose option (ii) subfolders unless flat placement fails, because changing `read_paper.py` and `fig_render_audit.py` adds avoidable code risk during a corpus-repair run.

Preferred target name shape:

```text
articles/<pid>__refill20260616_figNN__<image_sha12>.jpg
```

This keeps existing basename-oriented tools working, prevents cross-paper collision through the pid prefix, makes the refill provenance visible, and avoids silent overwrite if extraction changes.

Minimum guards before batch:

- Stage extracted images and patched markdown first; do not patch the only live copy directly.
- Produce a per-paper manifest with source PDF SHA-256, page, extracted image SHA-256, target basename, old markdown ref, new markdown ref, and confidence.
- Run one small pilot plus Seton 2012 stress pilot if time allows.
- Use contact sheets for visual sign-off.
- Run `fig_render_audit.py` after promotion.

So: per-paper physical extraction = yes; final `articles/<pid>__...jpg` flat placement = yes; final `articles/<pid>/figNN.jpg` subfolders = defer unless needed.
