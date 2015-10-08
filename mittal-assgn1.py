#########################################
# Part 1:max_match algorithm ,know the source of failure 
#########################################

#   Return the corpus file as the dictionary 
def read_corpus():

    fd = open("bigwordlist.txt", 'r')
# read the file as list
    corpus = fd.readlines()
    fd.close()
# Strip the newline character form the each word of corpus
    corpus = [word.rstrip('\n') for word in corpus]
# Split the list to make the key value pairs where value is frequeny
    corpus = [word.split() for word in corpus]
# take ony 75000 words from the list
    corpus = corpus[:75000]
# convert it into the dictionary

    return dict(corpus)



#MAX_MATCH ALGORITHM

def max_match(hashtag_word, corpus):
#strip the # character from the start of the word and conert it into lower case
    hashtag_word = hashtag_word.lstrip('#').lower()
# to know the lenght of the word,to know the end inex of the word
    length = len(hashtag_word)
# intially the start_index pointer starts from the position 0 of word
    start_index = 0
# list  to return the all words output from the max_match algorithm
    matched_words = []
 # loop while we still have an index that is less than our entire word length
    while start_index < length:
# Flag is toshow that matched found in corpus or not 
        matched_flag = False
 # check if word from start_index to the end is in corpus
        for i in range(length, 0, -1):

            if hashtag_word[start_index:i] in corpus:
#if the matches found,then append it into the list of matched_words
                matched_words.append(hashtag_word[start_index:i])
# set the start_index to end of the word matched
                start_index = i
                matched_flag = True
                break
# We don't have a match, increment our starting point and add single character
        if not matched_flag:
            matched_words.append(hashtag_word[start_index])
            start_index += 1
#return the list of matched words
    return matched_words




# function which read the corpus aand read the file hashtag file and apply the max_match algorithm and return the matched list and write it into the output_1.txt

def question1():
# read the bigwordlist and store it into the corpus ,to be used in the max_match 
    corpus = read_corpus()
# open the hasttags-dev file in reading mode
    mydata = raw_input('For The Question 1 \n Enter the hastags file name :')
    fi = open(mydata,"r")

   # fi = open("hashtags-dev.txt", 'r')
# open the output_1.txt file in writing mode to write the matched words in form of line 

    fd = open("output_1.txt", 'w')
# store the lines of hashtag file as element of list and stor it in the hash_word list

    hash_words = fi.readlines()
# close the hashtag file

    fi.close()
# for each hash_word strip the # and newline character 
    hash_words = [each_hash_words.lstrip('#').lower().rstrip('\n') for each_hash_words in hash_words]
# loop through each word of the list of hash_words and apply the max_match algorithm on each word
    for words in hash_words:
# join the list of returned matched word from the max_match algo
        matched = (' '.join(max_match(words, corpus)))
# write that on the output file
        fd.writelines(matched)
#write the new line character to after each line
        fd.write('\n')
# return the all the matched list       
    print "Please Find the Output File \"output_1.txt\" in same directory as Input File \n"
    return matched

# call the question1() function to get the matched words

question1()

#########################################
# Part 2: MinimumEditDistance Algorithm to calculate the WER
##########################################

# take the source and target words as a input and return the distance calculate
def min_distance(target,source):
# Calculate the length of target word
    n=len(target)
# calculate the length of Source Word
    m=len(source)

# Intialise the 2 Dimensional Array with 0 in all its element 
    dis=[[0 for i in range(m+1)] for j in range(n+1)]
# In 2D matrix, the first and first column values to be as the insert cost
    for i in range(1,n+1,1):
        dis[i][0]=dis[i-1][0]+1
    for j in range(1,m+1,1):
        dis[0][j]=dis[0][j-1]+1
# Loop through each element of the matrix and calculate the minimum distance
    for i in range(1,n+1,1):
        for j in range(1,m+1,1):
# if the diagonal element are same then substitution cost is zero,as there will be no substitution,inseration and deleteion
            if(target[i-1]==source[j-1]):
                Subst_cost=0
            else:
                Subst_cost=1

            dis[i][j]=min(dis[i-1][j]+1,dis[i][j-1]+1,dis[i-1][j-1]+Subst_cost)
# return the minimum distance between the source and target word
    return dis[n][m]


# function which read the target and source file and print out the average WER for the whole file 

def question2():
# intialise the total WER as 0
    wer_total=0
#Open the file which have the hashtags-train set  
    mydata = raw_input('For The Question 2 \n Enter the hastags-train file name :')
    fi = open(mydata,"r")
   # fi =open("hashtags-train.txt",'r')
    target_words=fi.readlines()

    fi.close()
#Open the file which have the hashtags-train refernce set ,refernce answers 
    mydata = raw_input('Enter the hastags-train Reference file name :')
    fs = open(mydata,"r")
    #fs =open("hashtags-train-reference.txt",'r')
    source_words=fs.readlines()
    print "\n"

    fs.close()
# strip the hash tag and newline character, and covert each word in source list to lower case 
    source_words=list([each_target_words.rstrip('\n').lower().split() for each_target_words in source_words])

    target_words=list([each_target_words.rstrip('\n').lower() for each_target_words in target_words])
