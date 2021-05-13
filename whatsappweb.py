#Importation des Librairies
import selenium
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os

#Recherche de nouveaux messages parmi les discussions
def findandpickdiscussion(downbuttondiv, newmessagenotif, whatsappdriver, msginputdiv):
    try:
        whatsappdriver.find_element_by_css_selector(downbuttondiv).click()
    except: pass
    try:
        whatsappdriver.find_element_by_css_selector(newmessagenotif).click()
    except: pass
    try:
        text_box = whatsappdriver.find_elements_by_css_selector(msginputdiv)[1]
        text_box.click()
    except: pass

#Identification de la discussion actuelle
def iddiscussion(discussionnamediv, discussions, whatsappdriver):
    currentdiscussion = whatsappdriver.find_element_by_css_selector(discussionnamediv)
    currentdiscussion = currentdiscussion.text
    for discussion in range(len(discussions)):
        if discussions[discussion]["discussionname"] == currentdiscussion:
            return discussion
    return -1


#Recherche et ouverture de la discussion selectionnee
def opendiscussion(nameofdiscussion, wait):
    target = nameofdiscussion
    x_arg = " //span[contains(@title, " + target + ")]"
    target = wait.until(ec.presence_of_element_located((By.XPATH, x_arg)))
    target.click()

#Recherche de nouveaux messages contenant des images
def findnewmessages(whatsappdriver, messages, lastmessages, messagediv):
    lastmessages += messages
    messages = whatsappdriver.find_elements_by_css_selector(messagediv)
    if not messages in lastmessages:
        templist = []
        for message in messages:
            if not message in lastmessages:
                templist.append(message)
        messages = templist
        return messages, True, lastmessages
    else:
        return messages, False, lastmessages

def findnewmessages_V2(whatsappdriver, messages, lastmessages, messagediv):
    messages = whatsappdriver.find_elements_by_css_selector(messagediv)
    newmessages = False
    templist = []
    for message in messages:
        msgid = message.get_attribute("data-id")
        if not msgid in lastmessages:
            newmessages = True
            templist.append(message)
    if templist != []:
        lastmessages += [message.get_attribute("data-id") for message in messages]
    return templist, newmessages, lastmessages

#Extraction du texte contenu sur le message
def readmessagetext(message):
    messagetexts = []
    for i in message:
        try:
            messagetext = i.find_element_by_css_selector("span.copyable-text")
            messagetext = messagetext.find_element_by_css_selector("span")
            messagetexts.append(messagetext.text)
        except:
            messagetext = "No Desc"
            messagetexts.append(messagetext)
    return messagetexts

#Extraction de l'heure d'envoi du message
def findmessagetime(message, spanname):
    messagetimes = []
    for i in message:
        timeofmessage = i.find_element_by_css_selector(spanname)
        messagetimes.append(timeofmessage.text)
    return messagetimes

#Recherche des messages contenant une image allant sur le padlet
def findpadletsends(messages):
    indexes = []
    for i in range(len(messages)):
        endstr = 10
        if len(messages[i]) < endstr:
            endstr = len(messages[i])
        if ("!padlet" in messages[i][0:endstr]) or ("! padlet" in messages[i][0:endstr]):
            indexes.append(i)
    return indexes

#Telechargement de l'image
def downloadimage(message, whatsappdriver, imgbtndiv, actbtndiv):
    imagebutton = message.find_element_by_css_selector(imgbtndiv)
    imagebutton.click()
    actionbuttons = whatsappdriver.find_element_by_css_selector(actbtndiv)
    downloadbutton = actionbuttons.find_element_by_xpath("//div[@title='Télécharger']")
    downloadbutton.click()
    closebutton = actionbuttons.find_element_by_xpath("//div[@title='Fermer']")
    closebutton.click()
    time.sleep(5)

#Envoi d'un message dans la discussion whatsapp
def sendmessage(text, whatsappdriver, msginputdiv, msginput):
    text_box = whatsappdriver.find_elements_by_css_selector(msginputdiv)[1]
    text_box = text_box.find_element_by_css_selector(msginput)
    text_box.send_keys(text)
    text_box.send_keys(Keys.RETURN)

