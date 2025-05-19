# 🗒️ Changelog - Manutan Sport Center

## 📖 Objectif du changelog
Ce changelog est destiné à documenter les évolutions et mises à jour de l'application Manutan Sport Center. Il fournit une vue d'ensemble des fonctionnalités ajoutées, des corrections de bugs et des améliorations de performance, permettant à l'équipe de développement et aux utilisateurs d'avoir une vision claire des modifications effectuées au fil du temps.

## Version 0.1 - 🚀 Création du projet
- 🎉 Création de l'application (Flask, HTML Templates, CSS, JS)
- 📡 Implémentation de la logique de scan des badges (py122u)
- 🏠 Création de la page d'accueil (Index)
- 🔑 Gestion de la connexion si le badge est reconnu
- 📊 Création de la page Dashboard
- 🏅 Création de la logique de récupération des sports (ETA.json)
- 📝 Création de la page Register
- 👤 Ajout de la création de compte (user.json)
- 👋 Création de la page Greeting

---

## Version 0.2 - 🔄 Mises à jour fonctionnelles - MAJEUR
- 🛠️ Ajout de fonctions pour le bon fonctionnement du code
- 👥 Création de la gestion de rôle (User, Coach)
- 📋 Création de la page Dashboard Coach (fonctionnelle)
- ✏️ Création de la logique de modification d’utilisateurs par les Coaches

---

## Version 0.3 - 🌟 Mises à jour fonctionnelles
- 🛠️ Ajout de fonctions pour le bon fonctionnement du code
- 📈 Mises à jour graphiques de la page Dashboard Coach
- 💬 Création de l'affichage de messages d'information
- 🛠️ Création de la possibilité de créer, modifier et supprimer des messages par les coaches
- 🚫 Création de la possibilité de rendre un sport indisponible par les coaches
- 🔄 Mise à jour de l'affichage du Dashboard pour présenter les sports correctement
---

## Version 0.4 - ⚙️ Mises à jour suite à la réunion du 17/02/25
- 🛠️ Ajout de fonctions pour le bon fonctionnement du code
- 🔄 Correction du bug d'update/ajout de Messages
- 🔄 Correction du bug d'update de Sport
- 📈 Ajout de la possibilité de sélectionner plusieurs sports
- 📈 Ajout de la catégorie "Sport en Autonomie" contenant "Course à pied", "Musculation" et "Cardio"
- 📢 Affichage du message d’information pendant le Greeting pour les utilisateurs n'ayant pas payé le Centre Sportif
- ✏️​ Permettre au coach de renseigner une séance pour un utilisateur
- 📈 Création du Dashboard (PowerBI)

### Informations :
Les emails et le dashboard en direct ne peuvent pes être réalisé actuellement. Ces tâches requiert d'avoir un Serveur à disposition pour envoyer des mail (SMTP) et stocker un des fichier pour les récupérer en direct dans un PowerBI. -> Voir avec l'équipe Infra si on peut utiliser un outils externe en attendant (Resend) pour réaliser les envois de mail. Le Dashboard est quand à lui déjà réalisé, mais attend d'avoir des données consultable en temps réel pour afficher des statistique instantanées.

## 🚧 Implémentations à venir 
- [x] 💬 Affichage de messages d'information
- [x] 🚫 Possibilité de rendre un sport indisponible par les coaches
- [x] 🐛 Corriger le bug de modification de messages
- [x] 🏷️ Corriger le bug de disponibilité des sports si deux itérations identiques dans la même journée 
- [x] ✅​ Cocher plusieurs sports 
- [x] 👟​ Muscu, Cardio, Course à mettre à chaque fois
- [x] 📢 Affichage du message d’information pendant le Greeting pour les utilisateurs n'ayant pas payé le centre (Obtenir le fichier pour faire l'ajout)
- [x] ✏️​ Permettre au coach de renseigner une séance pour un utilisateur
- [ ] 📮 Envoyer des mails (Coach manquant, fermé etc...) 
- [ ] 📈 Accéder au dashboard (équipe, PowerBI, analyse de stats en direct)
- [ ] ⚙️ Créer une vue de modification des sports pour les Coaches
- [ ] 🌐 Passer sous API + Node pour avoir un rendu plus propre