IMAGE = inventicon/message-db
VERSIONS := 11 12 13 14 15
VARIANTS := alpine bullseye bookworm

TARGETS = $(foreach variant,$(VARIANTS),$(foreach version,$(VERSIONS),$(version)-$(variant)))

$(TARGETS): %:
	@docker build --tag $(IMAGE):$* --build-arg BASE_IMAGE=postgres:$* .

$(addsuffix /run, $(TARGETS)): %/run:
	@docker run --rm --interactive --tty --publish 5432:5432 --env POSTGRES_PASSWORD=message_store $(IMAGE):$*

$(addsuffix /shell, $(TARGETS)): %/shell:
	@docker run --rm --interactive --tty --entrypoint sh $(IMAGE):$*
