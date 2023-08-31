alpine:
	@docker build -t inventicon/message-db:alpine \
	--build-arg BASE_IMAGE=postgres:15-alpine .

alpine/run:
	@docker run --rm -it -p 5432:5432 \
	--env POSTGRES_PASSWORD=message_store \
	inventicon/message-db:alpine

alpine/shell:
	@docker run --rm -it --entrypoint sh inventicon/message-db:alpine

debian:
	@docker build -t inventicon/message-db:debian \
	--build-arg BASE_IMAGE=postgres:15-bookworm .

debian/run:
	@docker run --rm -it -p 5432:5432 \
	--env POSTGRES_PASSWORD=message_store \
	inventicon/message-db:debian

debian/shell:
	@docker run --rm -it --entrypoint bash inventicon/message-db:debian
