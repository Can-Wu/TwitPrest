# To analyze the data acquired from twitter API with keywords 
import sys
import json
import re
import matplotlib.pyplot as plt
import numpy as np

Candicates_Names = ["Hillary Clinton", "Bernie Sanders",\
                    "Donald Trump", "John Kasich", "Ted Cruz"]
#Candicates_Names = ["Hillary Clinton", "Bernie Sanders","Donald Trump","Donald Trump","John Kasich", "Ted Cruz"]
regex_list=[]
score_list=[0] * len(Candicates_Names)
count_list=[0] * len(Candicates_Names)
for canidate in Candicates_Names:
    regex_list.append(canidate.replace(" ", "|"))

def get_score(twitter_words,scores):
            Score = 0
            for iter_word in twitter_words:
            #print "Actual Word",iter_word
            	if iter_word in scores:
                	Score =  Score + scores[iter_word]
                	#print iter_word,'Match',scores[iter_word]
	    return Score	


def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    sent_file.seek(0)
    tweet_file.seek(0)
    scores = {} # initialize an empty dictionary
    
    for line in sent_file:
        term, score  = line.split("\t")      # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)            # Convert the score to an integer.
    line_list=tweet_file.readlines()
    for x in line_list:
        json_data = json.loads(x)
        if "text" in json_data:
            twitter_text=json_data["text"]
            encoded_twitter_text = twitter_text.encode('utf-8')
            twitter_words=encoded_twitter_text.split();
	    already_counted = [0] * len(Candicates_Names)
            for iter_word in twitter_words:
		##Search for presidential Candidates Mentioned
		for i in range(0,len(Candicates_Names)):
			TEMP=re.search(regex_list[i],iter_word, flags=re.I | re.X)
			if TEMP:
				count_list[i]=count_list[i]+1
				if (already_counted[i]==0):
                			score_list[i] = score_list[i]+get_score(twitter_words,scores);
					already_counted[i]=1

    sum_count=sum(count_list);
    for i in range(0,len(count_list)):
	count_list[i]=100*float(count_list[i])/sum_count

    n_groups = len(Candicates_Names)
    index = np.arange(n_groups) 

    fig, ax = plt.subplots()
    labels = Candicates_Names
    sizes = count_list
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'red']
    plt.pie(sizes, labels = labels, colors = colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.savefig('candidate_pop_pie.png', format='png')       
    
    # sentiment plot
    fig, ax = plt.subplots()
    rects2 = plt.bar(index, score_list, bar_width,alpha=0.5,color='r')
    plt.ylabel('Sentiment Score',fontsize=18, color='b')
    plt.xlabel('Candidate',fontsize=18, color='b')
    plt.title('Candicate Sentiment Analysis')
    plt.ylim([-40, 80])
    plt.xticks(index + bar_width, Candicates_Names)
    plt.axhline(linewidth=2, color='b')
    plt.legend()
    plt.tight_layout()
    plt.grid()  
    plt.savefig('Sentiment.png', format='png')
    
    tweet_file.close()
 

if __name__ == '__main__':
    main()
