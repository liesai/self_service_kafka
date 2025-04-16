# self_service_kafka

+-------------------------------+
| Équipe consommatrice (team2) |
| souhaite consommer un topic  |
+---------------+--------------+
                |
                v
+-------------------------------+
| Création d'une demande YAML  |
| ou via portail interne       |
+---------------+--------------+
                |
                v
+-------------------------------+
| GitHub Action détecte la PR  |
| ou webhook reçoit la demande |
+---------------+--------------+
                |
                v
+-------------------------------+
| Le propriétaire du topic     |
| (ex: team1) est identifié     |
+---------------+--------------+
                |
                v
+-------------------------------+
| team1 est notifié (GitHub,   |
| Slack, email, etc.)          |
+---------------+--------------+
                |
                v
+-------------------------------+
| team1 approuve ou refuse     |
| la demande                   |
+------+---------+-------------+
       |         |
       v         v
    [OK]       [Refus]
     |             |
     v             v
+-------------------+      +------------------------+
| Terraform apply   |      | PR/comment mis à jour |
| crée les ACLs     |      | avec statut refusé    |
+--------+----------+      +------------------------+
         |
         v
+-------------------------------+
| Équipe consommatrice (team2) |
| peut lire et consommer depuis|
| le topic autorisé            |
+-------------------------------+

# Request for subscription 

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
