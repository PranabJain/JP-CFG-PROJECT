
import nltk
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
import tkinter as tk
from tkinter import ttk
 
def read_article(file_name):
    file = open("sample.txt", "r",errors='ignore')
    filedata = file.readlines()
    article = filedata[0].split(". ")
    sentences = []
    article = filedata
    for sentence in article:
        if sentence == '\n':
            continue
        else:
            print(sentence)
            sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
    sentences.pop() 
    return sentences

def to_compare_article(file_name):
    file = open("sample.txt", "r",errors='ignore')
    filedata2 = file.readlines()
    article2 = filedata2[0].split(". ")
    sentences2 = []
    article2 = filedata2
    for sentence in article2:
        if sentence == '\n':
            continue
        else:
            print(sentence)
            sentences2.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
    sentences2.pop() 
    return sentences2

def sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = []
 
    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]
 
    all_words = list(set(sent1 + sent2))
 
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)
 
    # build the vector for the first sentence
    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1
 
    # build the vector for the second sentence
    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1
 
    return 1 - cosine_distance(vector1, vector2)
 
def build_similarity_matrix(sentences, stop_words):
    # Create an empty similarity matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
 
    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2: #ignore if both are same sentences
                continue 
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)

    return similarity_matrix
def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg,)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()

def generate_summary():
    file_name = "sample.text"
    top_n=7
    stop_words = stopwords.words('english')
    summarize_text = []
    
    
    # Step 1 - Read text anc split it
    sentences =  read_article(file_name)
    
    # Step 2 - Generate Similary Martix across sentences
    sentence_similarity_martix = build_similarity_matrix(sentences, stop_words)

    # Step 3 - Rank sentences in similarity martix
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
    scores = nx.pagerank(sentence_similarity_graph)

    # Step 4 - Sort the rank and pick top sentences
    ranked_sentence = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)    
    print("Indexes of top ranked_sentence order are ", ranked_sentence)    

    for i in range(top_n):
      summarize_text.append(" ".join(ranked_sentence[i][1]))
    file = open("output.txt", "w",errors='ignore')
    file.writelines(summarize_text) 
    # Step 5 - Offcourse, output the summarize texr
    print("Summarize Text: \n", ". ".join(summarize_text))
    popupmsg("Hello")
    test = "Hello"
    return test
    
# let's begin
generate_summary()
