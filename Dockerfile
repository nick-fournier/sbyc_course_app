# Build stage runs on the CI host's native arch; its output is plain static files.
FROM --platform=$BUILDPLATFORM python:3.12-slim AS build
RUN pip install --no-cache-dir pyyaml
WORKDIR /src
COPY build.py .
COPY data data
COPY site site
RUN python build.py --out /dist

FROM nginx:1.27-alpine
COPY --from=build /dist /usr/share/nginx/html
