# M2 native AmigaGuide qualification

Status: PASS — automated AROS compatibility gate PASS; visible AmigaOS
navigation gate PASS

This is the final M2 qualification procedure. It combines the existing
automated native AROS compatibility gate with a human-visible AmigaOS gate.
The latter uses FS-UAE from the standard `Ploos-AS/amiga-runtime`
infrastructure and a user-owned AmigaOS installation.

Never commit or upload Kickstart ROMs, Workbench or AmigaOS files, keys, disk
images, or other licensed system files. The generated qualification bundle
contains only redistributable Documentation-Tools output and metadata.

## Automated AROS compatibility gate

GitHub Actions runs `.github/workflows/aros-amigaguide.yml` using the current
verifiable `deadwood2/AROS` ABIv11 Linux-hosted release. It builds and
structurally validates `ExampleAmiga.guide`, verifies the AROS runtime,
launches the guide through native AROS MultiView, and retains runtime evidence.

Hosted AROS renders native Intuition windows inside one top-level X11 AROS
screen. A separate X11 window named MultiView is not required. This
non-proprietary automated result does not replace the visible AmigaOS test.

## Baseline target

Use all of the following:

- the `a500plus` 68000 profile from `Ploos-AS/amiga-runtime`;
- a visible, non-headless FS-UAE session;
- AmigaOS 2.04 or later from files owned by the operator;
- a native AmigaGuide viewer or MultiView-capable environment;
- the generated `Work:` directory volume described below.

The preparation tool verifies that the selected amiga-runtime checkout contains
its FS-UAE backend and that `profiles/a500plus.conf` remains a 68000 profile.
It records the exact amiga-runtime revision and profile digest in the result
template. Documentation-Tools does not contain a second emulator/runtime
implementation.

## Prepare the Work volume

From the Documentation-Tools checkout, with the standard amiga-runtime checkout
next to it, run:

```sh
python3 tools/prepare-m2-native-qualification.py \
  --amiga-runtime ../amiga-runtime
```

This performs the required workflow in order:

1. validates `examples/ExampleAmigaManual.md`;
2. builds `ExampleAmiga.guide` with the existing generator;
3. runs the existing AmigaGuide structural validator;
4. verifies the amiga-runtime FS-UAE integration and 68000 profile;
5. creates `dist/m2-native-qualification/Work`;
6. records both repository revisions and the guide SHA-256;
7. emits a PENDING result and checklist without changing M2 status.

The `Work` directory contains only `ExampleAmiga.guide`, operator instructions,
checksums, and qualification metadata. It may be mounted directly as an FS-UAE
directory hard drive or copied into an existing Amiga-visible Work volume.

## Start the visible FS-UAE session

First create a saved FS-UAE configuration outside both repositories. It must
boot the operator's licensed AmigaOS 2.04+ system, match the amiga-runtime
`a500plus` profile (A500 Plus and 68000), and provide a native guide viewer.
Set `FS_UAE_CONFIG` to that configuration's absolute path.

Then run these exact commands from Documentation-Tools:

```sh
doc_tools=$PWD
runtime_dir=../amiga-runtime
python3 tools/prepare-m2-native-qualification.py \
  --amiga-runtime "$runtime_dir"
sh "$runtime_dir/backends/fs-uae/backend" probe
cd "$runtime_dir"
fs-uae "$FS_UAE_CONFIG" \
  --hard_drive_9="$doc_tools/dist/m2-native-qualification/Work" \
  --hard_drive_9_label=Work \
  --hard_drive_9_read_only=1 \
  --automatic_input_grab=0 \
  --fullscreen=0
```

The last command is intentionally visible and has no timeout or headless
wrapper. Drive slot 9 is used to avoid the usual system-drive slots; if the
saved configuration already uses slot 9, use another unused slot from 0 through
9 consistently for the three `hard_drive` options.

[FS-UAE supports mounting a host folder as an Amiga directory hard drive](https://fs-uae.net/docs/hard-drives/).
The saved configuration and every licensed file it references stay outside
this repository and outside the qualification bundle.

Inside AmigaOS, open `Work:ExampleAmiga.guide` with the native viewer. A typical
Shell command, when MultiView is installed, is:

```text
SYS:Utilities/MultiView Work:ExampleAmiga.guide
```

Using the Workbench icon or another native AmigaGuide-capable viewer is valid;
record the exact viewer used.

## Visible PASS/FAIL checklist

Record one PASS or FAIL for every item:

1. Guide opens without a parser or requester error.
2. Main node renders with its generated section links.
3. The first section link from Main works.
4. A middle section link from Main works.
5. The last section link from Main works.
6. Prev works where present.
7. Contents returns to Main.
8. Next works where present.
9. An internal cross-reference works.
10. Preformatted and code text renders correctly without command interpretation.
11. The literal `user@example.invalid` address renders with one `@` character.
12. Node names and navigation labels are valid, untruncated, and well formed.
13. The viewer closes normally.

The fixture's Introduction-to-Command Reference link and Troubleshooting-to-
Introduction link exercise internal references. Its Quick Start, Command
Reference, and ARexx Reference examples exercise preformatted text.

## Record the human result

After closing FS-UAE, run the interactive recorder:

```sh
python3 tools/record-m2-native-qualification.py
```

It verifies the guide digest before prompting for:

- FS-UAE version;
- exact AmigaOS version;
- viewer;
- date;
- each checklist PASS/FAIL result;
- optional notes.

The existing result already contains the Documentation-Tools commit SHA,
amiga-runtime commit SHA, `ExampleAmiga.guide` SHA-256, and Amiga profile. A
failed item makes the visible gate FAIL. Passing every item makes that recorded
visible gate PASS, but the tool never edits `README.md` or `ROADMAP.md` and does
not declare the M2 milestone complete.

## Qualified M2 result

The final visible gate passed on 2026-09-22 with all 13 checklist items marked
PASS. The qualified inputs and runtime were:

- Documentation-Tools source revision: `21865b1e4286b3bb96b7b7c0c6ac63a7b7002957`;
- amiga-runtime revision: `327292c45d9440127b31ec9e289ad0416e26d781`;
- `ExampleAmiga.guide` SHA-256: `383756b99bd63a170bfdde90287a269bb0a007f2a67054f44d08a0b6d7acd8f6`;
- FS-UAE 3.2.35 using the `a500plus` 68000 profile with 1 MiB Chip RAM,
  1 MiB Slow RAM, and no Fast RAM;
- AmigaOS 2.04 / Kickstart revision 37.175;
- native AmigaGuide 34.3 viewer;
- generated `Work:` directory mounted read-only.

The machine-readable result remains in the generated local qualification bundle
at `dist/m2-native-qualification/Work/qualification-result.json`. Screenshots
are retained separately outside the repository and are not packaged with the
bundle. Kickstart, Workbench, AmigaOS, viewer binaries, libraries, and other
licensed system files are never copied into qualification output or evidence.

## M2 PASS rule

M2 may be changed to PASS only after a person reviews evidence showing that:

- GitHub Actions structural qualification is green for the qualified source;
- the automated AROS MultiView compatibility gate is green;
- the visible result refers to the same Documentation-Tools source revision and
  guide SHA-256; and
- every visible AmigaOS checklist item is PASS.

The qualified result above satisfied this rule. Future changes that alter the
generated AmigaGuide must repeat the gate against the new source revision and
guide digest rather than reusing these observations.

If any item fails, retain the FAIL record, keep M2 pending, fix the generator or
fixture, rerun CI, rebuild the bundle, and repeat the visible gate. Screenshots
may be retained separately but must not include or be packaged with licensed
system files.
