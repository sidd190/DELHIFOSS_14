# A game solved by strict dominance

Rows are defensive actions. Columns are attacks. Entries are invented losses to the shop, not measured business losses or vulnerability scores. The defender minimizes; this attacker maximizes the same values.

| Defender | Attack API | Attack admin |
|---|---:|---:|
| Fix API | 2 | 8 |
| Harden admin | 4 | 5 |

Read across each row as the attacker:

- If the defender fixes the API: 8 > 2, so attack admin.
- If the defender hardens admin: 5 > 4, so attack admin.

**Attack API is strictly dominated by Attack admin.** It is worse for the attacker in every row. Eliminate that column; the defender then chooses between 8 and 5. **Harden admin, loss 5.**

The row worst cases are also 8 and 5. Minimizing those gives the same answer. At (Harden admin, Attack admin), the defender cannot reduce loss by switching rows (5 → 8), and the attacker cannot increase loss by switching columns (5 → 4). This is a pure saddle point.

Do not say the defender has a dominant strategy. Against Attack API, Fix API is better (2 < 4); against Attack admin, Harden admin is better (5 < 8). It is the **attacker's** dominated option that makes this example simple. Observing the defensive choice does not change the attacker's preference in this table.

## Run it

```sh
python3 game-theory/payoff.py
python3 game-theory/payoff.py 2 8 4 5
python3 game-theory/payoff.py --file game-theory/examples/baseline.json --json
bash test.sh
```

Try the other saved matrices: `no-dominance.json` shows crossing attack preferences; `ties.json` shows that equal outcomes are not strict dominance. The script reports a worst-case single-action recommendation even when no pure saddle point exists; it does not claim to solve a more general game in that case.

The solver uses exact rational arithmetic and rejects non-finite or malformed inputs. Tests check the direction of dominance, ties, decimal values, saddle-point conditions across 1,296 matrices and invalid inputs. The browser explorer duplicates the same simple comparisons with normal JavaScript numbers.

## Interpreting the numbers

These values illustrate broad defensive actions and remaining harm. A nonzero repaired-route loss does not mean a completely fixed ownership defect remains exploitable. The values could include incomplete coverage or other residual harm; in a real assessment that interpretation needs evidence. The admin route may affect more orders than one object-level API request. The table is not a measurement of this fictional application.

The game omits remediation costs, release delay, simultaneous attacks, chained flaws, attacker effort and alternative goals. In reality, blocking release or restricting an exposed service may be appropriate. Use the example to explain an opponent's choices, not as a universal patch-prioritization rule.
