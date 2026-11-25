## v1.0.0 (2026-11-25)

### Feat

- Add documentation for Bug B4 – Expired promo code acceptance issue
- Add documentation for Bug B1 – Dépassement du quota VIP
- add unit tests for ApiClient functionality
- export des resultats vers Xray
- **qa**: initialise le projet de tests QA (config, client API, fixtures)
- **fil-rouge**: bugs pédagogiques activables via SEED_BUGS
- **profile**: gestion du profil utilisateur (infos, avatar, mot de passe)

### Fix

- **checkout**: masquer l'icone cadenas aux technologies d'assistance

### Refactor

- comment out flaky marker and sleep in test_full_booking_flow_until_confirmation

### Perf

- test de charge flash sale avec Locust
