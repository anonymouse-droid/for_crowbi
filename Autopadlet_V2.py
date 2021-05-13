"""Ceci est le code principal d'autopadlet a executer dans le terminal. Veuillez vous 
referer au readme du repositoire github pour plus d'informations"""
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

#NO CHANGE
whatsapplink = "https://web.whatsapp.com/"

internetstatusdiv = "div." + "_1wQdF"#"pcVTC" 
imgmsgdiv2 = "div." + "_1B_Jc"#"_2FNAC"
imgmsgdiv = "div." + "gZ4ft"#"j9c-4" 
imgpicdiv = "div." + "_2MfUK"#"_1mTER" 
actionbuttonsdiv = "div." + "_1ljzS"#"_1RLgD" 
msginputdiv = "div." + "_1JAUF"#"_2HE1Z" 
msginputfield = "div." + "_2_1wd"#"_1awRl" 
normmsgdiv = "div." + "_24wtQ" 
normmsgdiv2 = "div." + "GDTQm" 
msgtimespan = "span." + "_17Osw"

downbuttondiv = "div." + "_2wFt8"
newmessagenotif = "div." + "_2TiQe"
discussionnamediv = "div." + "_2KQyF"


killtaskrequested = False
recoveredcrashes = 0

#NEW
padletlink = ""
discussionname = ""
messages = []
lastmessages = []
newmessagefound = False
commands = []
lastcommands = []
newcommandsfound = False
categories = []
catcodes = []
catids = []
uploadlog = {}
#CHANGES NECESSARY

discussions = []
"""
[{"discussionname": 'Mainaccount',
                "padletlink": "https://padlet.com/titicha/bz3zhbzqmuzhd1qm",
                "categories": ["First column", "second column", "third", "fourth"],
                "catcodes": ["C1", "C2", "C3", "C4"],
                "catids": ["section-41504012", "section-41504018", "section-41504020", "section-41504022"],
                "messages": [],
                "lastmessages": [],
                "newmessagefound": False,
                "commands": [],
                "lastcommands": [],
                "newcommandsfound": False},
                
                {"discussionname": 'Multipadlet?',
                "padletlink": "https://padlet.com/titicha/multipadlet",
                "categories": ["Column ONE", "Column TWO", "Column THREE", "Column Four"],
                "catcodes": ["C1", "C2", "C3", "C4"],
                "catids": ["section-51673453", "section-51673465", "section-51673480", "section-51673489"],
                "messages": [],
                "lastmessages": [],
                "newmessagefound": False,
                "commands": [],
                "lastcommands": [],
                "newcommandsfound": False}
                ]
"""
#csvReader.exportJSON("discussionswithpadlets.json", discussions)



def initialisation(whatsapplink):
    discussions = csvReader.importJSON("discussionswithpadlets.json")
    #print(discussions)
    os.system("rm -r /home/pi/Desktop/Projet_Transfert_Auto_Padlet/chromedata/Default")
    os.system("cp -r /home/pi/.config/chromium/Default /home/pi/Desktop/Projet_Transfert_Auto_Padlet/chromedata")
    coptions = webdriver.ChromeOptions()
    coptions.add_argument("--user-data-dir=/home/pi/Desktop/Projet_Transfert_Auto_Padlet/chromedata")
    whatsappdriver = selenium.webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver", options=coptions)
    whatsappdriver.get(whatsapplink)
    time.sleep(5)
    wait = WebDriverWait(whatsappdriver, 600)
    time.sleep(5)
    whatsappweb.opendiscussion('"Mainaccount"', wait)
    padletdriver = selenium.webdriver.Chrome(os.path.expanduser("/usr/lib/chromium-browser/chromedriver"))
    return whatsappdriver,padletdriver,discussions

#CHANGES NEEDED
whatsappdriver,padletdriver,discussions = initialisation(whatsapplink)

