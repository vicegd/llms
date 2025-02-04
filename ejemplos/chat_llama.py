#!/usr/bin/env python
# coding: utf-8

# # Chat con Llama y Streamlit

# ## Importaciones

# In[1]:


import streamlit as st #la librería para manejar la interfaz
import ollama #la librería para trabajar con los modelos


# ## Funciones para ayudar con el trabajo

# In[2]:


#inicializamos los parámetros de la aplicación
def initialize():
    st.set_page_config( #configuración básica
        page_title="Chatbot con Ollama y Llama3.1",
        layout="wide",
    )

#generamos la respuesta del modelo
def generateResponse(chat_completion): #chat completion es el generador
    for chunk in chat_completion: #cada chunk es un fragemento de la respuesta (no necesiriamente tokens)        
        if chunk['message']['content']: #si el contenido ni es nulo o vacío...
            yield chunk['message']['content'] #yield va generando "bajo demanda", si tener que esperar a toda la respuesta de golpe


# ## Inicializamos el sistemna y comenzamos a trabajar con él

# In[4]:


initialize()

models = ollama.list()['models'] #cargamos los modelos de Ollama que tenemos en nuestro equipo

if "messages" not in st.session_state: #si la sesión está todavía a vacío
    st.session_state.messages = [] #incializamos los mensajes de la sesión 
    system_prompt = """Eres un chatbot que se llama Ayudante. Vas a responder a todas las preguntas que sepas. 
                        Indicarás claramente cuando no sepas responder algo. 
                        También preguntarás lo que necesites para responder adecuadamente.
                        """
    st.session_state.messages.append({"role": "system", "content": system_prompt}) #añadimos el prompt del sistema

#muestra el diálogo desde el principio
with st.container(): #crea un contenedor en la interfaz de Streamlit (cuadro principal)
    #messages es una lista de diccionarios donde cada diccionario representa un mensaje en el chat
    for message in st.session_state.messages: #st.session_state se puede utilizar para guardar datos de ejecución (en este caso los mensajes de la conversación)
        if message["role"] != "system": #ocultamos el prompt de sistema
            with st.chat_message(message["role"]): #st.chat_message crea un contenedor diseñado para mostrar mensajes de chat. message["role"] determina como se visualiza el mensaje dependiendo del rol
                st.markdown(message["content"]) #renderiza el mensaje como markdowm

prompt = st.chat_input("¿Con qué te puedo ayudar?")
if prompt: #cada vez que se pulse INTRO en el cuadro de conversación
    st.chat_message("user").markdown(prompt) #se muestra el contenido del ÚLTIMO mensaje en el cuadro de conversación
    st.session_state.messages.append({"role": "user", "content": prompt}) #agregamos el mensaje introducido en el historial de conversaciones
    
    chat_completion = ollama.chat(
         model = "llama3.1", #el modelo seleccionado en el desplegable
         messages = st.session_state.messages, #le pasa todo el historial para tener el contexto
         stream = True,
    )
    
    with st.chat_message("assistant"):            
        response = generateResponse(chat_completion)
        full_response = st.write_stream(response) #st.write_stream simula la escritura                          
        st.session_state.messages.append({"role": "assistant", "content": full_response}) #agregamos la respuesta al historial de chat


# In[ ]:




