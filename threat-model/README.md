# Shop threat model

`shop-app.cdx.json` is the importable model. It contains five actors/components, three zones, eight directional flows, two threats and two linked controls. `shop-app.source.json` is authoring state; `register.md` and `register.json` provide a readable and structured threat/control record.

Follow the [Precogly walkthrough](../precogly/walkthrough.md) to inspect and edit the model. Save a copy before closing the guest editor.

The controls are proposed for a fictional application. T1 covers unauthorized order reads and delivery-address changes; T2 covers unauthorized administrative operations. The associated code demonstrates policy checks, not a deployed system.

The bundled frontend is pinned to `775a32647263ed7f25e1515fe6df7a8828812e1c`. Its serializer, import, linked controls, save and reopen behavior were checked. This verifies that build's own round trip, not all interchange consumers. Trust-level numbers are illustrative UI annotations, not calibrated risk values.

To rebuild from authoring state, use the exact source version above with its frontend dependencies installed:

```sh
node scripts/build-models.mjs /path/to/precogly/frontend
```

The script uses Precogly's actual serializer. It is optional; viewing and editing the prepared model needs only Python and a browser.
