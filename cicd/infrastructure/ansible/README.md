# Ansible

## Install

Initial install
```bash
# create and use python virtual environment
python3 -m venv venv
source venv/bin/activate
# install
pip install -r requirements.txt

# check install
ansible --version
```

If you already installed, you just need :
```bash
source venv/bin/activate
```

## Authentification

The path of the ssh certificate used it on `./inventory.yaml`, you need copy the ssh certificate of the server on this path.

## Usage

```bash
ansible-playbook -i inventory.yaml ./playbooks/installDocker.yaml 
ansible-playbook -i inventory.yaml ./playbooks/initJoinSwarmV2.yaml
ansible-playbook -i inventory.yaml ./playbooks/runDockerRepositoryWithCerts.yaml
```

