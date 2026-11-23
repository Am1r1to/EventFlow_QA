# Bug B1 – Dépassement du quota VIP

Le test `test_rm1_cannot_order_more_than_available_stock` échoue.

La requête SQL retourne :

- **Catégorie :** VIP
- **Quota :** 3
- **Réservations :** 4

On constate que 4 billets VIP ont été réservés alors que le quota maximum est de 3.

Le système a donc accepté une commande dépassant le stock disponible.

**Dépassement constaté :** 1 billet VIP.

**Prompt (Pdb) : interrogation de la base**

## Origine du bug

**Fichier :** `backend/app/routers/orders.py`

**Fonction :** `create_order`

**Ligne :** 99

```python
if item.quantity > category_available(db, category) and not settings.seed_bugs
```

**Analyse :** Le contrôle de stock est ignoré et l'API accepte la commande.

**Fichier :** `backend/app/services.py`

**Fonction :** `category_available`

**Ligne :** 47

```python
return max(0, category.quota - category_sold(db, category.id))
```

**Analyse :** Le `max(0, ...)` empêche le stock affiché de devenir négatif. Avec un quota de 3 et 4 réservations, le calcul donne 0 place restante au lieu de -1.

## Conclusion

Le bug B1 permet à l'API d'accepter plus de billets que le quota autorisé, car le contrôle RM1 est désactivé en mode bug. La base confirme 4 réservations pour 3 places VIP. Le stock affiché reste à 0 grâce à `max(0, ...)`.