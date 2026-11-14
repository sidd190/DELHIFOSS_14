# Bundled Precogly frontend

This is a real compiled Precogly frontend, included so the guest editor demo works offline.

Upstream: https://github.com/precogly/precogly
Source: commit `775a32647263ed7f25e1515fe6df7a8828812e1c`
Frontend package version: `0.3.0` (not asserted to be the latest release).
License: Apache-2.0; see `LICENSE` and `THIRD_PARTY_NOTICES.txt`.

Build: Vite production build of the frontend at this commit, without source changes. Only guest routes are supported by the bundled local server. Signed-in features require a backend and are outside this demonstration. Guest save/open, the shop component/threat/control relationships and screenshots are checked in the browser; see `../../evidence/`.

To rebuild, check out this exact commit, install its lockfile dependencies, and build the frontend into `vendor/precogly/app`. The original tool uses absolute asset paths; the provided launcher serves it on a dedicated localhost port. A `file://` URL is not sufficient for this compiled app. Your slides and original diagrams can be opened directly.

This build uses the serializer's CycloneDX 2.0 representation. We verify its own round trip, not schema equivalence to future revisions or support in unrelated products.

The source checkout's package manifest and lockfile are included as `build-package.json` and `build-package-lock.json`. Existing installed dependencies were used; no claim of a byte-identical future rebuild is made. Node was v24.16.0, Vite reported v7.3.2, and Chrome used for verification was 150.0.7871.114.

