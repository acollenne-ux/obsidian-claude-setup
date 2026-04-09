#!/usr/bin/env bash
# Demarre n8n self-hosted en arriere-plan avec les bonnes env vars.
# A utiliser avec run_in_background=true.

export N8N_HOST=localhost
export N8N_PORT=5678
export N8N_PROTOCOL=http
export WEBHOOK_URL=http://localhost:5678/
export N8N_DIAGNOSTICS_ENABLED=false
export N8N_VERSION_NOTIFICATIONS_ENABLED=false
export N8N_PERSONALIZATION_ENABLED=false
export N8N_RUNNERS_ENABLED=true
export N8N_PUBLIC_API_DISABLED=false
export N8N_USER_FOLDER="$HOME/.n8n-claude-local"
export DB_TYPE=sqlite
# Disable user setup wizard popup if possible
export N8N_HIDE_USAGE_PAGE=true

mkdir -p "$N8N_USER_FOLDER"

exec n8n start
