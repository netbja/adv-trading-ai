#!/bin/sh

echo "[INFO] Backup PostgreSQL: $POSTGRES_DB from host 'postgres'"

# Nom du fichier
BACKUP_FILE="/backup/${POSTGRES_DB}_$(date +%Y%m%d_%H%M%S).sql"

# Dump
pg_dump -h postgres -U "$POSTGRES_USER" "$POSTGRES_DB" > "$BACKUP_FILE"

# Nettoyage
find /backup -name '*.sql' -mtime +"${BACKUP_RETENTION_DAYS:-7}" -delete

echo "[INFO] Backup terminé : $BACKUP_FILE"
