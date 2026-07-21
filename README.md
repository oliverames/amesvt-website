# amesvt.com

This repository publishes the small Cloudflare Pages site at [amesvt.com](https://amesvt.com). It is a directory for Oliver's personal utilities; [ames.consulting](https://ames.consulting) is the public-facing site. It also serves Matrix client and server discovery files from `/.well-known/matrix/`.

There is no build step. Cloudflare Pages serves `index.html`, `_headers`, and the `.well-known` directory directly from `main`.

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

## Deploy

Deploy the repository root to the `amesvt-website` Cloudflare Pages project:

```sh
python3 scripts/build.py
npx wrangler pages deploy _site --project-name amesvt-website --branch main
```

After deployment, check the home page and both Matrix discovery endpoints:

```sh
curl -fsS https://amesvt.com/.well-known/matrix/server
curl -fsS https://amesvt.com/.well-known/matrix/client
```

## Rights

This is a personal website. No license is granted for reuse of its content or design.
