.PHONY: up-local down-local logs-local tf-init tf-plan tf-apply

up-local:
	docker compose -f infra/docker/docker-compose.local.yml up -d --build

down-local:
	docker compose -f infra/docker/docker-compose.local.yml down -v

logs-local:
	docker compose -f infra/docker/docker-compose.local.yml logs -f

tf-init:
	cd infra/terraform/cloudflare && terraform init && terraform validate
	cd infra/terraform/hetzner && terraform init && terraform validate

tf-plan:
	cd infra/terraform/cloudflare && terraform plan -out=tfplan || true
	cd infra/terraform/hetzner && terraform plan -out=tfplan || true

tf-apply:
	cd infra/terraform/cloudflare && terraform apply -auto-approve tfplan || true
	cd infra/terraform/hetzner && terraform apply -auto-approve tfplan || true