print("Enter loop")
#Boucle principale d'Autopadlet
while True :
    try:
        whatsappweb.findandpickdiscussion(downbuttondiv, newmessagenotif, whatsappdriver, msginputdiv)
        current_discussion = whatsappweb.iddiscussion(discussionnamediv, discussions, whatsappdriver)

        if current_discussion != -1:
            padletlink = discussions[current_discussion]["padletlink"]
            discussionname = discussions[current_discussion]["discussionname"]
            messages = discussions[current_discussion]["messages"]
            lastmessages = discussions[current_discussion]["lastmessages"]
            newmessagefound = discussions[current_discussion]["newmessagefound"]
            commands = discussions[current_discussion]["commands"]
            lastcommands = discussions[current_discussion]["lastcommands"]
            newcommandsfound = discussions[current_discussion]["newcommandsfound"]
            categories = discussions[current_discussion]["categories"]
            catcodes = discussions[current_discussion]["catcodes"]
            catids = discussions[current_discussion]["catids"]
            try:
                uploadlog = csvReader.importCSV(discussionname + "_uploaded_images.csv")
            except: uploadlog = []

            if padletdriver.current_url != padletlink:
                padletdriver.quit()
                padletdriver = selenium.webdriver.Chrome(os.path.expanduser("/usr/lib/chromium-browser/chromedriver"))
                padletdriver.get(padletlink)
                time.sleep(5)

            messages, newmessagefound, lastmessages = whatsappweb.findnewmessages_V2(whatsappdriver, messages, lastmessages, imgmsgdiv2)

            if newmessagefound and messages != []:
                try:
                    tmpmessages = [message.find_element_by_css_selector(imgmsgdiv) for message in messages]
                except:
                    tmpmessages = []
                    for message in messages:
                        try:
                            tmpmessages.append(message.find_element_by_css_selector(imgsmsgdiv))
                        except: pass
                messages = tmpmessages
                print("New message(s) found") 
                
                newmessagefound = False
                messagetexts = whatsappweb.readmessagetext(messages)
                messagetimes = whatsappweb.findmessagetime(messages, msgtimespan)
                padletsends = whatsappweb.findpadletsends(messagetexts)
                categorized = padlet.setimagecategories(messagetexts, padletsends, categories, catcodes, catids)
                messages_with_data = padlet.setmessagedata(messages, categorized, messagetexts, messagetimes, catcodes)
                print(messages_with_data)

                for message in messages_with_data: #On parcoure les messages detectes
                    if message["category_id"] != "ERR": #Verification pour savoir si le message a une categorie
                        if padlet.checkuploads(message, uploadlog): #Verification pour ne pas envoyer une deuxieme fois la meme image sur le padlet
                            uploadlog.append({"uploaddata": (message["category_name"] + message["Title"] + message["Description"] + message["Time"])})
                            padlet.updateuploadlog_V2(uploadlog, discussionname)
                            whatsappweb.downloadimage(message["message"], whatsappdriver, imgpicdiv, actionbuttonsdiv)
                            padlet.postonpadlet(message, padletdriver)
                            whatsappweb.sendmessage(('''L'image "''' + message["Title"] + '" est sur le padlet'), whatsappdriver, msginputdiv, msginputfield)
                    else:
                        whatsappweb.sendmessage(("Erreur dans le code de catégorie padlet"), whatsappdriver, msginputdiv, msginputfield)      

                if "VOID" in catcodes:
                    void_id_index = -1
                    for code in range(len(catcodes)):
                        if catcodes[code] == "VOID":
                            void_id_index = code
                    for message in range(len(messages)):
                        if not message in padletsends:
                            whatsappweb.downloadimage(messages[message], whatsappdriver, imgpicdiv, actionbuttonsdiv)
                            padlet.postonpadlet({"category_id": catids[void_id_index], "Title": messagetexts[message] , "Description": ""}, padletdriver)
                            whatsappweb.sendmessage(("L'image est sur le padlet"), whatsappdriver, msginputdiv, msginputfield)                    



            #Detection de nouveaux messages contenant des commandes
            commands, newcommandsfound, lastcommands = whatsappweb.findnewmessagesforcommands_V2(whatsappdriver, commands, lastcommands, lastmessages, normmsgdiv2, normmsgdiv)

            #Instructions a executer si il y a de nouvelles commandes
            if newcommandsfound and commands != []:
                print("New commands found")

                #Traitement de la commande et extraction des informations
                newcommandsfound = False
                commandtexts = whatsappweb.readmessagetext(commands)
                print(commandtexts)
                commandstoexecute = whatsappweb.findpadletsends(commandtexts)
                responses = whatsappweb.executecommands_V2(commandtexts, commandstoexecute, categories, catcodes, padletlink)
                commandtexts, commandstoexecute = [],[]

                #Envoi des reponses a la commande
                for text in responses:
                    #Envoi de la reponse
                    whatsappweb.sendmessage(text, whatsappdriver, msginputdiv, msginputfield)

                    #Instructions si le killcode est active
                    if "Autopadlet: Killing the autopadlet process" in text:
                        discussions[current_discussion]["padletlink"] = padletlink
                        discussions[current_discussion]["discussionname"] = discussionname
                        #discussions[current_discussion]["messages"] = messages
                        discussions[current_discussion]["lastmessages"] = lastmessages
                        discussions[current_discussion]["newmessagefound"] = newmessagefound
                        #discussions[current_discussion]["commands"] = commands
                        discussions[current_discussion]["lastcommands"] = lastcommands
                        discussions[current_discussion]["newcommandsfound"] = newcommandsfound
                        discussions[current_discussion]["categories"] = categories
                        discussions[current_discussion]["catcodes"] = catcodes
                        discussions[current_discussion]["catids"] = catids
                        csvReader.exportJSON("discussionswithpadlets.json", discussions)
                        killtaskrequested = True
                        time.sleep(5)
                        print("AUTOPADLET PROCESS TERMINATED")
                        whatsappdriver.quit()
                        padletdriver.quit()
                        quit()
                        exit()
                        break
            
            if len(lastmessages) >= 100:
                lastmessages = lastmessages[49:len(lastmessages)-1]
                print("CLEARED EXCESS MESSAGES")
            if len(lastcommands) >= 200:
                print(lastcommands)
                lastcommands = lastcommands[149:len(lastcommands)-1]
                print(lastcommands)
                print("CLEARED EXCESS COMMANDS")

            discussions[current_discussion]["padletlink"] = padletlink
            discussions[current_discussion]["discussionname"] = discussionname
            #discussions[current_discussion]["messages"] = messages
            discussions[current_discussion]["lastmessages"] = lastmessages
            discussions[current_discussion]["newmessagefound"] = newmessagefound
            #discussions[current_discussion]["commands"] = commands
            discussions[current_discussion]["lastcommands"] = lastcommands
            discussions[current_discussion]["newcommandsfound"] = newcommandsfound
            discussions[current_discussion]["categories"] = categories
            discussions[current_discussion]["catcodes"] = catcodes
            discussions[current_discussion]["catids"] = catids

            csvReader.exportJSON("discussionswithpadlets.json", discussions)


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
        whatsappdriver,padletdriver,discussions = initialisation(whatsapplink)
        recoveredcrashes += 1
        print("AUTOPADLET: RECOVERED CRASHES = "+str(recoveredcrashes))
