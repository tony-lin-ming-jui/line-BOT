import song_crawler
  

rank=song_crawler.ranking()

rankCh='\n'.join(rank[:11])
rankwestern='\n'.join(rank[11:22])
rankNEA='\n'.join(rank[-11:])
print(rankNEA)
