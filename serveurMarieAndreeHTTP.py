#
#Interface pour Marie Andree
#V3.0
#16/02/2025
#

import streamlit as st
import os
import random
import string
import json
from PyPDF2 import PdfReader
import docx
import socket
import hmac
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain import HuggingFaceHub
from streamlit_chat import message
from langchain.callbacks import get_openai_callback


###Fonction de protection par mot de passe
def check_password():
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.image("https://reference-syndicale.fr/logo-cgt.png", width=100)
    st.header("Bienvenue chez Marie-Andree!!")
    st.subheader("L'IA de la CGT Thales qui connait les Accords et Convention collective!")
    st.subheader("Cette page est protegee. Pour obtenir le mot de passe contactez : ")
    st.subheader("francois.baltazar[at]thalesaleniaspace.com")
    st.text_input(
        "Mot de Passe", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


if not check_password():
    st.stop()  # Do not continue if check_password is not True.
    

def accord_change():
    print("Changement Accord")
    print("Create session Key new")
    #Create new session key 
    for i in range(3):
        # get random string of length 6 without repeating letters
        result_str = ''.join(random.sample(string.ascii_lowercase, 8))
    st.session_state.key = result_str
    st.session_state.messages.append({"role": "assistant", "content": "Posez-moi vos questions sur cet accord alors. J'oublie notre conversation anterieure..."})
    #st.chat_message("assistant").write("Posez-moi vos questions sur cet accord alors.")
    
    return False


# "with" notation
def main():
    #load_dotenv()
    
    st.set_page_config(page_title="Discutes sur un accord Thales!", layout="wide")
    #st.set_page_config( layout="wide")
    st.header("Discussion accords Thales")
    for i in range(3):
        # get random string of length 6 without repeating letters
        result_str = ''.join(random.sample(string.ascii_lowercase, 8))
    if 'key' not in st.session_state:
        st.session_state.key = result_str
    #st.set_page_config(layout="wide")
    
    
    
    st.sidebar.image("https://reference-syndicale.fr/logo-cgt.png", use_container_width=True)
    #Select box
    option = st.sidebar.selectbox(
    "Selectionner l'accord",
    ("0-Tous les documents", 
    "1-Nouvelle convention Collective de la Metallurgie - Juin 2024",
    "2-Anticipation - Avril 2019",
    "3-Droit Syndical - Novembre 2018",
    "4-Representation du Personel - Novembre 2018",
    "5-Temps de Travail - Septembre 2023",
    "6-Dispositions Sociales avec avenants- Juin 2022",
    "7-CET - Juillet 2023",
    "8-Deplacements Professionels",
    "9-Handicap - Decembre 2024",
    "10-Deploiement CCN Metallurgie - Janvier 2023",
    "11-Interressement - Juin 2023",
    "12-PERECO - Mai 2021"),on_change=accord_change,
    )
    #st.sidebar.write("Questionner Marie Andree sur :", option)
    accord_num = option.split("-")[0]
    
    print("Accord number : " + accord_num)
    filepath="pages/zip/Accords_Groupe_Thales.zip"
    filename="Accords_Groupe_Thales.zip"
    mimetype="application/pdf"
    if accord_num == "0":
    	filepath="pages/zip/Accords_Groupe_Thales.zip"
    	filename="Accords_Groupe_Thales.zip"
    	mimetype="application/zip"
    elif accord_num == "1":
    	filepath="pages/pdfs/CNN_metallurgie_consolidee-au-10-06-2024.pdf"
    	filename="CNN_metallurgie_consolidee-au-10-06-2024.pdf"
    elif accord_num == "2":
    	filepath="pages/pdfs/Accord_Anticipation_04_2019.pdf"
    	filename="Accord_Anticipation_04_2019.pdf"
    elif accord_num == "3":
    	filepath="pages/pdfs/Accord_Droit_Syndical_11-2018.pdf"
    	filename="Accord_Droit_Syndical_11-2018.pdf"
    elif accord_num == "4":
    	filepath="pages/pdfs/Accord_Representation_Personel_11-2018.pdf"
    	filename="Accord_Representation_Personel_11-2018.pdf"
    elif accord_num == "5":
    	filepath="pages/pdfs/Accord_Temps_de_Travail_09-2023.pdf"
    	filename="Accord_Temps_de_Travail_09-2023.pdf"
    elif accord_num == "6":
    	filepath="pages/pdfs/Accord_Dispositions_Sociales_06-2022.pdf"
    	filename="Accord_Dispositions_Sociales_06-2022.pdf"
    elif accord_num == "7":
    	filepath="pages/pdfs/Accord_CET_07-2023.pdf"
    	filename="Accord_CET_07-2023.pdf"
    elif accord_num == "8":
    	filepath="pages/pdfs/Accord_Conditions_deplacement.pdf"
    	filename="Accord_Conditions_deplacement.pdf"
    elif accord_num == "9":
    	filepath="pages/pdfs/Accord_Handicap_12-2024.pdf"
    	filename="Accord_Handicap_12-2024.pdf"
    elif accord_num == "10":
    	filepath="pages/pdfs/Accord_de_deploiement_CCN_Metallurgie-01-2023.pdf"
    	filename="Accord_de_deploiement_CCN_Metallurgie-01-2023.pdf"
    elif accord_num == "11":
    	filepath="pages/pdfs/Accord_interressement_06-2023.pdf"
    	filename="Accord_interressement_06-2023.pdf"
    elif accord_num == "12":
    	filepath="pages/pdfs/Accord_PERECO_05-2021.pdf"
    	filename="Accord_PERECO_05-2021.pdf"

    with open(filepath, "rb") as file:
    	btn = st.sidebar.download_button(
    		label="Telecharger",
    		data=file,
    		file_name=filename,
    		mime=mimetype,
    	)
    
    
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Salut, je suis Marie-Andree, l'IA de la CGT Thales. Je connais quelques accords sur lesquels tu peux me poser des questions"}]
    
    
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])    
    
    st.session_state.processComplete = True

    if  st.session_state.processComplete == True:
        user_question = st.chat_input("Poses ta question sur les accords")
        if user_question:
                print("Demande au serveur IA : " + user_question)
                print("Session key : ",st.session_state.key)
                HOST = "192.168.1.157"  # The server's hostname or IP address
                PORT = 2209  # The port used by the server
                st.session_state.messages.append({"role": "user", "content": user_question})
                st.chat_message("user").write(user_question)
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    try: 
                        s.connect((HOST, PORT))
                        #Create dict and serialize it with json
                        user_question_dict = {}
                        user_question_dict[st.session_state.key] = user_question
                        user_question_dict["accord"] = accord_num
                        user_question_serialized = json.dumps(user_question_dict)
                        #s.sendall(user_question.encode())
                        s.sendall(user_question_serialized.encode())
                        data = s.recv(8192)
                        response = data.decode()
                        print("Reponse recue du serveur IA : " + response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        st.chat_message("assistant").write(response)
                    except ConnectionRefusedError:
                        st.session_state.messages.append({"role": "assistant", "content": "Desole je ne peux pas repondre, je suis en greve! Reessaie plus tard"})
                        st.chat_message("assistant").write("Desole je ne peux pas repondre, je suis en greve! Reessaie plus tard")



if __name__ == '__main__':
    main()