#Recherche de nouveaux messages contenant des commandes
def findnewmessagesforcommands(whatsappdriver,messages, lastmessages, msgdiv):
    lastmessages += messages
    messages = whatsappdriver.find_elements_by_css_selector(msgdiv)
    if not messages in lastmessages:
        templist = []
        for message in messages:
            if not message in lastmessages:
                templist.append(message)
        messages = templist
        return messages, True, lastmessages
    else:
        return messages, False, lastmessages

def findnewmessagesforcommands_V2(whatsappdriver, messages, lastmessages, lastimgmessages, messagediv, messagediv2):
    messages = whatsappdriver.find_elements_by_css_selector(messagediv)
    newmessages = False
    templist = []
    for message in messages:
        msgid = message.get_attribute("data-id")
        if (not msgid in lastmessages) and (not msgid in lastimgmessages):
            newmessages = True
            templist.append(message)
    if templist != []:
        lastmessages += [message.get_attribute("data-id") for message in messages if not message.get_attribute("data-id") in lastmessages]
    tmplist = []
    for command in templist:
        try:
            tmplist.append(command.find_element_by_css_selector(messagediv2))
        except: pass
    return tmplist, newmessages, lastmessages


#Traitement des reponses aux commandes
def executecommands(commandtexts, commandindexes):
    answers = []
    for i in commandindexes:
        if "instructions" in commandtexts[i] or "help" in commandtexts[i] or "aide" in commandtexts[i]:
            reply = "Bonjour, bienvenue dans le guide d'utilisation d'autopadlet. Ce systeme permet de transferer automatiquement les photos postées sur ce groupe whatsapp sur le padlet. Liste des commandes possibles: [!padlet syntaxe: instructions pour qu'une image soit transferée automatiquement], [!padlet liste catégories: liste des catégories du padlet], [!padlet lien padlet: renvoie le lien pour aller sur le padlet], [!padlet statut: renvoie le statut d'autopadlet et l'heure], [!padlet codesource: renvoie le lien vers le code source d'autopadlet"
        elif "syntaxe" in commandtexts[i] or "transfert" in commandtexts[i]:
            reply = "Afin qu'une photo soit transférée, suivez les instructions qui suivent: 1. Choisissez la photo a mettre sur whatsapp 2. Dans la description de la photo, écrivez en respectant la syntaxe: !padlet {Code correspondant a la catégorie dans le padlet (envoyer la commande \"!padlet liste catégories' pour avoir la liste des catégories)} {Titre a donner a l'image} ; {description a donner a l'image}\" (remplacer le texte dans les {} par ce qu'il faut et ne recopiez pas les {}) Exemple: !padlet C1EX Titre de l'image;Description de l'image"
        elif "liste catégories" in commandtexts[i]:
            reply = "Autopadlet: Bonjour, voici la liste des catégories dans le padlet: C1, C2, C3, C4"
        elif "lien padlet" in commandtexts[i]:
            reply = "Autopadlet: Bonjour, voici le lien vers le padlet: https://padlet.com/thilochalas/bz3zhbzqmuzhd1qm"
        elif "kill_autopadlet" in commandtexts[i]:
            reply = "(!padlet kill) Autopadlet: Killing the autopadlet process"
        elif "statut" in commandtexts[i]:
            reply = "Autopadlet est en ligne: " + time.strftime("%X %x")
        elif "codesource" in commandtexts[i]:
            reply = "Voici le lien vers le repositoire github avec le code source: https://github.com/ct"
        else:
            reply = "Cette commande n'existe pas. Envoyez !padlet aide pour avoir de l'aide."
        answers.append(reply)
    return answers

