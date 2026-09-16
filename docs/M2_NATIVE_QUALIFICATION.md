# M2 Native AmigaGuide Qualification

Status: PENDING

This is the final M2 gate. It verifies the generated `.guide` with the native AmigaGuide viewer on AmigaOS. Proprietary Kickstart ROMs and AmigaOS files must never be committed to this repository.

## Target

Baseline qualification target:

- visible FS-UAE session;
- AmigaOS 2.04 or later;
- native AmigaGuide/Multiview-capable environment available on the test system;
- generated `dist/ExampleAmiga.guide` copied to the Amiga-visible test volume.

## Prepare on the host

```sh
git pull --ff-only
rm -rf dist
mkdir -p dist
python3 tools/validate-docs.py examples/ExampleAmigaManual.md
python3 tools/build-amigaguide.py examples/ExampleAmigaManual.md dist/ExampleAmiga.guide
python3 tools/validate-amigaguide.py dist/ExampleAmiga.guide
sha256sum dist/ExampleAmiga.guide
```

The structural validator must pass before the native test starts.

## Native test

Open the generated guide with the native AmigaGuide viewer. Do not run this qualification headless.

Verify all of the following:

1. The guide opens without a parser/requester error.
2. The Main node is visible and contains the generated section links.
3. Open at least the first, one middle, and the last section from Main.
4. `Prev`, `Contents`, and `Next` navigation works where each link is expected.
5. Follow at least one generated internal cross-reference when the fixture contains one.
6. Code/preformatted text is readable and does not become AmigaGuide commands.
7. Literal `@` text, if present in the fixture, renders as text rather than being interpreted as a command.
8. No visibly broken node names, truncated navigation labels, or malformed text are observed.
9. Return to Main and close the viewer normally.

## Evidence

Record:

- date;
- repository commit SHA;
- SHA-256 of `ExampleAmiga.guide`;
- emulator/hardware and version;
- Amiga model/CPU profile;
- AmigaOS version;
- viewer used;
- PASS/FAIL for each native test item;
- notes for any normalization or environment-specific behavior.

Screenshots are useful evidence but are not required to be committed. Never add proprietary ROM, Workbench, AmigaOS, or other licensed system files as evidence.

## PASS rule

M2 may be marked PASS only when:

- GitHub Actions structural qualification is green for the qualified source commit; and
- every native test item above passes against an artifact generated from that source.

If any native item fails, keep M2 pending, record the failure precisely, fix the generator or fixture, rerun CI, and repeat native qualification.
