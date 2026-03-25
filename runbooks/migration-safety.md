# Migration safety runbook

- expand before contract
- dual-read or dual-write only with a removal plan
- verify backfills with explicit queries
- cut over only when old and new paths agree
- keep rollback instructions close to the migration note
