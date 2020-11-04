from selenium import webdriver

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import getpass 
  


username=input("e-mail >>> ")
try: 
    password = getpass.getpass(prompt='password>>>') 
except Exception as error: 
    print('ERROR', error) 
    quit()
materia=input("materia >>> ")
data=input("data appello >>> ")

if( username=='' or password=='' or materia=='' or data==''):
    print('uno dei valori è vuoto')
    quit()
d = DesiredCapabilities.CHROME
d["goog:loggingPrefs"] = { 'performance':'ALL' }


options = webdriver.ChromeOptions()
options.add_argument("--incognito")

driver = webdriver.Chrome(desired_capabilities=d , options=options)
driver.get('https://almaesami.unibo.it/almaesami/welcome.htm')

selector_as='body > div.contenutiCol > div.corpo > p:nth-child(2) > a'
accesso_studenti=driver.find_element_by_css_selector(selector_as)
accesso_studenti.click()

xpath_credenziali_unibo='//*[@id="bySelection"]/div[2]/div/span'
invia=driver.find_element_by_xpath(xpath_credenziali_unibo)
invia.click()

xpath_u='//*[@id="userNameInput"]'
xpath_p='//*[@id="passwordInput"]'
xpath_accedi='//*[@id="submitButton"]'



us=driver.find_element_by_xpath(xpath_u)
us.send_keys(username)

ps=driver.find_element_by_xpath(xpath_p)
ps.send_keys(password)


invia=driver.find_element_by_xpath(xpath_accedi)
invia.click()

verbalizzati=0
css_table='#tabella-af-list-studente'
table =  driver.find_element_by_css_selector(css_table)
i=2
trovato=0
for row in table.find_elements_by_tag_name("tr")[1:]:
    nome=driver.find_element_by_xpath('//*[@id="tabella-af-list-studente"]/tbody/tr['+str(i)+']/td[3]')
    if( materia.lower() in nome.text.lower()):
        verbalizzato=driver.find_element_by_xpath('//*[@id="tabella-af-list-studente"]/tbody/tr['+str(i)+']/td[6]')

        if ( verbalizzato.text>'verbalizzato'):
            #non è corretto, ho preso il verbalizzato
            verbalizzati=verbalizzati+1
        else:
            trovato=1
            break
    i=i+1
if(trovato==0):
    print('Non ho trovato la materia!')
    quit()
xpath_piu='//*[@id="tabella-af-list-studente"]/tbody/tr['+str(i)+']/td[1]/a'
piu=driver.find_element_by_xpath(xpath_piu)
piu.click()

i=i+1
table =  driver.find_element_by_xpath('//*[@id="tabella-af-list-studente"]/tbody/tr['+str(i)+']/td[2]/div/table/tbody')
prenotato=0
for row in table.find_elements_by_tag_name("tr")[1:]:
    if( 'prenotate' in row.text):
       prenotato=prenotato+row.text.count('prenotato')

if( verbalizzati>0):
    n=i+verbalizzati
else:
    n=i+prenotato#+1
   
selector_tab='//*[@id="tabella-af-list-studente"]/tbody/tr['+str(n)+']/td[2]/div/table/tbody'
tabella = driver.find_element_by_xpath(selector_tab)
i=0
l=len(tabella.find_elements_by_tag_name("tr"))
trovato=0
for row in tabella.find_elements_by_tag_name("tr")[1:]:
    if(trovato==1):
        break
    raw=row.text.split('Prenota')
    for el in raw[0:]:
        if(data in el):
            
            trovato=1
            break
    i=i+1 
if(trovato==0):
    print("non ho trovato la data")
    quit()
riga=i+1

xpath_prenota='//*[@id="tabella-af-list-studente"]/tbody/tr['+str(n)+']/td[2]/div/table/tbody/tr['+str(int(riga))+']/td[2]/a'

prenota=driver.find_element_by_xpath(xpath_prenota)
prenota.click()

prenota=driver.find_element_by_xpath('//*[@id="prenota"]')
prenota.click()


#controllare se c'è questionario
xpath_questionario='/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div[2]/h1'
elem = driver.find_elements_by_xpath(xpath_questionario)
if(len(elem) > 0):
    elem = driver.find_element_by_xpath(xpath_questionario)
    source_code = elem.get_attribute("outerHTML")
    if('Compilazione questionario di valutazione' in source_code):
        j=1
        ##1
        xpath_seleziona_valutazione_insegnamento='//*[@id="modelMap\'questionari\'.tutti0.domandeValutazione0.rispostaNumerica3"]'
        invia=driver.find_element_by_xpath(xpath_seleziona_valutazione_insegnamento)
        invia.click()
        ##2
        xpath_seleziona_valutazione_insegnamento='//*[@id="modelMap\'questionari\'.tutti0.domandeValutazione1.rispostaNumerica3"]'
        invia=driver.find_element_by_xpath(xpath_seleziona_valutazione_insegnamento)
        invia.click()
        ##3
        xpath_seleziona_valutazione_insegnamento='//*[@id="modelMap\'questionari\'.tutti0.domandeValutazione2.rispostaNumerica3"]'
        invia=driver.find_element_by_xpath(xpath_seleziona_valutazione_insegnamento)
        invia.click()
        ##4
        xpath_seleziona_valutazione_insegnamento='//*[@id="modelMap\'questionari\'.tutti0.domandeValutazione3.rispostaNumerica3"]'
        invia=driver.find_element_by_xpath(xpath_seleziona_valutazione_insegnamento)
        invia.click()
        ##5
        xpath_seleziona_valutazione_insegnamento='//*[@id="modelMap\'questionari\'.tutti0.domandeValutazione4.rispostaNumerica3"]'
        invia=driver.find_element_by_xpath(xpath_seleziona_valutazione_insegnamento)
        invia.click()
        
        xpath_valutazione_docenza='//*[@id="modelMap\'questionari\'.tutti1.domandeValutazione0.rispostaNumerica3"]'
        invia=driver.find_element_by_xpath(xpath_valutazione_docenza)
        invia.click()

        xpath_valutazione_frequenza='//*[@id="modelMap\'questionari\'.domandeSuFrequenza0.risposteMultiple1"]'
        invia=driver.find_element_by_xpath(xpath_valutazione_frequenza)
        invia.click()
    
        xpath_prenota='//*[@id="prenota"]'
        invia=driver.find_element_by_xpath(xpath_prenota)
        invia.click()
    
class_banner='banner'
esito = driver.find_element_by_class_name(class_banner).text
print (esito)
