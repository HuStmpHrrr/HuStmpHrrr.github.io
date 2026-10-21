template taken from
[https://github.com/BlackrockDigital/startbootstrap-resume](https://github.com/BlackrockDigital/startbootstrap-resume).

# Dependencies

* Pelican
* PyYaml

# Publishing

This is the `source` branch of `HuStmpHrrr.github.io`. Pushing to it runs
`.github/workflows/build-site.yml`, which builds the site inside the
`ghcr.io/hustmphrrr/site-builder` image and commits the result to `master`.
The image is defined by `Dockerfile` / `requirements.txt` and is rebuilt by
`.github/workflows/docker-image.yml` whenever they change.
