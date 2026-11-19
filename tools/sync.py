import re,os,sys,shutil,json
from PIL import Image,ImageDraw,ImageFont
# 사용법: python3 sync.py need|build <반코드> "<반 이름>" "<짧은이름>" <라이브 index.html> <저장소 폴더>
mode,code,label,short,live,repo=sys.argv[1:7]
s=open(live,encoding='utf-8').read()
ids=sorted(set(re.findall(r'/_blob/([0-9a-f]{32})',s)))
os.makedirs(f'{repo}/a',exist_ok=True)
have={os.path.splitext(f)[0]:f for f in os.listdir(f'{repo}/a')}
miss=[i for i in ids if i not in have]
if mode=='need':
    print('\n'.join(miss));print('MISSING',len(miss),file=sys.stderr);sys.exit(0)
if miss: sys.exit('missing %d: 먼저 read_asset으로 받아 a/<id>.<확장자> 로 넣기'%len(miss))
s=re.sub(r'/_blob/([0-9a-f]{32})',lambda m:'a/'+have[m.group(1)],s)
head=f'''<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="{short}">
<link rel="manifest" href="manifest.json">
<link rel="apple-touch-icon" href="icon-180.png">
<link rel="icon" href="icon-192.png">
'''
assert s.count('</title>')==1
s=s.replace('</title>','</title>\n'+head,1)
tail='''<div id="pwaTip" style="display:none;position:fixed;left:10px;right:10px;bottom:12px;z-index:2147483000;background:#2f5d50;color:#fff;border-radius:14px;padding:12px 14px 12px;font:15px/1.5 -apple-system,sans-serif;box-shadow:0 6px 24px rgba(0,0,0,.3)"><b id="pwaT" style="display:block;font-size:16px;margin-bottom:4px"></b><span id="pwaB"></span><button id="pwaX" type="button" style="position:absolute;right:8px;top:6px;border:0;background:none;color:#fff;font-size:20px">✕</button></div>
<script>(function(){try{if(navigator.storage&&navigator.storage.persist)navigator.storage.persist().catch(function(){})}catch(e){}
try{var ua=navigator.userAgent,ios=/iPhone|iPad|iPod/.test(ua)||(navigator.platform==='MacIntel'&&navigator.maxTouchPoints>1),sa=window.navigator.standalone===true||matchMedia('(display-mode: standalone)').matches;if(sa)return;var k=/KAKAOTALK/i.test(ua),t=document.getElementById('pwaTip'),T=document.getElementById('pwaT'),B=document.getElementById('pwaB');
if(k){T.textContent='⚠️ 카카오톡 안에서는 캐릭터·기록이 저장되지 않아요';B.innerHTML=ios?'오른쪽 아래 <b>공유(⬆) 또는 ⋯</b> → <b>Safari로 열기</b>를 누른 뒤, 홈 화면에 추가해서 써 주세요.':'오른쪽 위 <b>⋮</b> → <b>다른 브라우저로 열기</b>(크롬)를 누른 뒤, 홈 화면에 추가해서 써 주세요.'}
else if(ios){var n=0;try{n=+localStorage.getItem('pwaN')||0;localStorage.setItem('pwaN',n+1)}catch(e){}T.textContent='📲 홈 화면에 추가해서 쓰세요';B.innerHTML='아래 <b>공유(⬆)</b> 버튼 → <b>홈 화면에 추가</b> → <b>추가</b>. 그 다음부터는 바탕화면 아이콘으로 열면 캐릭터·기록이 안전하게 저장돼요.'}
else return;t.style.display='block';document.getElementById('pwaX').onclick=function(){t.style.display='none'}}catch(e){}})();</script>
'''
i=s.rfind('</body>')
s=s[:i]+tail+s[i:]
open(f'{repo}/index.html','w',encoding='utf-8').write(s)
json.dump({"name":label+" 수업 필기장","short_name":short,"start_url":"./","scope":"./","display":"standalone","background_color":"#2f5d50","theme_color":"#2f5d50","icons":[{"src":"icon-192.png","sizes":"192x192","type":"image/png"},{"src":"icon-512.png","sizes":"512x512","type":"image/png"}]},open(f'{repo}/manifest.json','w'),ensure_ascii=False)
F='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
for sz in (180,192,512):
    if os.path.exists(f'{repo}/icon-{sz}.png'): continue
    im=Image.new('RGB',(sz,sz),'#2f5d50');d=ImageDraw.Draw(im)
    d.rounded_rectangle([sz*.06,sz*.06,sz*.94,sz*.94],radius=sz*.12,outline='#c8a46a',width=max(3,sz//30))
    f=ImageFont.truetype(F,int(sz*.30),index=1)
    w=d.textbbox((0,0),short,font=f);d.text(((sz-(w[2]-w[0]))/2-w[0],(sz-(w[3]-w[1]))/2-w[1]-sz*.04),short,font=f,fill='#fff')
    f2=ImageFont.truetype(F,int(sz*.11),index=1);t='필기장';w=d.textbbox((0,0),t,font=f2)
    d.text(((sz-(w[2]-w[0]))/2-w[0],sz*.70),t,font=f2,fill='#f3d27a')
    im.save(f'{repo}/icon-{sz}.png')
open(f'{repo}/.nojekyll','w').close()
print('ok',len(ids),'assets')
