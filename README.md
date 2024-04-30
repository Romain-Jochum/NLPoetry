# NLPoetry 📝
"Infinite Inspiration, Endless Expressions"

## Description 📋
This is a class project for our NLP class, 

In this project we aim to fine-tune a LLM model (Mixtral 7b) to generate poems in French according to a given theme, author style or date.

We got the data via web scraping the website poesie-francaise.fr on the 21st of April 2024.

The finetuning was done one the 27th of April 2024 on bre.dev platform, it costed 4.75$ for roughly 3 hours of use out of which the training took around 30 minutes.

## Self Review ✅

The code is functionnal for a **MVP** but there are a lot of improvement possible:  
1. Merge the two scraping python scripts into one
2. Improve the metering function inside of the cleaning notebook
3. Finetune the meta data of our model
4. Finetune the model on using longer tokens
5. Update to the latest Mistral 7B v0.2  

## Links 🔗

Here are all the usefull links for this projet.

The [tutorial notebook](https://github.com/brevdev/notebooks/blob/main/mistral-finetune-own-data.ipynb) from brev.dev on how to fine tune Mistral 7B model used for finetuning Mistral 7B.  

Here is our [finetuned model](https://huggingface.co/Romain-Jochum/Mistral_7B_French_Poetry_Tuning/tree/main). (the link might not accessible, it I because of licences)

The [presentation](https://docs.google.com/presentation/d/1V2oZwTibtwemJEd7ksLPC_z93aWlcLYCAdNTloXmBCQ/edit?usp=sharing) and the [detailed review](https://docs.google.com/document/d/1S_Hr29yUpTz7Lvgs4-ujGEsdIdnX4bwjs2w3LyG-oIA/edit?usp=sharing) of the project.
