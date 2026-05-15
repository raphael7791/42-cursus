# Commandes de test avant de push

## 1. Tester tous les scripts

```bash
python3 ft_alembic_0.py
python3 ft_alembic_1.py
python3 ft_alembic_2.py
python3 ft_alembic_3.py
python3 ft_alembic_4.py          # doit crash avec AttributeError (normal)
python3 ft_alembic_5.py
python3 ft_distillation_0.py
python3 ft_distillation_1.py
python3 ft_transmutation_0.py
python3 ft_transmutation_1.py
python3 ft_transmutation_2.py
python3 ft_kaboom_0.py
python3 ft_kaboom_1.py            # doit crash avec ImportError (normal)
```

## 2. flake8 (0 erreur attendu)

```bash
python3 -m flake8 . --exclude=__pycache__
```

## 3. mypy (seule erreur = ft_alembic_4, c'est normal)

```bash
python3 -m mypy . --exclude=__pycache__
```

## 4. Nettoyer les __pycache__ avant de push

```bash
find . -type d -name __pycache__ -exec rm -rf {} +
```
