
# Kafka Access & Topic Creation Platform

Ce dépôt contient deux modules :

1. 📦 **Création de topics Kafka** avec validation, nomenclature, quotas, et ACLs automatisés.
2. 🔐 **Gestion des abonnements** à des topics existants avec validation par les propriétaires.

---

## 🧭 Flowchart 1 : Création de topics Kafka

```text
[Étape 1] 🧑‍💻 Développeur soumet une demande
   |
   |--> via PR GitHub (ajout d’un .tf) 
   |        OU via portail interne (qui crée une PR)
   ↓
[Étape 2] 🧠 GitHub Action - Validation automatique
   |
   |--> Vérifie nomenclature du topic
   |--> Vérifie quota par équipe (via API Confluent)
   |--> Vérifie partitions & retention < limites
   |--> Vérifie cohérence du Service Account
   ↓
[Étape 3] ✅ Validation manuelle de la PR (optionnel)
   |
   |--> Reviewer équipe ou ops valide que tout est conforme
   ↓
[Étape 4] 🚀 GitHub Action - Déploiement
   |
   |--> terraform init / plan / apply
   |--> Création du topic Kafka (Confluent Cloud)
   |--> Création des ACLs liées à l’équipe
   ↓
[Étape 5] 🔒 Contrôle des accès
   |
   |--> Seul le Service Account d’équipe peut :
   |       - écrire
   |       - lire
   |       - consommer depuis consumer group dédié
   ↓
[Étape 6] 📊 Monitoring & Audit
   |
   |--> Logs Confluent Cloud ingérés dans Splunk/Elasticsearch
   |--> Dashboards : par équipe, par topic, volumétrie, erreurs
   ↓
[Étape 7] 🔁 Maintien en conditions opérationnelles
   |
   |--> PRs suivantes pour modifier retention / partitions
   |--> Reset offset si demandé (via autre PR ou portail)
```

---

## 🔁 Flowchart 2 : Abonnement à un topic existant

```text
+-------------------------------+
| 👩‍💻 Équipe consommatrice     |
| veut s’abonner à un topic     |
+---------------+--------------+
                |
                v
+-------------------------------+
| Crée une PR avec un fichier  |
| subscriptions/request.yaml   |
+---------------+--------------+
                |
                v
+-------------------------------+
| GitHub Action est déclenchée |
| (validate-subscription.yml)  |
+---------------+--------------+
                |
                v
+-------------------------------+
| Script lit :                 |
| - request.yaml               |
| - catalog/topics.yaml        |
+---------------+--------------+
                |
                v
+-------------------------------+
| Vérifie que l’acteur GitHub  |
| (ex: alice) fait partie des  |
| approvers du topic           |
+--------+----------+----------+
         |          |
         | ✅ Oui    | ❌ Non
         v          v
+---------------+  +-----------------------------+
| Terraform plan|  | Rejet de la PR              |
| & apply ACLs  |  | (non autorisé à approuver)  |
+-------+-------+  +-----------------------------+
        |
        v
+-------------------------------+
| Les ACLs sont déployées :     |
| - READ sur le topic           |
| - READ sur le consumer group  |
+---------------+--------------+
                |
                v
+-------------------------------+
| 🔍 Les logs sont audités via |
| Splunk / Elastic              |
+-------------------------------+
```
