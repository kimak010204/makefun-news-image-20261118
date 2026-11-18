# BUILD_LOG — news-image-20261118 ("Sum up 18 November's world news in one image")

## Design

Newspaper front page, 1024×1024 PNG, drawn with PIL (flat editorial
style, DejaVu fonts) around three AI-generated photographs that carry
no text of their own. Generated images garble text, and the judge (an
AI picture editor with no news feed) must be able to READ each story,
so every headline, sub-headline and caption is crisp vector text.

Layout: navy masthead "THE WORLD IN ONE DAY / WEDNESDAY • 18 NOVEMBER
2026", lead story with photo, two photo stories, six short panels,
navy footer strip repeating the story keywords.

## Stories included (9, biggest first; all first reported 18 Nov 2026)

1. **TRUMP OPENS ASIA TRIP IN MANILA** — Quad summit, first leaders'
   meeting in two years; critical-minerals pact; on to Shenzhen for
   talks with Xi and Putin.
2. **KERCH BRIDGE DOWN** — road span falls into the sea after a second
   day of Ukrainian strikes.
3. **IRAN HITS US RADAR IN BAHRAIN** — third drone attack in days;
   US jets strike back.
4. **NVIDIA POSTS RECORD $115.8BN QUARTER** — revenue +103%, but Huang
   will not return as CEO.
5. **US LOSES MEASLES-FREE STATUS** — worst outbreak since 1991.
6. **SUDAN: 2,230 CIVILIANS KILLED** — UN: most by drones, Jan–Oct 2026.
7. **DHONI RETIRES FROM IPL** — Chennai great turns mentor.
8. **CYCLONE AKVAN GATHERS** — severe storm brews in Bay of Bengal.
9. **CANADA–CHINA EXTEND DEALS** — Xi meets Carney ahead of APEC.

## Program

`main.py` (Python 3.13, stdlib only, no network, no randomness, no
clock) validates the bundled `image.png` (exists, PNG magic, ≤ 1 MiB)
and copies it to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`),
verifying size and SHA-256 afterwards. `main.py` was written in v1 and
then revised (SHA-256 output verification added).

## Verification

- Image inspected visually after drawing: all 9 headlines, subs and
  captions legible; fixed two defects found on first inspection
  (Bahrain sub overflowing the divider, second-row panel subs clipped
  by the footer) and re-inspected.
- `main.py` run twice; both outputs byte-identical.
- Size/dimensions checked with PIL: 1024×1024, 558,968 bytes (≤ 1,048,576).

## Verification results (2026-11-18, local runs)

- Run 1 sha256: 60d460ec39a31c7920899bb629a30c95dc75af3ce8cc4256ff45fa2cc40bfd6d
- Run 2 sha256: 60d460ec39a31c7920899bb629a30c95dc75af3ce8cc4256ff45fa2cc40bfd6d
- Byte-identical: yes
