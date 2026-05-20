# Python-8 — Commandes de test sur ordi 42

## Installation de virtualenv (une seule fois)

```bash
python3 -m pip install virtualenv
```

## Creer et activer le venv

```bash
cd ~/Python-8
python3 -m virtualenv matrix_env
source matrix_env/bin/activate
```

Tu dois voir `(matrix_env)` au debut de ta ligne.

---

## Ex0 — construct.py

### Test hors venv (AVANT d'activer le venv)

```bash
python3 ex0/construct.py
```

Resultat attendu : `MATRIX STATUS: You're still plugged in`

### Test dans le venv

```bash
source matrix_env/bin/activate
python3 ex0/construct.py
```

Resultat attendu : `MATRIX STATUS: Welcome to the construct`

---

## Ex1 — loading.py

### Installer les dependances (dans le venv)

```bash
source matrix_env/bin/activate
pip install -r ex1/requirements.txt
```

### Lancer le programme

```bash
python3 ex1/loading.py
```

Resultat attendu : analyse de 1000 data points + `matrix_analysis.png` genere.

### Test SANS dependances (dans un venv vierge)

```bash
deactivate
python3 -m virtualenv test_venv
source test_venv/bin/activate
python3 ex1/loading.py
```

Resultat attendu : message `[MISSING]` + instructions d'installation.

Puis nettoyer :

```bash
deactivate
rm -rf test_venv
```

---

## Ex2 — oracle.py

### Installer python-dotenv (dans le venv)

```bash
source matrix_env/bin/activate
pip install python-dotenv
```

### Test 1 : sans fichier .env

```bash
python3 ex2/oracle.py
```

Resultat attendu : `[NOT CONFIGURED]` pour DATABASE_URL, API_KEY, ZION_ENDPOINT.

### Test 2 : avec fichier .env

```bash
cp ex2/.env.example ex2/.env
python3 ex2/oracle.py
```

Resultat attendu : `Connected to local instance`, `Authenticated`, `Online`.

### Test 3 : avec variables d'environnement (mode production)

```bash
MATRIX_MODE=production API_KEY=secret123 DATABASE_URL=postgres://prod:5432/db LOG_LEVEL=WARNING ZION_ENDPOINT=https://zion.net python3 ex2/oracle.py
```

Resultat attendu : `Mode: production`, `Connected to production instance`.

### Nettoyer le .env apres les tests

```bash
rm ex2/.env
```

---

## Verification flake8 + mypy

```bash
flake8 ex0/construct.py ex1/loading.py ex2/oracle.py
mypy ex0/construct.py ex2/oracle.py
mypy ex1/loading.py
```

- flake8 : 0 erreurs
- mypy ex0 + ex2 : 0 erreurs
- mypy ex1 : erreurs d'import seulement (autorise par le sujet)

---

## Nettoyer avant de push

```bash
deactivate
rm -rf matrix_env
rm -f ex2/.env
rm -f matrix_analysis.png
```

Ne jamais push : matrix_env/, .env, matrix_analysis.png, __pycache__/
