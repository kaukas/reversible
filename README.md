# Reversible

An API service that performs pixel level modifications to images, and stores the images, both original and modified.

Currently supported modifications:

- Invert bits of RGB values of random pixels.

*More to be implemented later.*

The project also includes a tool to verify that modified images become identical once changes are reversed.

Only PNG images supported at the moment. For JPEG, Pillow modifies the originals before even saving them which makes them irreversable.

## Setup

[uv](https://docs.astral.sh/uv/) is used to manage project environment and dependencies. Please install it first.

Project dependencies can be installed with:

```sh
make install
```

## Run

Run the API service:

```sh
make serve-api
```

Run the modification reversibility checker:

```sh
make verify-images-loop
```

Run the demo page frontend:

```sh
make serve-demo
```

Then you can open [the demo page](http://localhost:8001) to interact with the API. It allows uploading images and seeing their status: if they get successfully modified, and if their modifications are reversible.

You can also view [the generated API documentation](http://localhost:8000/redoc).

By default, SQLite is used as a development database, and files are stored in `/tmp`. The database and all the files can be removed by running:

```sh
make reset
```

## Run tests

Pytest is used to run tests:

```sh
make pytest
```

## Code checks

Reformat code with black:

```sh
make black
```

Check Python types with pyright:

```sh
make pyright
```

# Project contents

The `app` folder stores the API service code. The service can list uploaded images and supports an upload of another image. After upload the service parses the image with [Pillow](https://pillow.readthedocs.io/), modifies it, and stores both versions on disk. The modification metadata is stored in a SQLite database. Image file retrieval not implemented yet.

The `verifier` folder stores a script to verify that image modifications are reversible. It reads the modified images, modifies them in reverse, and compares results to the original images.

The app and the verifier have common dependencies: the `images` DB table definition stored in the `db-models` folder, and the modifications implementation stored in the `modifier` folder.

The `demo` folder stores a static page to list the uploaded images, and to upload a new one. Refresh the page to observe images (modifications, reversibility checks) being processed.
