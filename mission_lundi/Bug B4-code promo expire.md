
# B4 — Le code promo expiré est accepté

## Q1 — Test UI

Le test `test_expired_promo_code_shows_error` attend l'affichage du message `Promo code expired`.

Erreur pytest :
```text
AssertionError: Locator expected to have text 'Promo code expired'
Actual value: None
Error: element(s) not found
```

## Q2 — Reproductibilité

Le test échoue de la même manière lors de trois exécutions successives. Le défaut est reproductible et n'est pas un test instable (*flaky test*).

## Q3 — Front ou back ?

Test API : `test_rm4_promo_codes[EXPIRED]`

- Statut obtenu : **HTTP 201** (commande créée).
- Statut attendu : **HTTP 400** (code promo expiré refusé).

**Conclusion :** le back-end accepte à tort le code promo expiré.

## Q4 et Q5 — Trace Playwright

La requête `POST /api/orders` envoie le code promo `EXPIRED`.

Résultat :
- Statut de la commande : `pending`.
- `total_cents` : 2975, soit 29,75 €.
- Prix initial : 35 €.
- Remise appliquée : 5,25 € (15 %).
- Page suivante : `/checkout/41`.
- Console : aucune erreur JavaScript, uniquement des messages informatifs liés à Vite et React.

## Q6 — Vérification SQL et cause du bug

La base de données confirme :

| Champ | Valeur |
|---|---|
| Code | `EXPIRED` |
| Remise | 15 % |
| Date d'expiration | 22/11/2026 à 11:15:16 |

Le code était donc expiré lors du test du 23/11/2026.

**Cause identifiée :**
- Fichier : `backend/app/routers/orders.py`
- Fonction : `_validate_promo`
- Ligne : **34**

La condition `and not settings.seed_bugs` désactive la vérification lorsque `settings.seed_bugs = True`.

La date d'expiration n'est donc plus contrôlée et l'API accepte le code promo.

## Conclusion

Le bug B4 se situe côté back-end. Un code promo expiré est accepté, une remise de 15 % est appliquée et une commande est créée, au lieu de retourner HTTP 400 et d'afficher `Promo code expired`.
