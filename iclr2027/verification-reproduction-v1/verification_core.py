"""Original report matcher, copied verbatim from the source-bound audit."""

def report_matches(report,iid,resolved):
    # Related-Lite's pinned harness writes a single-task object, not SWE-bench's iid mapping.
    return (report.get('instance_id')==iid and isinstance(resolved,bool)
            and report.get('resolved') is resolved
            and (resolved is False or report.get('patch_applied') is True))
