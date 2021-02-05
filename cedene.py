from sly import Parser
from sly import Lexer

class BasitLexer(Lexer): 
    tokens = { ISIM, NUMARA, STRING } 
    ignore = '\t '
    literals = { '=', '+', '-', '/',  
                '*', '(', ')', ',', ';'} 
  
    ISIM = r'[a-zA-Z_][a-zA-Z0-9_]*'
    STRING = r'\".*?\"'
   

    # Numara tokenleri
    @_(r'\d+') 
    def NUMARA(self, t): 
        # Python integer türüne dönüştürülmesi
        t.value = int(t.value)  
        return t 

     # yorum tokenleri
    @_(r'//.*') 
    def YORUM(self, t): 
        pass
  
    # yeni satır tokeni(sadece göstermek için)
  
    @_(r'\n+') 
    def yeni_satir(self, t): 
        self.lineno = t.value.count('\n')


class BasitParser(Parser): 
    #Tokenlerin lexerdan parsera aktarımı
    tokens = BasitLexer.tokens 
  
    oncelik = ( 
        ('left', '+', '-'), 
        ('left', '*', '/')
    ) 
  
    def __init__(self): 
        self.env = { } 

    @_('') 
    def ifade(self, p): 
        pass

    @_('degisken_tanimla') 
    def ifade(self, p): 
        return p.degisken_tanimla 
  
    @_('ISIM "=" deyim') 
    def degisken_tanimla(self, p): 
        return ('degisken_tanimla', p.ISIM, p.deyim) 
  
    @_('ISIM "=" STRING') 
    def degisken_tanimla(self, p): 
        return ('degisken_tanimla', p.ISIM, p.STRING) 

  #deyimler arasında + - * / operatörleri geldiğinde yapılacak işlemler

    @_('deyim') 
    def ifade(self, p): 
        return (p.deyim) 
  
    @_('deyim "+" deyim') 
    def deyim(self, p): 
        return ('topla', p.deyim0, p.deyim1) 
  
    @_('deyim "-" deyim') 
    def deyim(self, p): 
        return ('cikar', p.deyim0, p.deyim1) 
  
    @_('deyim "*" deyim') 
    def deyim(self, p): 
        return ('carp', p.deyim0, p.deyim1) 
  
    @_('deyim "/" deyim') 
    def deyim(self, p): 
        return ('bol', p.deyim0, p.deyim1) 
            
    @_('ISIM') 
    def deyim(self, p): 
        return ('degisken', p.ISIM) 

    @_('NUMARA') 
    def deyim(self, p): 
        return ('numara', p.NUMARA)

class BasitCalistirma: 
    
    def __init__(self, agac, env): 
        self.env = env 
        sonuc = self.agacDolas(agac) 
        if sonuc is not None and isinstance(sonuc, int): 
            print(sonuc) 
        if isinstance(sonuc, str) and sonuc[0] == '"': 
            print(sonuc) 
  
    def agacDolas(self, dugum): 
  
        if isinstance(dugum, int): 
            return dugum 
        if isinstance(dugum, str): 
            return dugum 
  
        if dugum is None: 
            return None
  
        if dugum[0] == 'program': 
            if dugum[1] == None: 
                self.agacDolas(dugum[2]) 
            else: 
                self.agacDolas(dugum[1]) 
                self.agacDolas(dugum[2]) 
  
        if dugum[0] == 'numara': 
            return dugum[1] 
  
        if dugum[0] == 'str': 
            return dugum[1] 
  
        if dugum[0] == 'topla': 
            return self.agacDolas(dugum[1]) + self.agacDolas(dugum[2]) 
        elif dugum[0] == 'cikar': 
            return self.agacDolas(dugum[1]) - self.agacDolas(dugum[2]) 
        elif dugum[0] == 'carp': 
            return self.agacDolas(dugum[1]) * self.agacDolas(dugum[2]) 
        elif dugum[0] == 'bol': 
            if self.agacDolas(dugum[2])!=0:
                return self.agacDolas(dugum[1]) // self.agacDolas(dugum[2]) 
            else:
                print("sıfıra bölme hatası")

        if dugum[0] == 'degisken_tanimla': 
            self.env[dugum[1]] = self.agacDolas(dugum[2]) 
            return dugum[1] 
  
        if dugum[0] == 'degisken': 
            try: 
                return self.env[dugum[1]] 
            except LookupError: 
                print("Bilinmeyen değişken: '"+dugum[1]) 
                return 0

if __name__ == '__main__': 
    lexer = BasitLexer() 
    parser = BasitParser() 
    print('Çedene Programlama Diline Hoşgeldiniz....')
    env = {} 
      
    while True: 
          
        try: 
            text = input('Cedene > ') 
          
        except EOFError: 
            break
          
        if text: 
            agac = parser.parse(lexer.tokenize(text)) 
            BasitCalistirma(agac, env)
