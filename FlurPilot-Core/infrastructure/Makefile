
# Makefile for FlurPilot Infrastructure

.PHONY: init plan apply deploy destroy

# Variables - Adjust if needed or use environment variables
TF_DIR := .
ANSIBLE_DIR := ansible
PLAYBOOK := $(ANSIBLE_DIR)/deploy.yml
TF_OUTPUT_IP := $(shell terraform output -raw ipv4_address 2>/dev/null)

# Terraform Commands
init:
	terraform init

plan:
	terraform plan -out=tfplan

apply:
	terraform apply tfplan

destroy:
	terraform destroy

# Ansible Deployment
# Requires Terraform to be applied first to get the IP
deploy:
	@if [ -z "$(TF_OUTPUT_IP)" ]; then \
		echo "Error: Server IP not found. Run 'make apply' first."; \
		exit 1; \
	fi
	@echo "Deploying to $(TF_OUTPUT_IP)..."
	# Ensure private key is added to ssh-agent or specify with --private-key
	ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i "$(TF_OUTPUT_IP)," $(PLAYBOOK) \
		--user deployer \
		--extra-vars "check_env_supabase_url=$${SUPABASE_URL}" \
		--extra-vars "check_env_supabase_anon=$${SUPABASE_ANON_KEY}" \
		--extra-vars "check_env_db_pass=$${DB_PASSWORD}"
