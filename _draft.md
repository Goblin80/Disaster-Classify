[comment]: # (View this using any online Markdown Editor)
# Scrapping Process
## Collecting URLs
* The articles were carefully selected only from reputable news outlets, using various search engines and other news aggregators.
* Passing collected URLs to a soft crawler that respects the site's scrapping policy to fetch each article's raw HTML and saving it locally for further analysis.
* Further analysis consists of isolating the article's body and generate a summary of the text and extract relevernt keywords + publish date.
* Then all of this information is saved in a special format that facilates accessibilty as it has the ability to retrieve complete topics or individual events.
### Pre-Classify
* Article's text is tokenized and filtered the stopping word.
* To avoid potential discrepancies the number of occurrences of each word in a document is divided by the total number of words in the document using 'tfidf'.
* To reduce inflectional forms and sometimes related forms of a word to a common base form 'stemming' used.
### Selected Classifers
1. Stochastic Gradient Descent.
2. Multinomial Naïve Bayes.
3. Passive-Aggressive.
4. KNeighbors.
5. Random Forest.
6. LogisticRegression.
7. Linear Support Vector.
## Classification Process
### Topic Classify
* A sample from each topic has been taken to a Mulitclass trainning process according the procedure mentioned above.
* A sample from each topic has been taken to a One Vs. All trainning process according the procedure mentioned above.
### Event Classify
* A sample from each event has been taken to a Mulitclass trainning process according the procedure mentioned above.
* A sample from each event has been taken to a One Vs. All trainning process according the procedure mentioned above.