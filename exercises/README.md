# Take the shop further

Use copies of the fictional model and code. Each exercise asks for a changed path, an enforcement rule and a way to check it.

## 1. Follow a request and its response

Draw Alice reading her own order, then requesting Bob's. Label the caller-controlled identifier, trusted identity, authorization decision and returned data. State whether the two requests should have different outcomes and why.

**Check your answer:** authentication is shared, but permission for the object differs. Possession of Bob's identifier is not permission to retrieve his data.

## 2. Reject an address edit without changing anything

Read `update_delivery_address` and its tests. Compare an eligible edit, a cross-user edit and an edit after dispatch. Add an assertion that the entire stored order is unchanged after a rejected request if you write another negative case.

**Check your answer:** ownership, writable fields and order state are separate checks. An error response alone does not establish that the write was prevented.

## 3. Consider a dispatch race

Draw two concurrent operations: an address change and dispatch. Place a status read and an address write on the timeline. Find an interleaving where a separate status check becomes stale.

Describe a database conditional update or transaction that preserves the rule. Explain how a failed condition is reported. The in-memory example does not implement this production solution.

## 4. Give administrators an appropriate policy

Explain why a customer ownership rule is insufficient for authorized administrators. Define a particular privileged operation and its required permission. Check both a real authorized operator and an ordinary customer sending an admin-looking role field.

**Check your answer:** permission comes from trusted server context and applies to the operation; the request body cannot grant itself authority. Production policies may also limit tenant, action, value or scope.

## 5. Add another route into the shop

Use [the growing-shop figure](../presentation/assets/growing-shop.svg) as a design prompt. Add a mobile endpoint to a copy of the model. Trace identity and authorization through it, including any internal service call.

Record a threat, its control, and an integration-test idea for that new route. Do not assume that the existing web endpoint's guard automatically protects it. The diagram illustrates a possible design; it is not an implemented extension.

## 6. Challenge the loss table

Run the unchanged baseline, then the supplied no-dominance and tie examples:

```sh
python3 game-theory/payoff.py
python3 game-theory/payoff.py --file game-theory/examples/no-dominance.json
python3 game-theory/payoff.py --file game-theory/examples/ties.json
```

Explain why the baseline eliminates one attack, why crossing preferences do not, and why equal losses do not establish strict dominance. A worst-case single-action recommendation is not a general solution to every strategic decision problem.

## 7. Return to the release decision

Before choosing what to fix, write down the evidence you still need: reachability, attacker capability, scope of harm, existing controls, remediation effort and interim options. State what new evidence would change your decision.

**Check your answer:** invented loss values cannot establish real risk. Restrictions, compensating controls or release delay may be options outside the two-row exercise.
