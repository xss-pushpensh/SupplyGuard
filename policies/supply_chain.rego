package supplyguard

# Deny unpinned GitHub Actions
deny[msg] {
    input.type == "github_action"
    not startswith(input.ref, "sha256:")
    not regex.match("^[a-f0-9]{40}$", input.ref)
    msg := sprintf("Unpinned GitHub Action: %s@%s", [input.name, input.ref])
}

# Deny unsigned artifacts
deny[msg] {
    input.type == "artifact"
    input.signed == false
    msg := sprintf("Unsigned artifact: %s", [input.name])
}

# Deny packages not in allowlist
deny[msg] {
    input.type == "package"
    not input.allowlisted
    not input.internal
    msg := sprintf("Suspicious package: %s@%s", [input.name, input.version])
}
