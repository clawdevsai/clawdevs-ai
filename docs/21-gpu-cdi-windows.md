# CDI GPU Setup (Windows + Docker Desktop + WSL2)

Objetivo: habilitar CDI para que `--gpus nvidia.com` funcione no Docker e no Minikube (`make up-cdi`).

## 1) Validar baseline da GPU no host

No PowerShell:

```powershell
nvidia-smi
docker run --rm --gpus all nvidia/cuda:12.3.2-base-ubuntu22.04 nvidia-smi
```

Se isso falhar, pare aqui e corrija driver/Docker Desktop GPU.

## 2) Verificar distros WSL2

```powershell
wsl -l -v
```

Confirme uma distro Linux ativa (ex.: `Ubuntu`) para instalar toolkit.

## 3) Instalar NVIDIA Container Toolkit na distro Linux

Exemplo para Ubuntu:

```bash
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey \
  | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg

curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
  | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' \
  | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
```

## 4) Gerar e validar CDI

Na mesma distro:

```bash
sudo nvidia-ctk cdi generate --output=/etc/cdi/nvidia.yaml
sudo nvidia-ctk cdi list
```

Esperado: entradas `nvidia.com/gpu=...`.

## 5) Reiniciar Docker Desktop

No PowerShell:

```powershell
wsl --shutdown
```

Feche/reabra Docker Desktop.

## 6) Validar CDI no Docker

```powershell
docker run --rm --device nvidia.com/gpu=all nvidia/cuda:12.3.2-base-ubuntu22.04 nvidia-smi
```

Se ainda falhar com `unresolvable CDI devices`, CDI não está visível para o daemon Docker Desktop.

## 7) Subir cluster com CDI

```powershell
make up-cdi
make gpu-debug
make gpu-smoke
```

Esperado em `make gpu-debug`: `GPU` diferente de `<none>` no node.

## Observacoes

- `nvidia-device-plugin` em `Running` não garante GPU disponível: o node precisa anunciar `nvidia.com/gpu`.
- No projeto atual, apenas `ollama` pede GPU; `openclaw-gateway` roda em CPU e consome Ollama pela rede.
