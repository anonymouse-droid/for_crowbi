"""Ceci est le code principal d'autopadlet a executer dans le terminal. Veuillez vous 
referer au readme du repositoire github pour plus d'informations """
#Importation des Librairies et elements associes
#Selenium
import selenium
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
#Autres
import os
import time
import pyautogui
#Custom
import whatsappweb
import padlet
import csvReader

#Liens vers les pages internet
whatsapplink = "https://web.whatsapp.com/"
padletlink = "https://padlet.com/titicha/bz3zhbzqmuzhd1qm"

#Nom de la discussion whatsapp
discussionname = '"Mainaccount"'

#Variables servant a la lecture des messages dans whatsapp web
messages = []
lastmessages = []
newmessagefound = False

commands = []
lastcommands = []
newcommandsfound = False

#Noms des classes des .div de whatsapp web
internetstatusdiv = "div." + "pcVTC" 
imgmsgdiv = "div." + "j9c-4" 
imgpicdiv = "div." + "_1mTER" 
actionbuttonsdiv = "div." + "_1RLgD" 
msginputdiv = "div." + "_2HE1Z" 
msginputfield = "div." + "_1awRl" 
normmsgdiv = "div." + "_2tbXF" 
msgtimespan = "span." + "_2JNr-"

#Categories du padlet
categories = ["First column", "second column", "third", "fourth"]
catcodes = ["C1", "C2", "C3", "C4"]
catids = ["section-41504012", "section-41504018", "section-41504020", "section-41504022"]

#Autres
killtaskrequested = False
recoveredcrashes = 0

#Fonction servant a demarrer et initialiser les pages web...
def initialisation(whatsapplink, discussionname, padletlink, commands, lastcommands):
    #Ouverture de la liste des images deja envoyees sur le padlet
    uploadlog = csvReader.importCSV("uploadedimages.csv")

    #Recuperation du profil chrome
    #(Ligne suivante): Remplacer le chemin (c.f. README)
    os.system("rm -r /home/pi/Desktop/Projet_Transfert_Auto_Padlet/chromedata/Default")
    #(Ligne suivante): Remplacer les chemin (c.f. README)
    os.system("cp -r /home/pi/.config/chromium/Default /home/pi/Desktop/Projet_Transfert_Auto_Padlet/chromedata")

    #Reglage des options de chrome
    coptions = webdriver.ChromeOptions()
    #(Ligne suivante): Remplacer les chemin (c.f. README)
    coptions.add_argument("--user-data-dir=/home/pi/Desktop/Projet_Transfert_Auto_Padlet/chromedata")

    #Ouverture de whatsapp web et navigetion jusqu'a la discussion choisie
    #(Ligne suivante): Remplacer les chemin (c.f. README)
    whatsappdriver = selenium.webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver", options=coptions)
    whatsappdriver.get(whatsapplink)
    time.sleep(5)
    wait = WebDriverWait(whatsappdriver, 600)
    whatsappweb.opendiscussion(discussionname, wait)

    #Ouverture du padlet
    #(Ligne suivante): Remplacer les chemin (c.f. README)
    padletdriver = selenium.webdriver.Chrome(os.path.expanduser("/usr/lib/chromium-browser/chromedriver"))
    padletdriver.get(padletlink)
    commands, newcommandsfound, lastcommands = whatsappweb.findnewmessagesforcommands(whatsappdriver, commands, lastcommands, normmsgdiv)
    return uploadlog,whatsappdriver,padletdriver,commands,newcommandsfound,lastcommands

#Initialisation d'Autopadlet
uploadlog,whatsappdriver,padletdriver,commands,newcommandsfound,lastcommands = initialisation(whatsapplink, discussionname, padletlink, commands, lastcommands)

