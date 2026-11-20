# SkeuoHLE

**SkeuoHLE** is the iPhone OS emulator core embedded in SkeuoLauncher. It is a high-level emulator for early iPhone OS apps: it reimplements selected iOS frameworks on the host, so compatible apps run without booting iOS.

SkeuoHLE is built on [touchHLE](https://github.com/touchHLE/touchHLE) and the community forks that carry it forward. See [NOTICE](NOTICE) for the full lineage and attribution. It is not an official Apple or touchHLE product.

The repository does not distribute commercial apps or iOS firmware. Use only app bundles (`.app`) or IPAs (`.ipa`) that you are entitled to use.

## Embedded Android core

The Android host loads `libskeuohle_core.so`, built from [`platform/android/skeuohle_embed`](platform/android/skeuohle_embed). It has no SDL window or app picker: the host app renders it into its own `Surface`, from a bound service running in a separate process, and forwards touch, motion, text and lifecycle events over JNI (`com.vokki.skeuolauncher.skeuohle.SkeuoHleCore`).

```sh
cargo build -p skeuohle_embed --release --target aarch64-linux-android
```

The [embedded workflow](.github/workflows/skeuohle_embedded.yml) builds the same library in CI and packages it with its license and source notices.

## Desktop build

```sh
cargo run --release -- path/to/app.app
```

Command-line options are documented in [`OPTIONS_HELP.txt`](OPTIONS_HELP.txt); compatibility changes are tracked in [`CHANGELOG.md`](CHANGELOG.md).

## License

The emulator source and its modifications are under the [Mozilla Public License 2.0](LICENSE). Copyright remains with the respective contributors. See [NOTICE](NOTICE) for attribution and [LICENSING.md](LICENSING.md) for third-party licenses and binary distribution requirements. Bundled libraries, fonts and platform code with separate notices keep their own licenses.