def executecommands_V2(commandtexts, commandindexes, categories, catcodes, lien_padlet):
    answers = []
    for i in commandindexes:
        if "instructions" in commandtexts[i] or "help" in commandtexts[i] or "aide" in commandtexts[i]:
            reply = "Bonjour, bienvenue dans le guide d'utilisation d'autopadlet. Ce systeme permet de transferer automatiquement les photos postées sur ce groupe whatsapp sur le padlet. Liste des commandes possibles: [!padlet syntaxe: instructions pour qu'une image soit transferée automatiquement], [!padlet liste catégories: liste des catégories du padlet], [!padlet lien padlet: renvoie le lien pour aller sur le padlet], [!padlet statut: renvoie le statut d'autopadlet et l'heure], [!padlet codesource: renvoie le lien vers le code source d'autopadlet]"
        elif "syntaxe" in commandtexts[i] or "transfert" in commandtexts[i]:
            reply = "Afin qu'une photo soit transférée, suivez les instructions qui suivent: 1. Choisissez la photo a mettre sur whatsapp 2. Dans la description de la photo, écrivez en respectant la syntaxe: !padlet {Code correspondant a la catégorie dans le padlet (envoyer la commande \"!padlet liste catégories' pour avoir la liste des catégories)} {Titre a donner a l'image} ; {description a donner a l'image}\" (remplacer le texte dans les {} par ce qu'il faut et ne recopiez pas les {}) Exemple: !padlet C1EX Titre de l'image;Description de l'image"
        elif "liste catégories" in commandtexts[i]:
            reply = "Autopadlet: Bonjour, voici la liste des catégories dans le padlet (categorie: code correspondant): " + str([categories[i]+": "+catcodes[i] for i in range(len(categories))])
        elif "lien padlet" in commandtexts[i]:
            reply = "Autopadlet: Bonjour, voici le lien vers le padlet: " + lien_padlet
        elif "kill_autopadlet" in commandtexts[i]:
            reply = "(!padlet kill) Autopadlet: Killing the autopadlet process"
        elif "statut" in commandtexts[i]:
            reply = "Autopadlet est en ligne: " + time.strftime("%X %x")
        elif "codesource" in commandtexts[i]:
            reply = "Voici le lien vers le repositoire github avec le code source: https://gitet"
        else:
            reply = "Cette commande n'existe pas. Envoyez !padlet aide pour avoir de l'aide."
        answers.append(reply)
    return answers

#Ajout de discussions (Autopadlet V3)
def checkifignore(current_discussion, knowndiscussions, commandtexts):
    for discussion in knowndiscussions:
        if discussion["discussionname"] == current_discussion and discussion["configured"] == True:
            for text in commandtexts:
                if "!padlet configurer" in text:
                    return False
            return True
    return False

def checkifnewdiscussion(current_discussion, knowndiscussions):
    for discussion in knowndiscussions:
        if discussion["discussionname"] == current_discussion:
            return knowndiscussions
    knowndiscussions.append({"discussionname": current_discussion, "configured": False})
    csvReader.exportJSON("alldiscussions.json", knowndiscussions)
    return knowndiscussions

def finddiscussionindex(current_discussion, knowndiscussions):
    for i in range(len(knowndiscussions)):
        if knowndiscussions[i]["discussionname"] == current_discussion:
            return i
    return -1

def checkwhichcommand(commandtexts, discussionindex, knowndiscussions):
    for text in commandtexts:
        if "!padlet ignorer" in text:
            knowndiscussions[discussionindex]["configured"] = True
            send_info_message = False
            go_to_configure = "None"
            return send_info_message, go_to_configure, knowndiscussions
        elif "!padlet configurer" in text and "lien" in text:
            knowndiscussions[discussionindex]["configured"] = False
            send_info_message = False
            go_to_configure = "lien"
        elif "!padlet configurer" in text and "categories" in text:
            knowndiscussions[discussionindex]["configured"] = False
            send_info_message = False
            go_to_configure = "categories"
        elif "!padlet configurer" in text and "codes categories" in text:
            knowndiscussions[discussionindex]["configured"] = False
            send_info_message = False
            go_to_configure = "catcodes"
        elif "!padlet configurer" in text and "lien" in text:
            knowndiscussions[discussionindex]["configured"] = False
            send_info_message = False
            go_to_configure = "lien"
