#!/bin/bash
set -euo pipefail
exec rq worker default --url ${REDIS_URL:-redis://redis:6379/0}
