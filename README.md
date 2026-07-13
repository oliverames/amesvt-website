# amesvt.com

This repository publishes the small static site at [amesvt.com](https://amesvt.com). It also serves Matrix client and server discovery files from `/.well-known/matrix/`.

There is no build step. GitHub Pages serves `index.html`, `CNAME`, and the `.well-known` directory directly from `main`.

## Check changes locally

Run the repository validator:

```sh
python3 scripts/validate.py
```

To view the site locally:

```sh
python3 -m http.server 8000
```

Then open `http://localhost:8000`.

## Release

Push a reviewed change to `main`. GitHub Pages deploys the updated files automatically. After deployment, check the home page and both Matrix discovery endpoints:

```sh
curl -fsS https://amesvt.com/.well-known/matrix/server
curl -fsS https://amesvt.com/.well-known/matrix/client
```

## Rights

This is a personal website. No license is granted for reuse of its content or design.
