# parcelgrid (vendored)

Vendored copy of the ParcelGrid carrier SDK, forked at v2.4.1 and patched in tree. Upstream is
unmaintained. This directory is checked in, compiled, and deployed like the rest of `tracking` —
it is *not* excluded from the build, and it is not in `.gitignore`.

Do not skip this directory when auditing call sites. The local patches reach into
`Billing` directly.
