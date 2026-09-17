import sys,re,pathlib
src=pathlib.Path(__file__).parent; out=src.parent
STAR='<svg viewBox="0 0 24 24"><path d="M12 2l2.9 6.9 7.1.6-5.4 4.7 1.6 7L12 17.3 5.8 21.2l1.6-7L2 9.5l7.1-.6z"/></svg>'
STARS='<div class="tp-stars">'+''.join(f'<i>{STAR}</i>' for _ in range(5))+'</div>'
EXTRA={}
imp=[30,40,50,60,70,80,90,100,110,120,130,140,150,160,200,250,300,350,400,500]

TAN=2.70
def rata(c,y,t=TAN):
    r=t/100/12;n=y*12;return c*r/(1-(1+r)**-n)
def eur(x,dec=0):
    s=f"{x:,.{dec}f}";return s.replace(',','X').replace('.',',').replace('X','.')
top={50,100,150,200}
newp={20,25,35,45,170,180}
allk=sorted(set(imp)|newp)
def fascia(k): return 'a' if k<=100 else ('b' if k<=200 else 'c')
cards=[]
for k in allk:
    c=k*1000;r30=rata(c,30);inc=r30/0.33
    badge='<span class="badge">Più cercato</span>' if k in top else ''
    cls='imp'+(' new' if k in newp else '')
    href=("#" if k in newp else f"https://www.euroansa.it/calcola-la-tua-rata/mutuo-{k}-mila-euro")
    cards.append(f'<a class="{cls}" data-f="{fascia(k)}" href="{href}"><span class="imp-k">Mutuo {eur(c)} €</span>{badge}<span class="imp-r">da <b>{eur(r30,2)} €</b> al mese</span><span class="imp-m">in 30 anni · reddito consigliato {eur(round(inc,-1))} €</span><span class="imp-go">Calcola la rata <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m9 18 6-6-6-6"/></svg></span></a>')
EXTRA['CARDS']='\n'.join(cards)
rows=[]
for k in imp:
    c=k*1000
    tds=''.join(f'<td><span class="v-r">{eur(rata(c,y),2)} €</span><span class="v-i">{eur(round(rata(c,y)/0.33,-1))} €</span></td>' for y in (10,15,20,25,30))
    rows.append(f'<tr><th scope="row"><a href="https://www.euroansa.it/calcola-la-tua-rata/mutuo-{k}-mila-euro">Mutuo {eur(c)} €</a></th>{tds}</tr>')
EXTRA['RATE_ROWS']='\n'.join(rows)
items=','.join('{"@type":"ListItem","position":%d,"name":"Mutuo %s euro","url":"https://www.euroansa.it/calcola-la-tua-rata/mutuo-%d-mila-euro"}'%(i+1,eur(k*1000),k) for i,k in enumerate(imp))
EXTRA['ITEMLIST']=items
EXTRA['NIMP']=str(len(imp))

def build(page,title,foot_hub=False,foot_guide=False):
    body=(src/page).read_text(); css=(src/'base.css').read_text()
    fi=('<li class="hl"><a href="mutuo-importi-hub.html">Tutti gli importi</a></li>' if foot_hub else '')+''.join(f'<li><a href="#">Mutuo {k}.000€</a></li>' for k in imp if foot_hub or k not in (30,110,350))
    fg='<li class="hl"><a href="consulente-del-credito.html">Consulente del credito</a></li>' if foot_guide else ''
    parts={'HEADER':(src/'header.html').read_text(),'REVIEWS':(src/'reviews.html').read_text(),'FOOTER':(src/'footer.html').read_text()}
    for k,v in parts.items(): body=body.replace('{{'+k+'}}',v)
    for k,v in EXTRA.items(): body=body.replace('{{'+k+'}}',v)
    body=body.replace('{{BASECSS}}',css).replace('{{STARS}}',STARS).replace('{{MOCKTITLE}}',title).replace('{{FOOT_IMPORTI}}',fi).replace('{{FOOT_GUIDE}}',fg)
    left=re.findall(r'\{\{[A-Z_]+\}\}',body)
    if left: print('placeholder non risolti',set(left))
    (out/page).write_text(body); print('ok',page,len(body))
build('consulente-del-credito.html','Pagina informativa Consulente del credito',foot_guide=True)
if (src/'mutuo-importi-hub.html').exists(): build('mutuo-importi-hub.html','Pagina hub importi mutuo',foot_hub=True)

# ---- Hub: generated blocks ----
