# Executable policy sketches

`authorization.py` illustrates object-level and administrative authorization. `Session` stands in for identity and permissions established by trusted authentication middleware; do not populate it from untrusted role fields.

The customer API can retrieve an order and change its delivery address before dispatch. Both use the same ownership guard. Editing accepts only `delivery_address`, rejects blank/invalid values, and rejects changes after processing. Caller-supplied owner, role and status fields are not editable.

Run `bash test.sh` from the repository root. The 12 authorization tests cover legitimate reads and edits, cross-customer rejection with unchanged state, missing orders, dispatched orders, invalid/injected fields, and administrative permission. Mutation checks remove the ownership guard and demonstrate that both cross-user read and write tests catch it; a separate mutation checks the admin guard.

This is an in-memory policy sketch with no HTTP, authentication middleware, database transactions or deployment. A production implementation must make the dispatch-status condition and write atomic, maintain consistent policies across endpoints and validate addresses according to its business rules. The example length/nonblank validation does not verify deliverability. Passing these tests does not prove a complete application secure.

`matrix.html` is the optional interactive dominance explorer. The main talk uses a single Python baseline run.
