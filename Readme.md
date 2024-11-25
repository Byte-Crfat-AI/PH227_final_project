# Chatbot for the Physics Department IITB

## Overview

This project is a chatbot designed for the Physics Department at IITB. It leverages Retrieval-Augmented Generation (RAG) to provide answers to the queries asked to the chatbot (Gemini) about the Physics Department at IITB.

## Data

For this project our Mother data was UG rulebook which gives us the primary details about things in IIT Bombay. For extrction of data about Physics department specifically we have used the Course Book by Department of Physics. But this lacked details about the professors and research going on in Physics Department, hence we deployed a Gemini powered web scraper that scrapes the data from the Physics department website and leverages gemini to obtain a structured meaningful data in JSON format.



## Google Drive
As the source files are kind of bulky, here is the google drive link with the source files https://drive.google.com/file/d/1IhVSvYO337Vf4uGm4dy8tcUa6G8-J5Lz/view?usp=drive_link
