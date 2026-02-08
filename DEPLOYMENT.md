# Deployment

- Traefik healthchecks verify the container serves HTTP before routing traffic to it
- Docker healthchecks verify the container serves HTTP before Swarm uses the container
- Automatic rollback if the new container fails health checks

## Deploy

Trigger manually from GitHub Actions (`workflow_dispatch`):

## Traefik router

Config lives on the server at `/home/debian/router/`. Redeploy the router with:

```bash
cd /home/debian/router
export $(cat .env | xargs)
docker stack deploy -c docker-compose.yaml traefik
```

## Monitoring

- **Status page:** https://remigirard.github.io/13_empreinte_souffrance/
- **Uptime checks:** every 5 min via GitHub Actions (`.github/workflows/uptime.yaml`)
- **Deploy health monitor:** polls frontend + API every 5s during deploys, auto-rollbacks if service stays down

## Troubleshooting

```bash
docker service ls                                          # list services
docker service ps lheuredescomptes-main_frontend           # check tasks
docker service logs -f lheuredescomptes-main_frontend      # view logs
docker service rollback lheuredescomptes-main_frontend     # manual rollback
```
