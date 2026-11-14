# Your Threat Model Has an Opponent

Resources from the DelhiFOSS talk: start with two access-control flaws in a fictional shop, consider the attacker's choices, and build a threat model whose controls can be checked.

**A vulnerability list is the beginning. Follow the attacker, trace the system, and verify the controls.**

## Try the live matrix

**[Open the interactive demo](https://sidd190.github.io/DELHIFOSS_14/)** — edit the four losses or try the presets. It runs in your browser; no installation or account is needed.

## Explore the material

- [Slides (PDF)](presentation/slides.pdf) and [browser slides](presentation/slides.html).
- [Shop architecture](architecture/shop-app.md), [diagram](architecture/shop-app.svg) and [printable diagram](architecture/architecture.pdf).
- [Precogly model](threat-model/shop-app.cdx.json) and [threat/control register](threat-model/register.md).
- [Hands-on Precogly walkthrough](precogly/walkthrough.md).
- [Loss-matrix example](game-theory/README.md) and [Python program](game-theory/payoff.py).
- [Authorization example](demo/authorization.py), [its scope](demo/README.md) and [tests](tests/).
- [Exercises](exercises/README.md) and [further reading](resources/further-reading.md).

GitHub displays the PDF and Markdown directly. To use the HTML slides, interactive matrix and bundled Precogly editor, download or clone the repository and run it locally.

## Run locally

Requires **Python 3.10+** and a modern browser. No package installation, account or internet connection is required after downloading the repository.

```sh
git clone https://github.com/sidd190/DELHIFOSS_14.git
cd DELHIFOSS_14
bash start.sh
```

Open **http://127.0.0.1:4173** for the resources and **http://127.0.0.1:4174/guest** for Precogly. Keep the terminal running; Ctrl+C stops both servers. On Windows, run `python scripts/serve.py`. If those ports are already in use, stop the earlier instance before starting another.

```sh
python3 game-theory/payoff.py
python3 -m unittest discover -s tests -v
```

The browser slides use arrow keys or space to advance and F for fullscreen.

## The example

Customers can read their orders and change the delivery address **before dispatch**. Administrators perform privileged operations. T1 examines missing ownership checks on reads and writes; T2 examines missing permission checks on administrative operations. A denied write must leave the stored order unchanged.

The game uses the following invented losses. The defender minimizes; the attacker maximizes.

| Defender | Attack API | Attack admin |
|---|---:|---:|
| Fix API | 2 | 8 |
| Harden admin | 4 | 5 |

For the attacker, **Attack API is strictly dominated**: 8 > 2 and 5 > 4. Against Attack admin, the defender chooses **Harden admin**, giving loss 5 instead of 8. Hardening admin is a best response here, not a dominant defensive strategy.

The four questions connect the decision to the application:

1. What are we working on?
2. What can go wrong?
3. What are we going to do about it?
4. Did we do a good enough job?

## What these artifacts establish

The small in-memory code example checks ownership, address-edit eligibility and administrative permission. Its tests include rejected-write state checks and deliberate guard-removal checks. It is not a deployed shop, authentication system or database transaction design. Real implementations need consistent endpoint authorization and atomic handling of dispatch status and address updates.

The Precogly frontend is pinned to commit `775a32647263ed7f25e1515fe6df7a8828812e1c`. Its import, linked threats/controls, save and reopen workflow was checked. This does not establish compatibility with every interchange consumer or prove the application secure. See [bundle provenance and licenses](vendor/precogly/README.md).

The larger-shop figure is a hypothetical design extension. The executable example and saved model cover the smaller shop.

## Adapt it

Edit the matrix or make a copy of the threat model. Start from the [exercises](exercises/README.md), change one thing, and explain which control or test must change with it.

The audience slide source is [presentation/slides.source.json](presentation/slides.source.json). Run `python3 scripts/build_slides.py` after changing it. Diagrams are editable SVG files. To regenerate the model from its authoring JSON, see [threat-model/README.md](threat-model/README.md).

Original examples and slides are MIT licensed. The bundled Precogly build and dependencies retain their own licenses and notices under `vendor/precogly/`.

The live matrix is published from `docs/` through GitHub Pages. After editing `demo/matrix.html`, run `python3 scripts/build_demo.py` and commit the regenerated `docs/index.html`.

Web photographs and illustrations retain their Creative Commons licenses; see [asset credits](presentation/ASSET-CREDITS.md). The meme captions are fictional.

The current deck uses a hands-on Precogly walkthrough after the tool introduction. The meme panels use credited web assets and fictional captions.
