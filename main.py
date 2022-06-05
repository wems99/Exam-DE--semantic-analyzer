from parsing import Parsing
from tokenizer import tokenize
from analizadorSemantico import AnalisadorSemantico

if __name__ == '__main__':
    print(
        '''
                       _ _              _               _____                  __        _   _           
     /\               | (_)            | |             / ____|                /_/       | | (_)          
    /  \   _ __   __ _| |_ ______ _  __| | ___  _ __  | (___   ___ _ __ ___   __ _ _ __ | |_ _  ___ ___  
   / /\ \ | '_ \ / _` | | |_  / _` |/ _` |/ _ \| '__|  \___ \ / _ \ '_ ` _ \ / _` | '_ \| __| |/ __/ _ \ 
  / ____ \| | | | (_| | | |/ / (_| | (_| | (_) | |     ____) |  __/ | | | | | (_| | | | | |_| | (_| (_) |
 /_/    \_\_| |_|\__,_|_|_/___\__,_|\__,_|\___/|_|    |_____/ \___|_| |_| |_|\__,_|_| |_|\__|_|\___\___/ 
                                                                                                         
                                                                                                         

        Proyecto de:
            Allen Blanco Contreras
            Gabriel Alvarado Martínez

        '''
    )

    print("Análisis Codigo 1")
    analizer = AnalisadorSemantico('codeString2.txt')
    analizer.analizar()
    print("------------------------------")
    print("Análisis Codigo 2")
    analizer = AnalisadorSemantico('codeString 1.txt')
    analizer.analizar()
    print("------------------------------")
    print("Análisis Codigo 3")
    analizer = AnalisadorSemantico('code1Correct.txt')
    analizer.analizar()
    print("------------------------------")
    print("Análisis Codigo 4")
    analizer = AnalisadorSemantico('code2Incorrect.txt')
    analizer.analizar()
