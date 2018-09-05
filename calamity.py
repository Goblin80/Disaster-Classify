import time
import nltk
import requests
from random import choice
from newspaper import Article, Config

class Calamity:
    config = Config()
    config.request_timeout = 20
    config.memoize_articles = False
    config.browser_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    
    def __init__(self, filepath):
        self.payload = []
        self.filepath = filepath
        self.urls_skipped = []
        try:
            Calamity.load(self, filepath)
            print('Object has been successfully loaded')
        except:
            print(filepath, 'not found, nvm creating a new empty one')
            
        
        
    def _sz(a): # str/eval
        return {
            'text': a.text,
            'title': a.title,
            'url': a.url,
            'keywords': a.keywords,
            'tags': a.tags,
            'summary': a.summary,
            'date': int(a.publish_date.timestamp()) if a.publish_date != None else None
    #         'raw' : a.html
        }
    
    def load(self, f):
        new_payload = eval(open(f, 'r').read())
        existing_metas = [x['meta'] for x in self.payload]
        
        for event in new_payload:
            if event['meta'] in existing_metas:
                idx = existing_metas.index(event['meta'])
                existing_articles = self.payload[idx]['articles']
                existing_articles_url = [x['url'] for x in self.payload[idx]['articles']]
                article_count = 0
                for article in event['articles']:
                    if article['url'] not in existing_articles_url:
                        existing_articles.append(article)
                        article_count += 1
                if article_count:
                    print('[+] Added', article_count, 'articles to exisiting event', event['meta']['label'])
            else:
                print('[+] New event', event['meta']['label'], 'had been added')
                self.payload.append(event)
            
    def urlRead(f):
        return list(filter(None, open(f, 'r').read().split('\n')))
    
    def save(self):
        f = self.filepath
        f = f.split('.')[0]
        try:
            open(f + '-' +  str(int(time.time())) + '.lobj', 'w').write(str(self.payload))
        except:
            print('[X] Failed to write the Object')
            
    def overwrite(self):
        f = self.filepath
        f = f.split('.')[0]
        try:
            open(f, 'w').write(str(self.payload))
        except:
            print('[X] Failed to write the Object')
        
            
    def listTopics(self):
        return [(x['meta']['topic'], x['meta']['label'], len(x['articles'])) for x in self.payload]
    
    def listEvents(self, topic):
        res = []
        for x in self.payload:
            if x['meta']['topic'] == topic:
                res.append(x['meta']['label'])
        return res
    
    def listAllEvents(self):
        return [x['meta']['label'] for x in self.payload]
    
    def numArticles(self, eventLabel):
        for x in self.payload:
            if x['meta']['label'] == eventLabel:
                return len(x['articles'])
        print('[?] Label not found')
        return 0
    
    def getEvent(self, eventLabel):
        for x in self.payload:
            if x['meta']['label'] == eventLabel:
                return x
        print('[?] Event', eventLabel, 'not found')
    
    def peekEvent(self, eventLabel):
        for x in self.payload:
            if x['meta']['label'] == eventLabel:
                return choice(x['articles'])['text']
        print('[?] Event', eventLabel, 'not found')
        
    def fetch(self, topic, label, year, urlfilepath=None, urllist=None):
        b = []
        if urlfilepath != None:
            urllist = Calamity.urlRead(urlfilepath)
        
        urllist_clean = list(set(urllist))
        if(len(urllist_clean) < len(urllist)):
            print('[*] Removed', len(urllist) - len(urllist_clean),'duplicate URLs')
            urllist = urllist_clean
        
        for x in urllist:
            a = Article(url= x.strip(), config= Calamity.config)
            try:
                a.download()
                a.parse()
                a.nlp()
                b.append(Calamity._sz(a))
            except Exception as e:
                if Calamity._tryRequests(x, a) == False:
                    print('[X] Error at: ', x)
                    print(str(e))
                    self.urls_skipped.append(x)
                else:
                    print('[*] Obtained', x, 'using requests instead')
                    b.append(Calamity._sz(a))
                                
        p = {'articles': b, 'meta': {'label' : label, 'year': year, 'topic': topic}}                
        for x in self.payload:
            if x['meta'] == p['meta']:
                x['articles'].extend(p['articles'])
                break
        else:
            self.payload.append(p)
        print('[+] Added', len(b), 'articles to', label)
        
    def _tryRequests(url, articleInstance):
        r = requests.get(url, headers={'User-Agent' : 'newspaper/0.2.7'})
        if r.status_code == 200:
            articleInstance.set_html(r.text)
            articleInstance.parse()
            articleInstance.nlp()
            return True
        return False