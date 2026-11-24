# Releasing

README examples use `book000/ssh-over-wireguard@v1`. The `v1` tag follows the latest published compatible release; users receive updates when it moves. A GitHub Action runs directly from the repository at the selected ref, with no separate build artifact.

A maintainer with permission to run workflows and publish releases should:

1. Review and merge the changes to `master`, confirm required checks pass, and select a reviewed commit on `master`. Verify the action in a Linux GitHub Actions workflow with working WireGuard and SSH endpoints, including success and failure cleanup and restoration of the runner's original `net.ipv4.ip_forward` value.
2. Open **Actions → Release → Run workflow**, select the ref to release (default: `master`), and enter a new stable semantic version such as `v1.2.3`. The selected ref's commit must be on `master`. Use a new major version for breaking changes and do not reuse release-specific tags.
3. Check that the workflow succeeds and that the new release-specific tag and its floating major tag both resolve to the selected commit. Inspect the released `action.yml` to confirm the intended cleanup behavior is present. For a compatible `v1` release, the workflow updates `v1`; the README examples stay on `@v1`.

The workflow tests the selected commit with `python -m unittest discover -s tests`, creates the version tag and a GitHub Release with generated notes, then moves the corresponding major tag to that commit. It rejects invalid versions, commits outside `master`, and updates that would move the major tag backwards or across histories. Releases are serialized, and the major-tag update uses a lease to detect concurrent changes.

The workflow needs permission to create releases and update tags. Tag protection or immutable release settings may prevent a tag update; the existing `v1` tag is associated with a GitHub Release. If any step fails, inspect the run and remote tags before retrying: a version tag or release may already have been created even if the major tag was not updated. Do not overwrite a release-specific tag; resolve partial publication and any repository policy restrictions with maintainers before proceeding.

See GitHub's [action release guidance](https://docs.github.com/en/actions/how-tos/create-and-publish-actions/manage-custom-actions) and [immutable release guidance](https://docs.github.com/en/actions/how-tos/create-and-publish-actions/using-immutable-releases-and-tags-to-manage-your-actions-releases).
