# OHMind documentation

Source for <https://lunyang.github.io/>. The site uses GitHub Pages/Jekyll and Just the Docs. Application source lives separately at <https://github.com/lunyang/OHMind>.

## Preview

Install Ruby, its development headers (for example `ruby-dev` on Ubuntu), a C/C++ build toolchain, and Bundler, then run:

```bash
bundle install
bundle exec jekyll build --strict_front_matter
bundle exec jekyll serve --host 127.0.0.1
```

Open <http://127.0.0.1:4000/>. Ruby dependencies and the pinned remote theme require network access on the first build. Build output is ignored. Use `bundle3.0` instead of `bundle` if your distribution names the executable that way.

Run the standard-library-only site check after building:

```bash
python3 scripts/check_site.py _site
```

## Updating content

Use the actual application implementation to verify settings and behavior. Keep page permalinks stable. New pages need a title, permalink, layout, and parent/navigation order where applicable. Use Jekyll link tags for internal Markdown page links so missing targets fail the build. Record the source revision and material integration limits in `release-notes.md`; do not invent a released software version.

## Publish

Review the documentation branch, reconcile its source baseline with the code users can obtain, and run the build/link checks. Then merge into the branch selected in the repository's Settings → Pages. The inspected repository's default branch is `master`; verify the actual Pages source in GitHub before merging. Check the Pages deployment result and live installation, memory, and resume pages afterward.

A local build or a local branch does not update the public website. This repository update does not publish the separate OHMind code repository.
