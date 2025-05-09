#!/bin/bash --login
#-------------------------------------------------------------------------------
set -e
cd /usr/local/share/zimagi

SERVICE_TYPE="$1"
SERVICE_SETTINGS="${2:-$SERVICE_TYPE}"

if [[ -z "$SERVICE_TYPE" ]]; then
  echo "Service gateway requires a process type identifier"
  exit 1
fi
if [[ -f "./scripts/config/${SERVICE_TYPE}.sh" ]]; then
  source "./scripts/config/${SERVICE_TYPE}.sh"
fi

# Service initialization mode
export ZIMAGI_SERVICE_INIT=True
export "ZIMAGI_${SERVICE_TYPE^^}_INIT"=True
export ZIMAGI_NO_MIGRATE=True
export ZIMAGI_SERVICE="$SERVICE_SETTINGS"
#-------------------------------------------------------------------------------

if [ "$SERVICE_TYPE" == "worker" ]; then
  trap 'kill -s TERM "$PPID"; echo "Command exited <$?>: $BASH_COMMAND"' EXIT
  trap 'kill -s TERM "${PROCESS_PID}"; wait "${PROCESS_PID}"; cleanup' SIGTERM
fi

function cleanup () {
  echo ""
  echo "================================================================================"
  echo "> Service shut down: cleaning up"
  echo ""
  rm -f "/var/local/zimagi/${SERVICE_TYPE}.pid"
}

echo ""
echo "================================================================================"
echo "================================================================================"
echo "--------------------------------------------------------------------------------"
echo "> Initializing ${SERVICE_TYPE} service"
echo ""
if [[ ! -z "$ZIMAGI_POSTGRES_HOST" ]] && [[ ! -z "$ZIMAGI_POSTGRES_PORT" ]]; then
  ./scripts/wait.sh --hosts="$ZIMAGI_POSTGRES_HOST" --port=$ZIMAGI_POSTGRES_PORT --timeout=60
fi
if [[ ! -z "$ZIMAGI_REDIS_HOST" ]] && [[ ! -z "$ZIMAGI_REDIS_PORT" ]]; then
  ./scripts/wait.sh --hosts="$ZIMAGI_REDIS_HOST" --port=$ZIMAGI_REDIS_PORT --timeout=60
fi

if [[ "${SERVICE_TYPE^^}" == "SCHEDULER" ]]; then
  zimagi migrate
  zimagi module init
  if [[ ! -z "$ZIMAGI_ADMIN_API_KEY" ]]; then
    zimagi user save admin encryption_key="$ZIMAGI_ADMIN_API_KEY" --lock=admin_key_init --lock-timeout=0 --run-once
  fi
else
  zimagi service lock wait startup --timeout=120
  zimagi module init --types=module
fi
zimagi info

if [[ ! -z "${ZIMAGI_SERVICE_PROCESS[@]}" ]]; then
  # Switch into service execution mode (subprocess)
  export ZIMAGI_SERVICE_INIT=False
  export ZIMAGI_SERVICE_EXEC=True
  export "ZIMAGI_${SERVICE_TYPE^^}_INIT"=False
  export "ZIMAGI_${SERVICE_TYPE^^}_EXEC"=True
  echo ""
  echo "--------------------------------------------------------------------------------"
  echo "================================================================================"
  echo "================================================================================"
  echo "> Starting ${SERVICE_TYPE} service"
  echo ""
  rm -f "/var/local/zimagi/${SERVICE_TYPE}.pid"

  # Launch service process
  "${ZIMAGI_SERVICE_PROCESS[@]}" &
  PROCESS_PID="$!"
  wait "${PROCESS_PID}"
fi