# List too store the output of max_match algo applied on the hashtags-train set
    target_set=[]
# Read the corpus
    dct=read_corpus()
# for each word in target_words apply max_match algo and appennd in the target_set
    for target1 in target_words:
        target_set.append(max_match(target1,dct))
# compute the length of list of source_words to calculate the WER
    sources_count = len(source_words)
# Used Zip to extract the each word pair from the target_set and source_word
    for target,source in zip(target_set,source_words):
        # call the min_distance function to calculate the minimum distance between the target and source word
        min_dist=min_distance(target,source)
# calculate tjhe WER for each word
        wer =float(min_dist)/len(source)
# calculate the total Wer  to find out the average
        wer_total +=wer

    print ("By averaged WERs =", wer_total/float(sources_count), wer_total, sources_count )

# call the question1() function to get the matched words

question2()

#########################################
# Part 3,modiified max_match algorithm and chanded in the lexi con 
#########################################


# Modiified algorithm to be used in the Part 3 of the assignment,comment only on the changed part 
def max_match_modified(hashtag_word, corpus):
    hashtag_word = hashtag_word.lstrip('#').lower()
    length = len(hashtag_word)
    start_index = 0
    matched_words = []

    while start_index < length:
        matched_flag = False
        for i in range(length, 0, -1):
            if hashtag_word[start_index:i] in corpus:
# check if "the" is part of the matched word,if it is then only append the "the" in list of matched words
                if  "the" in  hashtag_word[start_index:i]:
                     matched_words.append("the")
                else:
# otherwise,add all the mathed word
                    matched_words.append(hashtag_word[start_index:i])
                start_index = i
                matched_flag = True
                break

        if not matched_flag:
            #matched_words.append(hashtag_word[start_index])
#earlier if no match found then we store the single charcter in the list of matched word
            start_index += 1

    return matched_words


# Function return the modified lexicon
def read_corpus_new():
# Read the correct lexicon 
    dic= read_corpus()
# list of only valid two character allowed
    valid_two_chars = ["an","as","at","be","by","do","go","he","hi",
                           "if","in","is","it","me","my","no","of","oh","on","or","pi",
                           "so","to","up","us","we","cu"]
#list of only valide 3 character allowed
    valid_three_chars = ["the","its","ski","nbc","now","may","you","day","are","and","pit","lad"]
    valid_four_chars = ["lost","have","ever","iran","area","may","with","fail","chip","dont","like","bank","saga","less","ball","talk",
                        "that","lose","team","that","also","news","list"]
# list to store the list of the new words in dictionary
    newdic=[]
# loop through each word in dictionary 
    for key in dic:
# only add the word in the dictionary which have length greater than 1,no single charcter are added
        if len(key)>1:
# if it is 2 charcter word,check if it is in the list of valid two character
            if len(key)==2:
                if key in valid_two_chars:
#append that in the newdic
                    newdic.append([key,dic[key]])
            else:
# if the length of that word is 3,then check if it s valid ,then append it in dictionary
                if len(key)==3:
                    if key in valid_three_chars:
                         newdic.append([key,dic[key]])
                else:
                    if len(key)==4:
                        if key in valid_four_chars:
                             newdic.append([key,dic[key]])
                    else:
                             newdic.append([key,dic[key]])


#convert that into dictionary
    new_dic= dict(newdic)

 #return that new dictionary
    return new_dic

import sys
# return the minimum distance between the source and target word and write the output to output_3 file,it is same as question2 except it calls the max_match_modified
def question3():

    wer_total=0
    min_dis_total=0
    mydata = raw_input('For question 3\n Please Enter the hashtag-train file :')
    fi = open(mydata,"r")

  #  fi =open("hashtags-train.txt",'r')
    target_words=fi.readlines()

    fi.close()
    mydata = raw_input('Please Enter the hashtag-train-refernce file :')
    fs = open(mydata,"r")
    #fs =open("hashtags-train-reference.txt",'r')
    source_words=fs.readlines()


    fs.close()
    source_words=list([each_target_words.rstrip('\n').lower().split() for each_target_words in source_words])

    target_words=list([each_target_words.rstrip('\n').lower() for each_target_words in target_words])

    target_set=[]
    dct1=read_corpus_new()
    fout = open("output_3.txt",'w')
    for target1 in target_words:
        target_set.append(max_match_modified(target1,dct1))
        matched = (' '.join(max_match_modified(target1, dct1)))
        fout.writelines(matched)
        fout.write('\n')
    sources_count = len(source_words)
    fout.close()
    #print target_set

    for target,source in zip(target_set,source_words):
        #print "susan"
        min_dist=min_distance(target,source)
        wer =float(min_dist)/len(source)
        wer_total +=wer
        min_dis_total += min_dist
        #print wer
    print ("By averaged WERs =", wer_total/float(sources_count), wer_total, sources_count )
    print "Please Find the Output File \"output_3.txt\" in same directory as Input File \n"
  #  print ("By totalling WER =", min_dis_total/float(final_word_count), min_dis_total, final_word_count)
question3()




