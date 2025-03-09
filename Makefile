serve-api:
	uv run fastapi dev
PHONY: serve-api

serve-demo:
	cd demo && python3 -m http.server 8001
PHONY: serve-demo

verify-images-loop:
	while true; do \
		printf "Verifying..."; \
		uv run verifier/main.py; \
		echo " done"; \
		sleep 5; \
	done
PHONY: verify-images-loop

black:
	uv run black app db-models modifier verifier
PHONY: black

pyright:
	uv run pyright
PHONY: pyright

reset:
	source .env && \
		echo $$SQLALCHEMY_DATABASE_URI | cut -d '/' -f 4- | xargs rm -f && \
		rm -rf $$IMAGE_UPLOADED_PATH && \
		rm -rf $$IMAGE_MODIFIED_PATH
PHONY: reset
