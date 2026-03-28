# External Access Overlay

Este overlay configura o frontend para acesso externo ao backend.

## Uso

### Com kubectl port-forward (desenvolvimento):

```bash
# Terminal 1: Port-forward do backend
kubectl port-forward svc/clawdevs-panel-backend 8000:8000

# Terminal 2: Aplica o overlay
kubectl apply -k overlays/external
```

### Com minikube tunnel:

```bash
# Inicie o tunnel (requer terminal aberto)
minikube tunnel

# Atualize o ConfigMap com a URL correta
kubectl create configmap external-config --from-literal=API_URL=http://127.0.0.1:31881 -n default -o yaml --dry-run=client | kubectl apply -f -
```

### URL Padrão

O valor padrão é `http://localhost:8000`, que funciona com:

```bash
kubectl port-forward svc/clawdevs-panel-backend 8000:8000
```
