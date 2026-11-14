# Shop threat register

Two stipulated access-control flaws. Controls are proposed for the fictional system; the code tests a small policy sketch.

## T1 · Customer reads or redirects another order

Alice obtains Bob’s order ID. Missing object-level authorization on GET exposes his order; missing authorization on PATCH lets her change his delivery address before dispatch and potentially redirect the parcel. Information disclosure and tampering are two consequences of the same authorization weakness. This is stipulated in the teaching scenario.

**C1 · Authorize reads and address changes**

Check trusted caller ownership for both GET and PATCH. Accept only delivery_address and only while the order is processing; reject writes once dispatch begins. TEST: Alice may read/update A-101 before dispatch, but cannot read or change B-202. A rejected write leaves all data unchanged. Removing the guard must break both cross-owner regression tests. Production must enforce status and write atomically. See tests/test_authorization.py.

## T2 · Customer invokes an admin operation

A normal customer calls an administrative backend operation directly and supplies role=admin in the body. If the operation relies on UI hiding or client role claims, it grants administrative access. Impact: unauthorized changes and access. Opening scenario assumes weak access control.

**C2 · Check trusted permissions per admin operation**

Validate identity and required permission at every privileged operation; use trusted server permissions, deny by default. TEST: a customer is denied even with role=admin; an authorized operator succeeds. Remove the guard and confirm the negative test fails. Network restriction and MFA are additional layers.
