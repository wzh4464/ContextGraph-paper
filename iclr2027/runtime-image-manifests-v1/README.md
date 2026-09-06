# Frozen verifier image manifest reproduction

This package checks the original public-registry manifest bytes for the base
image and all 99 fixed Related-Lite task images. The original local image IDs
were observed with Docker 29.4.0's containerd image store and identify its
manifest/index targets, rather than being assumed to be configuration digests.
All requests used immutable digests and anonymous pull authorization; the token
was not saved. No tag substitution or benchmark outcome selection occurred.

Run without Docker, network access or third-party Python dependencies:

```bash
uv run --no-project python reproduce.py
```

The script checks all file hashes, all 188 raw manifest objects, the original
100-image identities, and all recorded configuration/layer descriptors.
There are 99 image-index roots with a selected linux/amd64 descriptor and
1 single-image root whose platform was not independently read from its config.
The 99 selected descriptors reference 88 distinct platform-manifest byte strings;
shared platform manifests account for the difference in these counts.
The descriptors identify 661 distinct configuration/layer objects with
31,571,851,536 declared compressed bytes. These payloads have NOT been downloaded
or verified by this package. It is not a full image archive or execution test.

The registry observation was completed on 2026-09-06 at 21:50 UTC. This snapshot
does not guarantee future registry availability. It also does not bind the
historical solver environment or every derived verifier-image parent link.
Original image references and upstream benchmark identities remain explicit.

To prepare an image later, use its exact digest and platform; for example:

```bash
docker pull --platform linux/amd64 jiayuanz3/swecontextbench@sha256:38dbaeb2a1825a731e80299b3e48a0cd50f7ed8a28720ef2833c452e53b48f07
```

`images.json` contains the full fixed inventory. Pulling images and running the
frozen harness remain separate from this offline metadata check. Existing
benchmark predictions and verdicts are unchanged. This is a local review draft,
not a published or complete anonymous execution release.
