# Video Clips Directory 🎥

**No video is distributed with this repository.** This directory is intentionally
empty apart from this file. Everything in it is gitignored, and nothing in
`.gitignore` should ever be changed to re-track it.

During the hackathon the clips were committed so that footage could be moved
between teammates and the DGX Spark. That is no longer how they are shared, and
committed video is the reason the repository grew to 1.5 GB. Keep clips outside
Git.

### To run anything here

Drop your own `.mp4` / `.mov` files into this directory and point the CLI at
them:

```bash
python3 -m src.main --video data/video_clips/<your-clip>.mp4 --stream
```

The pipeline does not care what the file is called. `data/scenarios.json`
references `scenario_1.mp4` and `scenario_2.mp4` by name, so use those filenames
if you want the named scenarios to resolve.

### What the demo clips were

Simulated emergency and traffic camera feeds — a multi-vehicle crash with a
commercial chemical tanker breach, a highway rollover with a fuel spill, and
several road-incident samples. They are not included here and are not
redistributed.
