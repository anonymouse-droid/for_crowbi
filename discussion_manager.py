import csvReader

discussions = [{"discussionname": 'Mainaccount',
                "padletlink": "https://padlet.com/thilochalas/bz3zhbzqmuzhd1qm",
                "categories": ["First column", "second column", "third", "fourth", "NONE"],
                "catcodes": ["C1", "C2", "C3", "C4", "VOID"],
                "catids": ["section-41504012", "section-41504018", "section-41504020", "section-41504022", "section-52239313"],
                "messages": [],
                "lastmessages": [],
                "newmessagefound": False,
                "commands": [],
                "lastcommands": [],
                "newcommandsfound": False},
                
                {"discussionname": 'Multipadlet?',
                "padletlink": "https://padlet.com/thilochalas/multipadlet",
                "categories": ["Column ONE", "Column TWO", "Column THREE", "Column Four", "NONE"],
                "catcodes": ["C1", "C2", "C3", "C4", "VOID"],
                "catids": ["section-51673453", "section-51673465", "section-51673480", "section-51673489", "section-52239330"],
                "messages": [],
                "lastmessages": [],
                "newmessagefound": False,
                "commands": [],
                "lastcommands": [],
                "newcommandsfound": False},

                {"discussionname": 'Maths expertes Tle',
                "padletlink": "https://padlet.com/julietierno/ksuy76z8oopbxk7e",
                "categories": ["DS, DM et interros", "Progression Prevue", "Chapitre 1 Cours", "Chapitre 2 Cours", "Chapitre 3 Cours", "Chapitre 4 Cours", "Chapitre 5 Cours", "Chapitre 6 Cours", "Chapitre 7 Cours", "Chapitre 1 Exercices", "Chapitre 2 Exercices", "Chapitre 3 Exercices", "Chapitre 4 Exercices", "Chapitre 5 Exercices", "Chapitre 6 Exercices", "Chapitre 7 Exercices", "Images a trier"],
                "catcodes": ["DSDM", "PP", "C1C", "C2C", "C3C", "C4C", "C5C", "C6C", "C7C", "C1EX", "C2EX", "C3EX", "C4EX", "C5EX", "C6EX", "C7EX", "VOID"],
                "catids": ["section-40996450", "section-41017892", "section-40996545", "section-40996706", "section-40996607", "section-40996788", "section-40997070", "section-40996932", "section-40997157", "section-40996563", "section-40996739", "section-40996630", "section-40996816", "section-40997097", "section-40996954", "section-40997172", "section-52235332"],
                "messages": [],
                "lastmessages": [],
                "newmessagefound": False,
                "commands": [],
                "lastcommands": [],
                "newcommandsfound": False}
                ]
###################################################################################################
discussions_a_ajouter = [{"discussionname": 'Mainaccount',
                "padletlink": "https://padlet.com/thilochalas/bz3zhbzqmuzhd1qm",
                "categories": ["First column", "second column", "third", "fourth", "NONE"],
                "catcodes": ["C1", "C2", "C3", "C4", "VOID"],
                "catids": ["section-41504012", "section-41504018", "section-41504020", "section-41504022", "section-52239313"],
                "messages": [],
                "lastmessages": [],
                "newmessagefound": False,
                "commands": [],
                "lastcommands": [],
                "newcommandsfound": False}
                ]
###################################################################################################
def sauvegarder_discussions(discussions):
    csvReader.exportJSON("discussionswithpadlets.json", discussions)
def ajouter_discussions(discussions_a_ajouter):
    discussions = csvReader.importJSON("discussionswithpadlets.json")
    discussions += discussions_a_ajouter
    sauvegarder_discussions(discussions)
def modifier_discussion(nomdiscussion, parametre, nouvelle_valeur):
    
###################################################################################################
#mettre les fonctions ici