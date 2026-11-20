from PIL import Image
import numpy as np, sys
A=Image.open('pu005.jpg').convert('RGB');B=Image.open('pu006.jpg').convert('RGB')
a=np.asarray(A,dtype=float);b=np.asarray(B,dtype=float)
D=146;Y0,Y1=100,420;AX0=27;BX1=498;F=60
BA,BB,GAP_A,GAP_B,BG=[int(v) for v in sys.argv[2:7]]
def bot_a(x): return BG if x>=GAP_A else BA
def bot_b(x): return BG if x<GAP_B else BB
La=a[Y0:Y1,AX0:532]; Rb=b[Y0:Y1,D:BX1]
w=np.linspace(0,1,F)[None,:,None]
mix=a[Y0:Y1,532-F:532]*(1-w)+b[Y0:Y1,D-F:D]*w
C=np.concatenate([np.concatenate([La[:,:-F],mix],axis=1),Rb],axis=1)
tot=(532-AX0)+BX1
c=np.asarray(Image.fromarray(C.clip(0,255).astype('uint8')).resize((tot,Y1-Y0),Image.LANCZOS),dtype=float)
na=a.copy();nb=b.copy()
def ytop_a(x): return max(int(152-(x-25)*0.77)+8,125) if x<95 else 126
def ytop_b(x): return int(100+(x-418)*0.62)+8 if x>418 else 126
for x in range(AX0,532):
    yt=ytop_a(x); yb=bot_a(x); na[yt:yb,x]=c[yt-Y0:yb-Y0,x-AX0]
for x in range(0,BX1):
    yt=ytop_b(x); yb=bot_b(x); nb[yt:yb,x]=c[yt-Y0:yb-Y0,532-AX0+x]
S=sys.argv[1]
Image.fromarray(na.clip(0,255).astype('uint8')).save(S+'/pu005_pano.jpg',quality=93)
Image.fromarray(nb.clip(0,255).astype('uint8')).save(S+'/pu006_pano.jpg',quality=93)
o=Image.new('RGB',(1064,740));o.paste(Image.open(S+'/pu005_pano.jpg'),(0,0));o.paste(Image.open(S+'/pu006_pano.jpg'),(532,0));o.save(S+'/pano.png')
o.crop((330,340,800,440)).resize((940,200),Image.LANCZOS).save(S+'/bas.png')