print("Enter loop")
#Boucle principale d'Autopadlet
while True :
    #Le try/except sert ici pour la gestion des crashs pouvant se produire
    try:
        #Recherche de noveaux messages comportant des images
        messages, newmessagefound, lastmessages = whatsappweb.findnewmessages(whatsappdriver, messages, lastmessages, imgmsgdiv)

        #Instructions a executer si un nouveau message est arrive
        if newmessagefound and messages != []:
            print("New message(s) found") 
            
            #Traitement du message et extraction des informations
            newmessagefound = False
            messagetexts = whatsappweb.readmessagetext(messages)
            messagetimes = whatsappweb.findmessagetime(messages, msgtimespan)
            padletsends = whatsappweb.findpadletsends(messagetexts)
            categorized = padlet.setimagecategories(messagetexts, padletsends, categories, catcodes, catids)
            messages_with_data = padlet.setmessagedata(messages, categorized, messagetexts, messagetimes, catcodes)
            print(messages_with_data)

            #Transfert de l'image sur le padlet
            for message in messages_with_data: #On parcoure les messages detectes
                if message["category_id"] != "ERR": #Verification pour savoir si le message a une categorie
                    if padlet.checkuploads(message, uploadlog): #Verification pour ne pas envoyer une deuxieme fois la meme image sur le padlet
                        uploadlog.append({"uploaddata": (message["category_name"] + message["Title"] + message["Description"] + message["Time"])})
                        padlet.updateuploadlog(uploadlog)
                        whatsappweb.downloadimage(message["message"], whatsappdriver, imgpicdiv, actionbuttonsdiv)
                        padlet.postonpadlet(message, padletdriver)
                        whatsappweb.sendmessage(('''L'image"''' + message["Title"] + '" est sur le padlet'), whatsappdriver, msginputdiv, msginputfield)
                else:
                    whatsappweb.sendmessage(("Erreur dans le code de catégorie padlet"), whatsappdriver, msginputdiv, msginputfield)      
    

        #Detection de nouveaux messages contenant des commandes
        commands, newcommandsfound, lastcommands = whatsappweb.findnewmessagesforcommands(whatsappdriver, commands, lastcommands, normmsgdiv)

        #Instructions a executer si il y a de nouvelles commandes
        if newcommandsfound and commands != []:
            print("New commands found")

            #Traitement de la commande et extraction des informations
            newcommandsfound = False
            commandtexts = whatsappweb.readmessagetext(commands)
            commandstoexecute = whatsappweb.findpadletsends(commandtexts)
            responses = whatsappweb.executecommands(commandtexts, commandstoexecute)
            commandtexts, commandstoexecute = [],[]

            #Envoi des reponses a la commande
            for text in responses:
                #Envoi de la reponse
                whatsappweb.sendmessage(text, whatsappdriver, msginputdiv, msginputfield)

                #Instructions si le killcode est active
                if text == "Autopadlet: Killing the autopadlet process":
                    killtaskrequested = True
                    time.sleep(5)
                    print("AUTOPADLET PROCESS TERMINATED")
                    whatsappdriver.quit()
                    padletdriver.quit()
                    quit()
                    exit()
                    break
        

        #Detection d'une perte de connexion internet
        try:
            internetloss = whatsappdriver.find_element_by_css_selector(internetstatusdiv)
            internetloss = internetloss.text
            if internetloss != "L'ordinateur n'est pas connecté":
                raise Exception("Not lost")
            print("INTERNET: CONNEXION LOST")

            #Attente du retour de la connexion internet
            while "pas connecté" in internetloss:
                #print("INTERNET: WAITING FOR RESPONSE")
                time.sleep(1)
                try:
                    internetloss = whatsappdriver.find_element_by_css_selector(internetstatusdiv)
                    internetloss = internetloss.text
                except:
                    internetloss = " "
            time.sleep(10)
            commands, newcommandsfound, lastcommands = whatsappweb.findnewmessagesforcommands(whatsappdriver, commands, lastcommands, normmsgdiv)
        except:
            #print("Internet connexion is stable")
            pass
        time.sleep(5)
    except:
        #Quitter le programme si le killcode est active
        if killtaskrequested:
            quit()

        #Retablissement automatique (en cas de crash)
        print("AUTOPADLET: FATAL ERROR OCCURED")
        print("AUTOPADLET: RESTARTING")
        for i in range(5):
            pyautogui.press("esc")
        whatsappdriver.quit()
        padletdriver.quit()
        uploadlog,whatsappdriver,padletdriver,commands,newcommandsfound,lastcommands = initialisation(whatsapplink, discussionname, padletlink, commands, lastcommands)
        recoveredcrashes += 1
        print("AUTOPADLET: RECOVERED CRASHES = "+str(recoveredcrashes))
