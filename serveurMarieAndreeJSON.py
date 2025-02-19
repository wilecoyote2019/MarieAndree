#
#Backend pour Marie Andre
#V3.0
#16/02/2025
#
import streamlit as st
import os
import socket
from PyPDF2 import PdfReader
import docx
import sys
import json

from langchain_community.chat_models import ChatOpenAI
from langchain_community.llms import OpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.callbacks.manager import get_openai_callback
from langchain_openai import OpenAIEmbeddings







def main():


    openai_api_key = "OPENAI_API_KEY"  
    print("Server Version 3.0 OK")
    
    #Launch socket and main loop 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        chat_histories = {}
        chat_history = []
        conversation_chains = {}
        s.bind(("192.168.1.157", 2209))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connection de : {addr}")
                while True:
                    data = conn.recv(8192)
                    if not data:
                        break
                    print("Requete recue : ", data)
                    data_loaded = json.loads(data)

                    session_key=next(iter(data_loaded))
                    
                    query=data_loaded[session_key]
                    accord=data_loaded["accord"]
                    
                    #Here we create the language model 
                    vectorestore_dir = "./vectorestores/vectorestore." + accord + "/"
                    print("Using vectorestore directory : " + vectorestore_dir)
                    FAISS_INDEX=vectorestore_dir
                    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
		    #Check if there is a local vector store
                    index_path=vectorestore_dir + "index.faiss"
                    if os.path.exists(index_path):
                        print("Vector store exists using it")
                        vetorestore=FAISS.load_local(FAISS_INDEX, embeddings,allow_dangerous_deserialization=True)
                    else:
                    	print("Vector store does not exists")
                    # create conversation chain
                    # llm = ChatOpenAI(openai_api_key=openai_api_key, model_name = 'gpt-3.5-turbo',temperature=0)
                    llm = ChatOpenAI(openai_api_key=openai_api_key, model_name = 'gpt-4-turbo-preview',temperature=0)
                    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
                    conversation_chain = ConversationalRetrievalChain.from_llm(
			llm=llm,
			retriever=vetorestore.as_retriever(),
			memory=memory
		    )
                    
                    
                    ########################################
                    print("Session key:",session_key,"-Query:",query) 
                    #Check if there is chat history
                    if session_key in chat_histories:
                        print("There is a chat history")
                        chat_history=chat_histories[session_key]
                        conversation_chain = conversation_chains[session_key]
                    else:
                        print("No chat history")
                        chat_history=[]
                        llm = ChatOpenAI(openai_api_key=openai_api_key, model_name = 'gpt-4-turbo-preview',temperature=0)
                        memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
                        conversation_chain = ConversationalRetrievalChain.from_llm(
                            llm=llm,
                            retriever=vetorestore.as_retriever(),
                            memory=memory
                        )
                        conversation_chains[session_key] = conversation_chain
                   
                    with get_openai_callback() as cb:
                        #query = data.decode('utf-8')
                        result = {}
                        result = conversation_chain({"question": query, "chat_history": chat_history})
                        chat_history.append((query, result["answer"]))
                        chat_histories[session_key] = chat_history
                        
                        response=result["answer"]
                        print(response.encode())
                        conn.sendall(response.encode('utf-8'))



if __name__ == '__main__':
    main()






