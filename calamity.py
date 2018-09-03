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
            Calamity._load(self, filepath)
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
    
    def _load(self, f):
        self.payload = eval(open(f, 'r').read())
            
    def urlRead(f):
        return list(filter(None, open(f, 'r').read().split('\n')))
    
    def save(self):
        f = self.filepath
        f = f.split('.')[0]
        try:
            open(f + '-' +  str(int(time.time())) + '.lobj', 'w').write(str(self.payload))
        except:
            print('Failed to write the Object')
            
    def overwrite(self):
        f = self.filepath
        f = f.split('.')[0]
        try:
            open(f, 'w').write(str(self.payload))
        except:
            print('Failed to write the Object')
        
            
    def listTopics(self):
        return [(x['meta']['topic'], x['meta']['label']) for x in self.payload]
    
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
        print('Label not found')
        return 0
    
    def getEvent(self, eventLabel):
        for x in self.payload:
            if x['meta']['label'] == eventLabel:
                return x
        print('Event', eventLabel, 'not found')
    
    def peekEvent(self, eventLabel):
        for x in self.payload:
            if x['meta']['label'] == eventLabel:
                return choice(x['articles'])['text']
        print('Event', eventLabel, 'not found')
        
    def fetch(self, topic, label, year, urlfilepath=None, urllist=None):
        b = []
        if urlfilepath != None:
            urllist = Calamity.urlRead(urlfilepath)
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
                x['articles'].append(p['articles'])
                break
        else:
            self.payload.append(p)
        print('[$] Added', len(b), 'articles to', label)
        
    def _tryRequests(url, articleInstance):
        r = requests.get(url, headers={'User-Agent' : 'newspaper/0.2.7'})
        if r.status_code == 200:
            articleInstance.set_html(r.text)
            articleInstance.parse()
            articleInstance.nlp()
            return True
        return False