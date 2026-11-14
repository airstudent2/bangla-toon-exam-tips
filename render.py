#!/usr/bin/env python3
"""
Bangla Toon Flat — Animation Renderer
পরীক্ষায় ১০০ নম্বর পাওয়ার ৩টি স্মার্ট টিপস!
1080×1920 | 9:16 | 30fps | ~60s
"""
import os, sys, math, subprocess, shutil, base64, tempfile
from pathlib import Path

# Dependencies are installed in GitHub Actions workflow

# ── constants ─────────────────────────────────────────────────
W, H   = 1080, 1920
FPS    = 30
TOTAL  = 60.30
NF     = int(TOTAL * FPS) + 2

ALPONA = '#F6F1E7'; TERRACOTTA = '#C8643B'; MARIGOLD = '#F2A900'
LAL    = '#B3202A'; TEAL = '#1F7A74'; JUTE = '#D9B88F'
INK    = '#1B1A22'; NIGHT = '#1E2A4A'
BOARD  = '#1A4525'; DESK  = '#7A4A28'; SKY = '#87CEEB'
PAPER  = '#FAF8F0'; SKR   = '#D4956A'; SKS = '#C07850'
HR_R   = '#1B1A22'; HR_S  = '#2A2010'

# ── timing data ────────────────────────────────────────────────
SEG = [
  {"id":1,"sp":"Narrator","s":0.00,"e":7.30,"words":[
    {"w":"হাঁহ!","s":0.00,"e":0.70},{"w":"এত","s":0.85,"e":1.15},
    {"w":"পড়াশোনা","s":1.16,"e":1.70},{"w":"করেও","s":1.71,"e":2.10},
    {"w":"পরীক্ষায়","s":2.20,"e":2.80},{"w":"মাত্র","s":2.81,"e":3.25},
    {"w":"৫০","s":3.26,"e":3.85},{"w":"নম্বর!","s":3.86,"e":4.50},
    {"w":"অথচ","s":4.90,"e":5.30},{"w":"তার","s":5.31,"e":5.55},
    {"w":"বন্ধু","s":5.56,"e":5.90},{"w":"সুমন","s":5.91,"e":6.35},
    {"w":"পেল","s":6.36,"e":6.65},{"w":"১০০!","s":6.66,"e":7.30},
  ]},
  {"id":2,"sp":"Rahul","s":7.50,"e":13.00,"words":[
    {"w":"এত","s":7.50,"e":7.75},{"w":"পড়াশোনা","s":7.76,"e":8.30},
    {"w":"করেও","s":8.31,"e":8.70},{"w":"মাত্র","s":8.80,"e":9.20},
    {"w":"৫০","s":9.21,"e":9.75},{"w":"নম্বর?","s":9.76,"e":10.30},
    {"w":"তুই","s":10.50,"e":10.80},{"w":"এত","s":10.81,"e":11.05},
    {"w":"কম","s":11.06,"e":11.35},{"w":"পড়েও","s":11.36,"e":11.75},
    {"w":"১০০","s":11.80,"e":12.20},{"w":"পেলি","s":12.21,"e":12.55},
    {"w":"কীভাবে?","s":12.56,"e":13.00},
  ]},
  {"id":3,"sp":"Suman","s":13.10,"e":17.80,"words":[
    {"w":"হা!","s":13.51,"e":14.10},{"w":"কারণ","s":14.30,"e":14.75},
    {"w":"আমি","s":14.76,"e":15.05},{"w":"শুধু","s":15.06,"e":15.40},
    {"w":"পড়ি","s":15.41,"e":15.75},{"w":"না,","s":15.76,"e":16.10},
    {"w":"স্মার্টভাবে","s":16.20,"e":17.15},{"w":"পড়ি।","s":17.16,"e":17.80},
  ]},
  {"id":4,"sp":"Suman","s":18.20,"e":24.00,"words":[
    {"w":"প্রথমত,","s":18.20,"e":18.90},{"w":"শুধু","s":19.00,"e":19.35},
    {"w":"বই","s":19.36,"e":19.65},{"w":"পড়ে","s":19.66,"e":19.95},
    {"w":"যাস","s":19.96,"e":20.25},{"w":"না।","s":20.26,"e":20.60},
    {"w":"বই","s":20.80,"e":21.05},{"w":"বন্ধ","s":21.06,"e":21.40},
    {"w":"করে","s":21.41,"e":21.70},{"w":"নিজে","s":21.75,"e":22.05},
    {"w":"নিজে","s":22.06,"e":22.40},{"w":"উত্তর","s":22.41,"e":22.80},
    {"w":"মনে","s":22.81,"e":23.10},{"w":"করার","s":23.11,"e":23.40},
    {"w":"চেষ্টা","s":23.41,"e":23.75},{"w":"কর।","s":23.76,"e":24.00},
  ]},
  {"id":5,"sp":"Suman","s":24.50,"e":29.00,"words":[
    {"w":"দ্বিতীয়ত,","s":24.50,"e":25.30},{"w":"আগের","s":25.40,"e":25.80},
    {"w":"বছরের","s":25.81,"e":26.25},{"w":"প্রশ্নপত্র","s":26.26,"e":27.05},
    {"w":"সময়","s":27.10,"e":27.55},{"w":"ধরে","s":27.56,"e":27.90},
    {"w":"প্র্যাকটিস","s":27.91,"e":28.60},{"w":"কর।","s":28.61,"e":29.00},
  ]},
  {"id":6,"sp":"Suman","s":29.40,"e":37.80,"words":[
    {"w":"তৃতীয়ত,","s":29.40,"e":30.15},{"w":"পরীক্ষার","s":30.25,"e":30.80},
    {"w":"হলে","s":30.81,"e":31.15},{"w":"আগে","s":31.20,"e":31.55},
    {"w":"ভালো","s":31.56,"e":31.95},{"w":"জানা","s":31.96,"e":32.35},
    {"w":"প্রশ্নগুলোর","s":32.36,"e":33.15},{"w":"উত্তর","s":33.16,"e":33.55},
    {"w":"লিখবি।","s":33.56,"e":34.20},{"w":"আর","s":34.40,"e":34.70},
    {"w":"শেষে","s":34.71,"e":35.15},{"w":"সময়","s":35.20,"e":35.65},
    {"w":"রেখে","s":35.66,"e":36.05},{"w":"সব","s":36.06,"e":36.35},
    {"w":"উত্তর","s":36.36,"e":36.75},{"w":"চেক","s":36.76,"e":37.20},
    {"w":"করবি।","s":37.21,"e":37.80},
  ]},
  {"id":7,"sp":"Narrator","s":38.00,"e":44.50,"words":[
    {"w":"রাহুল","s":38.00,"e":38.45},{"w":"এবার","s":38.46,"e":38.80},
    {"w":"এই","s":38.81,"e":39.05},{"w":"তিনটি","s":39.06,"e":39.45},
    {"w":"নিয়ম","s":39.46,"e":39.85},{"w":"মেনে","s":39.86,"e":40.25},
    {"w":"প্রস্তুতি","s":40.26,"e":40.85},{"w":"নিল।","s":40.86,"e":41.35},
    {"w":"পরের","s":41.50,"e":41.90},{"w":"পরীক্ষায়","s":41.91,"e":42.50},
    {"w":"তার","s":42.51,"e":42.75},{"w":"নম্বর","s":42.76,"e":43.15},
    {"w":"অনেকটাই","s":43.16,"e":43.80},{"w":"বেড়ে","s":43.81,"e":44.10},
    {"w":"গেল!","s":44.11,"e":44.50},
  ]},
  {"id":8,"sp":"Rahul","s":44.70,"e":49.90,"words":[
    {"w":"ওয়াও!","s":44.70,"e":45.40},{"w":"এবার","s":45.50,"e":45.90},
    {"w":"বুঝেছি,","s":45.91,"e":46.50},{"w":"শুধু","s":46.60,"e":47.00},
    {"w":"পড়লেই","s":47.01,"e":47.50},{"w":"হয়","s":47.51,"e":47.75},
    {"w":"না,","s":47.76,"e":48.05},{"w":"সঠিক","s":48.15,"e":48.60},
    {"w":"পদ্ধতিতে","s":48.61,"e":49.15},{"w":"পড়তে","s":49.16,"e":49.50},
    {"w":"হয়।","s":49.51,"e":49.90},
  ]},
  {"id":9,"sp":"Narrator","s":50.00,"e":60.30,"words":[
    {"w":"মনে","s":50.00,"e":50.30},{"w":"রেখো,","s":50.31,"e":50.80},
    {"w":"ফুল","s":50.90,"e":51.25},{"w":"মার্কসের","s":51.26,"e":51.85},
    {"w":"কোনো","s":51.86,"e":52.20},{"w":"ম্যাজিক","s":52.21,"e":52.75},
    {"w":"নেই।","s":52.76,"e":53.25},{"w":"নিয়মিত","s":53.40,"e":53.95},
    {"w":"প্র্যাকটিস,","s":53.96,"e":54.70},{"w":"নিজের","s":54.80,"e":55.20},
    {"w":"স্মৃতি","s":55.21,"e":55.65},{"w":"যাচাই","s":55.66,"e":56.15},
    {"w":"আর","s":56.20,"e":56.45},{"w":"সময়ের","s":56.46,"e":56.90},
    {"w":"সঠিক","s":56.91,"e":57.30},{"w":"ব্যবহারই","s":57.31,"e":58.00},
    {"w":"তোমাকে","s":58.05,"e":58.45},{"w":"ভালো","s":58.46,"e":58.85},
    {"w":"ফলের","s":58.86,"e":59.20},{"w":"পথে","s":59.21,"e":59.50},
    {"w":"এগিয়ে","s":59.51,"e":59.85},{"w":"দেবে।","s":59.86,"e":60.30},
  ]},
]

# ── utils ──────────────────────────────────────────────────────
def lerp(a,b,t): return a+(b-a)*max(0,min(1,t))
def ease(t): t=max(0,min(1,t)); return t*t*(3-2*t)
def dk(c,f=0.2):
    r,g,b=int(c[1:3],16),int(c[3:5],16),int(c[5:7],16)
    return f'#{max(0,int(r*(1-f))):02x}{max(0,int(g*(1-f))):02x}{max(0,int(b*(1-f))):02x}'
def breath(t,a=4): return math.sin(t*math.pi*2*0.38)*a
def do_blink(t): return (t%3.6)<0.09

def mouth_at(t):
    for seg in SEG:
        for w in seg['words']:
            if w['s']<=t<=w['e']:
                word=w['w']
                for c in word:
                    if c in 'মবপফভ': return 'mm', seg['sp']
                    if c in 'আঅাো': return 'aa', seg['sp']
                    if c in 'ইিীএেৈ': return 'ee', seg['sp']
                    if c in 'উুূওৌ': return 'oo', seg['sp']
                return 'aa', seg['sp']
    return 'closed', None

def caption_at(t):
    for seg in SEG:
        ws=seg['words']
        if not ws or t>ws[-1]['e']+0.4 or t<ws[0]['s']-0.1: continue
        ci=0
        for i,w in enumerate(ws):
            if w['s']<=t: ci=i
        st=max(0,ci-1); en=min(len(ws),st+4)
        chunk=ws[st:en]
        if chunk and chunk[0]['s']-0.1<=t<=chunk[-1]['e']+0.3:
            hl=next((w['w'] for w in chunk if w['s']<=t<=w['e']),None)
            return ' '.join(w['w'] for w in chunk), hl
    return '',None

def scene_at(t):
    if t<7.3: return 1
    elif t<13.1: return 2
    elif t<18.2: return 3
    elif t<24.1: return 4
    elif t<29.4: return 5
    elif t<38.0: return 6
    elif t<44.7: return 7
    elif t<50.0: return 8
    else: return 9

# ── mouth drawing ──────────────────────────────────────────────
def _mouth(p, mx, my, ms, ex, s):
    bc='#8B1A1A'
    if ms=='aa':
        p.append(f'<ellipse cx="{mx}" cy="{my+2*s}" rx="{13*s}" ry="{10*s}" fill="{bc}" stroke="{INK}" stroke-width="{3*s}"/>')
        p.append(f'<ellipse cx="{mx}" cy="{my+4*s}" rx="{9*s}" ry="{5*s}" fill="#C45050"/>')
    elif ms=='ee':
        p.append(f'<path d="M {mx-15*s},{my} Q {mx},{my+9*s} {mx+15*s},{my}" fill="{bc}" stroke="{INK}" stroke-width="{2.5*s}"/>')
    elif ms=='oo':
        p.append(f'<ellipse cx="{mx}" cy="{my+2*s}" rx="{8*s}" ry="{12*s}" fill="{bc}" stroke="{INK}" stroke-width="{2.5*s}"/>')
    elif ms=='mm':
        p.append(f'<line x1="{mx-12*s}" y1="{my}" x2="{mx+12*s}" y2="{my}" stroke="{INK}" stroke-width="{4*s}" stroke-linecap="round"/>')
    else:  # closed
        if ex=='happy' or ex=='excited':
            p.append(f'<path d="M {mx-14*s},{my-3*s} Q {mx},{my+9*s} {mx+14*s},{my-3*s}" fill="{bc}" stroke="{INK}" stroke-width="{3*s}" stroke-linecap="round"/>')
        elif ex in ('sad','annoyed','thinking'):
            p.append(f'<path d="M {mx-12*s},{my+4*s} Q {mx},{my-4*s} {mx+12*s},{my+4*s}" fill="none" stroke="{INK}" stroke-width="{3*s}" stroke-linecap="round"/>')
        else:
            p.append(f'<path d="M {mx-10*s},{my} Q {mx},{my+4*s} {mx+10*s},{my}" fill="none" stroke="{INK}" stroke-width="{3*s}" stroke-linecap="round"/>')

# ── eyes drawing ───────────────────────────────────────────────
BROWS = {
    'normal':    {'bl':-2, 'br':2,  'lid':0.0,  'pdy':0},
    'happy':     {'bl':-7, 'br':7,  'lid':0.25, 'pdy':-1},
    'sad':       {'bl':12, 'br':-12,'lid':0.42, 'pdy':2},
    'surprised': {'bl':-12,'br':12, 'lid':-0.1, 'pdy':-2},
    'thinking':  {'bl':6,  'br':-4, 'lid':0.28, 'pdy':-2},
    'annoyed':   {'bl':15, 'br':-15,'lid':0.48, 'pdy':0},
    'confident': {'bl':-4, 'br':4,  'lid':0.15, 'pdy':0},
    'excited':   {'bl':-10,'br':10, 'lid':0.0,  'pdy':-3},
    'explaining':{'bl':-3, 'br':3,  'lid':0.08, 'pdy':-1},
}

def _eyes(p, cx, hy, s, ex, blink, skin, hr, eye_ox=20):
    ec=BROWS.get(ex, BROWS['normal'])
    for ox, bk in [(-eye_ox, ec['bl']), (eye_ox, ec['br'])]:
        ex2=cx+ox*s; ey=hy+5*s
        p.append(f'<circle cx="{ex2}" cy="{ey}" r="{8*s}" fill="white" stroke="{INK}" stroke-width="{2.5*s}"/>')
        if blink:
            p.append(f'<path d="M {ex2-8*s},{ey} Q {ex2},{ey+5*s} {ex2+8*s},{ey}" fill="{skin}" stroke="{INK}" stroke-width="{2*s}"/>')
        else:
            py=ey+ec['pdy']*s
            p.append(f'<circle cx="{ex2}" cy="{py}" r="{5*s}" fill="{INK}"/>')
            p.append(f'<circle cx="{ex2+2*s}" cy="{py-2*s}" r="{2*s}" fill="white"/>')
            if ec['lid']>0:
                lh=8*ec['lid']*s
                p.append(f'<rect x="{ex2-8*s}" y="{ey-8*s}" width="{16*s}" height="{lh+1}" rx="{2*s}" fill="{skin}"/>')
        # Brow
        bv=bk*s*0.11
        bx1,by1=ex2-11*s, hy-10*s+(bv if ox<0 else -bv)
        bx2,by2=ex2+11*s, hy-10*s+(-bv if ox<0 else bv)
        p.append(f'<path d="M {bx1},{by1} Q {ex2},{hy-10*s} {bx2},{by2}" fill="none" stroke="{hr}" stroke-width="{4.5*s}" stroke-linecap="round"/>')

# ── character: Rahul ───────────────────────────────────────────
def rahul(cx, cy, s=3.0, ex='normal', ms='closed', arm='rest', blink=False):
    p=[]
    SH='#C8643B'; SHL='#E07848'; PA='#1E1E30'; SHO='#111118'
    # shadow
    p.append(f'<ellipse cx="{cx}" cy="{cy+210*s}" rx="{60*s}" ry="{11*s}" fill="#00000018"/>')
    # legs
    for dx in (-20,3):
        p.append(f'<rect x="{cx+dx*s}" y="{cy+128*s}" width="{17*s}" height="{68*s}" rx="{5*s}" fill="{PA}" stroke="{INK}" stroke-width="{4.5*s}"/>')
    # shoes
    for dx in (-14,14):
        p.append(f'<ellipse cx="{cx+dx*s}" cy="{cy+200*s}" rx="{18*s}" ry="{8*s}" fill="{SHO}" stroke="{INK}" stroke-width="{3.5*s}"/>')
    # back arm L
    _arm_r(p, cx, cy, s, arm, -1, SKR, SH)
    # torso
    p.append(f'<path d="M {cx-32*s},{cy+55*s} Q {cx-34*s},{cy+90*s} {cx-30*s},{cy+130*s} L {cx+30*s},{cy+130*s} Q {cx+34*s},{cy+90*s} {cx+32*s},{cy+55*s} Z" fill="{SH}" stroke="{INK}" stroke-width="{5*s}"/>')
    for i in range(4):
        lx=cx+(-24+i*16)*s
        p.append(f'<line x1="{lx}" y1="{cy+60*s}" x2="{lx}" y2="{cy+128*s}" stroke="{SHL}" stroke-width="{2.5*s}" opacity="0.5"/>')
    for i in range(3):
        ly=cy+(72+i*22)*s
        p.append(f'<line x1="{cx-30*s}" y1="{ly}" x2="{cx+30*s}" y2="{ly}" stroke="{SHL}" stroke-width="{2*s}" opacity="0.4"/>')
    p.append(f'<path d="M {cx-14*s},{cy+55*s} L {cx},{cy+70*s} L {cx+14*s},{cy+55*s}" fill="{ALPONA}" stroke="{INK}" stroke-width="{3.5*s}" stroke-linejoin="round"/>')
    # front arm R
    _arm_r(p, cx, cy, s, arm, 1, SKR, SH)
    # neck
    p.append(f'<rect x="{cx-9*s}" y="{cy+42*s}" width="{18*s}" height="{18*s}" rx="{5*s}" fill="{SKR}" stroke="{INK}" stroke-width="{4.5*s}"/>')
    # head
    hy=cy-50*s
    p.append(f'<ellipse cx="{cx}" cy="{hy}" rx="{46*s}" ry="{48*s}" fill="{SKR}" stroke="{INK}" stroke-width="{5.5*s}"/>')
    # ears
    for dx in (-45,45):
        p.append(f'<circle cx="{cx+dx*s}" cy="{hy+8*s}" r="{9*s}" fill="{SKR}" stroke="{INK}" stroke-width="{4*s}"/>')
    # hair
    p.append(f'<path d="M {cx-44*s},{hy+6*s} Q {cx-48*s},{hy-28*s} {cx-26*s},{hy-50*s} Q {cx-10*s},{hy-62*s} {cx+10*s},{hy-62*s} Q {cx+26*s},{hy-62*s} {cx+44*s},{hy-50*s} Q {cx+48*s},{hy-28*s} {cx+44*s},{hy+6*s}" fill="{HR_R}" stroke="{INK}" stroke-width="{3.5*s}"/>')
    p.append(f'<path d="M {cx-18*s},{hy-58*s} Q {cx-5*s},{hy-72*s} {cx+5*s},{hy-62*s}" fill="{HR_R}" stroke="{INK}" stroke-width="{2.5*s}"/>')
    p.append(f'<path d="M {cx+5*s},{hy-62*s} Q {cx+18*s},{hy-74*s} {cx+28*s},{hy-55*s}" fill="{HR_R}" stroke="{INK}" stroke-width="{2.5*s}"/>')
    # cheeks
    for dx in (-29,29):
        p.append(f'<circle cx="{cx+dx*s}" cy="{hy+16*s}" r="{12*s}" fill="#E8A09055"/>')
    # eyes
    _eyes(p, cx, hy, s, ex, blink, SKR, HR_R)
    # nose
    p.append(f'<path d="M {cx-4*s},{hy+18*s} Q {cx+1*s},{hy+25*s} {cx+5*s},{hy+18*s}" fill="none" stroke="{INK}" stroke-width="{2.8*s}" stroke-linecap="round"/>')
    # mouth
    _mouth(p, cx, hy+30*s, ms, ex, s)
    return '\n'.join(p)

def _arm_r(p, cx, cy, s, arm, sign, sk, sh):
    sx=cx+sign*32*s; sy=cy+62*s
    if arm=='celebrate':
        ex=cx+sign*52*s; ey=cy-10*s
        p.append(f'<path d="M {sx},{sy} Q {cx+sign*58*s},{cy+28*s} {ex},{ey}" fill="none" stroke="{sh}" stroke-width="{22*s}" stroke-linecap="round"/>')
        p.append(f'<circle cx="{ex}" cy="{ey}" r="{13*s}" fill="{sk}" stroke="{INK}" stroke-width="{3*s}"/>')
    elif arm=='gesture' and sign==1:
        ex=cx+85*s; ey=cy+50*s
        p.append(f'<path d="M {sx},{sy} Q {cx+65*s},{cy+55*s} {ex},{ey}" fill="none" stroke="{sh}" stroke-width="{22*s}" stroke-linecap="round"/>')
        p.append(f'<circle cx="{ex}" cy="{ey}" r="{13*s}" fill="{sk}" stroke="{INK}" stroke-width="{3*s}"/>')
    elif arm=='hold_paper':
        ex=cx+sign*55*s; ey=cy+110*s
        p.append(f'<path d="M {sx},{sy} Q {cx+sign*58*s},{cy+78*s} {ex},{ey}" fill="none" stroke="{sh}" stroke-width="{22*s}" stroke-linecap="round"/>')
        p.append(f'<circle cx="{ex}" cy="{ey+8*s}" r="{13*s}" fill="{sk}" stroke="{INK}" stroke-width="{3*s}"/>')
    elif arm=='write' and sign==1:
        ex=cx+70*s; ey=cy+120*s
        p.append(f'<path d="M {sx},{sy} Q {cx+60*s},{cy+88*s} {ex},{ey}" fill="none" stroke="{sh}" stroke-width="{22*s}" stroke-linecap="round"/>')
        p.append(f'<circle cx="{ex}" cy="{ey+8*s}" r="{11*s}" fill="{sk}" stroke="{INK}" stroke-width="{3*s}"/>')
        # pencil
        angle=25; rx=ex+8*s; ry=ey+22*s
        p.append(f'<rect x="{rx-3*s}" y="{ry-15*s}" width="{6*s}" height="{22*s}" rx="{2*s}" fill="{MARIGOLD}" stroke="{INK}" stroke-width="{2*s}" transform="rotate({angle},{rx},{ry})"/>')
    elif arm=='sad':
        ex=cx+sign*42*s; ey=cy+128*s
        p.append(f'<path d="M {sx},{sy} Q {cx+sign*44*s},{cy+90*s} {ex},{ey}" fill="none" stroke="{sh}" stroke-width="{22*s}" stroke-linecap="round"/>')
        p.append(f'<circle cx="{ex}" cy="{ey+8*s}" r="{13*s}" fill="{sk}" stroke="{INK}" stroke-width="{3*s}"/>')
    else:  # rest / default
        ex=cx+sign*48*s; ey=cy+138*s
        p.append(f'<path d="M {sx},{sy} Q {cx+sign*52*s},{cy+95*s} {ex},{ey}" fill="none" stroke="{sh}" stroke-width="{22*s}" stroke-linecap="round"/>')
        p.append(f'<circle cx="{ex}" cy="{ey+8*s}" r="{13*s}" fill="{sk}" stroke="{INK}" stroke-width="{3*s}"/>')

# ── character: Suman ───────────────────────────────────────────
def suman(cx, cy, s=3.0, ex='normal', ms='closed', arm='rest', blink=False):
    p=[]
    SH='#E8F0FF'; SH2='#B8CCE8'; PA='#1E3058'; SHO='#1A1A30'; GLS='#888880'
    p.append(f'<ellipse cx="{cx}" cy="{cy+210*s}" rx="{58*s}" ry="{11*s}" fill="#00000018"/>')
    for dx in (-20,3):
        p.append(f'<rect x="{cx+dx*s}" y="{cy+128*s}" width="{17*s}" height="{68*s}" rx="{5*s}" fill="{PA}" stroke="{INK}" stroke-width="{4.5*s}"/>')
    for dx in (-14,14):
        p.append(f'<ellipse cx="{cx+dx*s}" cy="{cy+200*s}" rx="{18*s}" ry="{8*s}" fill="{SHO}" stroke="{INK}" stroke-width="{3.5*s}"/>')
    _arm_s(p, cx, cy, s, arm, -1, SKS, SH)
    p.append(f'<path d="M {cx-32*s},{cy+55*s} Q {cx-34*s},{cy+90*s} {cx-30*s},{cy+130*s} L {cx+30*s},{cy+130*s} Q {cx+34*s},{cy+90*s} {cx+32*s},{cy+55*s} Z" fill="{SH}" stroke="{INK}" stroke-width="{5*s}"/>')
    for i in range(5):
        by=cy+(65+i*14)*s
        p.append(f'<circle cx="{cx}" cy="{by}" r="{2.5*s}" fill="{SH2}"/>')
    p.append(f'<path d="M {cx-14*s},{cy+55*s} L {cx},{cy+68*s} L {cx+14*s},{cy+55*s}" fill="{SH}" stroke="{INK}" stroke-width="{3.5*s}" stroke-linejoin="round"/>')
    _arm_s(p, cx, cy, s, arm, 1, SKS, SH)
    p.append(f'<rect x="{cx-9*s}" y="{cy+42*s}" width="{18*s}" height="{18*s}" rx="{5*s}" fill="{SKS}" stroke="{INK}" stroke-width="{4.5*s}"/>')
    hy=cy-50*s
    p.append(f'<ellipse cx="{cx}" cy="{hy}" rx="{44*s}" ry="{46*s}" fill="{SKS}" stroke="{INK}" stroke-width="{5.5*s}"/>')
    for dx in (-43,43):
        p.append(f'<circle cx="{cx+dx*s}" cy="{hy+8*s}" r="{9*s}" fill="{SKS}" stroke="{INK}" stroke-width="{4*s}"/>')
    p.append(f'<path d="M {cx-43*s},{hy+6*s} Q {cx-46*s},{hy-22*s} {cx-22*s},{hy-45*s} Q {cx-5*s},{hy-54*s} {cx+15*s},{hy-50*s} Q {cx+38*s},{hy-42*s} {cx+43*s},{hy+6*s}" fill="{HR_S}" stroke="{INK}" stroke-width="{3.5*s}"/>')
    p.append(f'<path d="M {cx-5*s},{hy-50*s} Q {cx-10*s},{hy-30*s} {cx-15*s},{hy-10*s}" fill="none" stroke="{ALPONA}" stroke-width="{2.5*s}" stroke-linecap="round" opacity="0.5"/>')
    # glasses
    for ox,ow in [(-40,28),(12,28)]:
        p.append(f'<rect x="{cx+ox*s}" y="{hy-6*s}" width="{ow*s}" height="{21*s}" rx="{5*s}" fill="none" stroke="{GLS}" stroke-width="{3.5*s}"/>')
    p.append(f'<line x1="{cx-12*s}" y1="{hy+5*s}" x2="{cx+12*s}" y2="{hy+5*s}" stroke="{GLS}" stroke-width="{3*s}"/>')
    for ox2,tx2 in [(-40,-50),(40,50)]:
        p.append(f'<line x1="{cx+ox2*s}" y1="{hy+5*s}" x2="{cx+tx2*s}" y2="{hy+10*s}" stroke="{GLS}" stroke-width="{2.5*s}"/>')
    # glass shine
    for ox3 in [-37,15]:
        p.append(f'<path d="M {cx+ox3*s},{hy-3*s} Q {cx+ox3*s+7*s},{hy-5*s} {cx+ox3*s+14*s},{hy-3*s}" fill="none" stroke="white" stroke-width="{2*s}" opacity="0.6"/>')
    for dx in (-27,27):
        p.append(f'<circle cx="{cx+dx*s}" cy="{hy+17*s}" r="{11*s}" fill="#E8A09055"/>')
    _eyes(p, cx, hy, s, ex, blink, SKS, HR_S, eye_ox=26)
    p.append(f'<path d="M {cx-3*s},{hy+18*s} Q {cx+1*s},{hy+24*s} {cx+4*s},{hy+18*s}" fill="none" stroke="{INK}" stroke-width="{2.8*s}" stroke-linecap="round"/>')
    _mouth(p, cx, hy+30*s, ms, ex, s)
    return '\n'.join(p)

def _arm_s(p, cx, cy, s, arm, sign, sk, sh):
    sx=cx+sign*32*s; sy=cy+62*s
    if arm=='explain' and sign==-1:
        ex=cx-72*s; ey=cy+25*s
        p.append(f'<path d="M {sx},{sy} Q {cx-55*s},{cy+42*s} {ex},{ey}" fill="none" stroke="{sh}" stroke-width="{22*s}" stroke-linecap="round"/>')
        p.append(f'<circle cx="{ex}" cy="{ey}" r="{12*s}" fill="{sk}" stroke="{INK}" stroke-width="{3*s}"/>')
        p.append(f'<line x1="{ex}" y1="{ey-12*s}" x2="{ex}" y2="{ey-26*s}" stroke="{sk}" stroke-width="{9*s}" stroke-linecap="round"/>')
    elif arm=='gesture' and sign==1:
        ex=cx+82*s; ey=cy+48*s
        p.append(f'<path d="M {sx},{sy} Q {cx+68*s},{cy+52*s} {ex},{ey}" fill="none" stroke="{sh}" stroke-width="{22*s}" stroke-linecap="round"/>')
        p.append(f'<circle cx="{ex}" cy="{ey}" r="{12*s}" fill="{sk}" stroke="{INK}" stroke-width="{3*s}"/>')
    elif arm=='hold_book':
        ex=cx+sign*58*s; ey=cy+112*s
        p.append(f'<path d="M {sx},{sy} Q {cx+sign*60*s},{cy+82*s} {ex},{ey}" fill="none" stroke="{sh}" stroke-width="{22*s}" stroke-linecap="round"/>')
        p.append(f'<circle cx="{ex}" cy="{ey+8*s}" r="{12*s}" fill="{sk}" stroke="{INK}" stroke-width="{3*s}"/>')
    else:
        ex=cx+sign*46*s; ey=cy+136*s
        p.append(f'<path d="M {sx},{sy} Q {cx+sign*50*s},{cy+92*s} {ex},{ey}" fill="none" stroke="{sh}" stroke-width="{22*s}" stroke-linecap="round"/>')
        p.append(f'<circle cx="{ex}" cy="{ey+8*s}" r="{12*s}" fill="{sk}" stroke="{INK}" stroke-width="{3*s}"/>')

# ── props ──────────────────────────────────────────────────────
def prop_paper(x, y, score, s=1.0):
    p=[]
    try:
        val = int(score)
        sc_col = TEAL if val >= 80 else (MARIGOLD if val >= 60 else LAL)
    except Exception:
        sc_col = MARIGOLD if score == '?' else TEAL
    pw,ph=int(160*s),int(220*s)
    p.append(f'<rect x="{x}" y="{y}" width="{pw}" height="{ph}" rx="{8*s}" fill="{PAPER}" stroke="{INK}" stroke-width="{4*s}"/>')
    for i in range(5):
        p.append(f'<line x1="{x+15*s}" y1="{y+50*s+i*28*s}" x2="{x+pw-15*s}" y2="{y+50*s+i*28*s}" stroke="#C8C0A8" stroke-width="{2*s}"/>')
    cx2=x+pw//2; cy2=y+int(140*s)
    p.append(f'<circle cx="{cx2}" cy="{cy2}" r="{50*s}" fill="{sc_col}" stroke="{INK}" stroke-width="{4*s}"/>')
    fs=int(42*s) if len(str(score))<=2 else int(32*s)
    p.append(f'<text x="{cx2}" y="{cy2+fs//3}" text-anchor="middle" fill="white" font-size="{fs}" font-weight="700" font-family="Hind Siliguri,Lohit Bengali,sans-serif">{score}</text>')
    p.append(f'<text x="{cx2}" y="{cy2+int(68*s)}" text-anchor="middle" fill="{sc_col}" font-size="{int(20*s)}" font-weight="700" font-family="Hind Siliguri,Lohit Bengali,sans-serif">নম্বর</text>')
    return '\n'.join(p)

def prop_book(x, y, s=1.0, color=TEAL, closed=True):
    p=[]; bw,bh=int(120*s),int(160*s)
    if closed:
        p.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="{6*s}" fill="{color}" stroke="{INK}" stroke-width="{5*s}"/>')
        p.append(f'<rect x="{x}" y="{y}" width="{int(20*s)}" height="{bh}" rx="{6*s}" fill="{dk(color)}" stroke="{INK}" stroke-width="{4*s}"/>')
        for i in range(3):
            p.append(f'<line x1="{x+28*s}" y1="{y+55*s+i*22*s}" x2="{x+bw-8*s}" y2="{y+55*s+i*22*s}" stroke="white" stroke-width="{3*s}" opacity="0.6"/>')
    else:
        cx2=x+bw; bw2=bw*2
        p.append(f'<path d="M {cx2},{y} Q {cx2-10},{y+bh//2} {cx2},{y+bh} Q {cx2-bw},{y+bh+5*s} {cx2-bw},{y+bh} Q {cx2-bw-5},{y+bh//2} {cx2-bw},{y} Z" fill="white" stroke="{INK}" stroke-width="{4*s}"/>')
        p.append(f'<path d="M {cx2},{y} Q {cx2+10},{y+bh//2} {cx2},{y+bh} Q {cx2+bw},{y+bh+5*s} {cx2+bw},{y+bh} Q {cx2+bw+5},{y+bh//2} {cx2+bw},{y} Z" fill="white" stroke="{INK}" stroke-width="{4*s}"/>')
        for i in range(4):
            p.append(f'<line x1="{cx2-bw+20*s}" y1="{y+30*s+i*25*s}" x2="{cx2-20*s}" y2="{y+30*s+i*25*s}" stroke="#C0B8A0" stroke-width="{2*s}"/>')
        p.append(f'<rect x="{cx2-8*s}" y="{y-5*s}" width="{16*s}" height="{bh+10*s}" fill="{color}" stroke="{INK}" stroke-width="{4*s}"/>')
    return '\n'.join(p)

def prop_step_card(x, y, num, text, s=1.0):
    p=[]; cw,ch=int(560*s),int(100*s)
    p.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="{16*s}" fill="white" stroke="{MARIGOLD}" stroke-width="{5*s}"/>')
    br=int(38*s); bx=x+br+int(15*s); by=y+ch//2
    p.append(f'<circle cx="{bx}" cy="{by}" r="{br}" fill="{MARIGOLD}" stroke="{INK}" stroke-width="{4*s}"/>')
    p.append(f'<text x="{bx}" y="{by+br//3}" text-anchor="middle" fill="{INK}" font-size="{int(32*s)}" font-weight="700" font-family="Hind Siliguri,Lohit Bengali,sans-serif">{num}</text>')
    tx=bx+br+int(20*s); ty=by+int(10*s)
    p.append(f'<text x="{tx}" y="{ty}" fill="{INK}" font-size="{int(26*s)}" font-weight="700" font-family="Hind Siliguri,Lohit Bengali,sans-serif">{text}</text>')
    return '\n'.join(p)

def _sparkle(cx2, cy2, r):
    p=[]
    for a in range(0,360,90):
        ar=math.radians(a); ar2=math.radians(a+45)
        p.append(f'<line x1="{cx2}" y1="{cy2}" x2="{cx2+r*math.cos(ar):.0f}" y2="{cy2+r*math.sin(ar):.0f}" stroke="{MARIGOLD}" stroke-width="{max(1,r//4+1)}" stroke-linecap="round"/>')
    p.append(f'<circle cx="{cx2}" cy="{cy2}" r="{max(1,r//4)}" fill="{MARIGOLD}"/>')
    return '\n'.join(p)

# ── backgrounds ────────────────────────────────────────────────
def bg_classroom():
    p=[f'<rect width="{W}" height="{H}" fill="#F5EDD8"/>',
       f'<rect width="{W}" height="1300" fill="#EDE0C4"/>',
       f'<rect y="1300" width="{W}" height="{H-1300}" fill="{JUTE}"/>',
       f'<line x1="0" y1="1300" x2="{W}" y2="1300" stroke="{INK}" stroke-width="6"/>']
    for y in range(1310, H, 90):
        p.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="#C8A878" stroke-width="1.5" opacity="0.5"/>')
    for x in range(0, W, 110):
        p.append(f'<line x1="{x}" y1="1300" x2="{x}" y2="{H}" stroke="#C8A878" stroke-width="1.5" opacity="0.5"/>')
    # chalkboard
    p.extend([
      f'<rect x="80" y="100" width="920" height="560" rx="12" fill="{BOARD}" stroke="{INK}" stroke-width="8"/>',
      f'<rect x="95" y="115" width="890" height="530" rx="8" fill="#1A4020"/>',
      f'<text x="540" y="360" text-anchor="middle" font-size="56" font-weight="700" fill="white" font-family="Hind Siliguri,Lohit Bengali,sans-serif" opacity="0.9">পরীক্ষার প্রস্তুতি</text>',
      f'<text x="540" y="440" text-anchor="middle" font-size="40" font-weight="700" fill="{MARIGOLD}" font-family="Hind Siliguri,Lohit Bengali,sans-serif">৩টি স্মার্ট টিপস</text>',
      f'<line x1="130" y1="500" x2="950" y2="500" stroke="white" stroke-width="2" opacity="0.4" stroke-dasharray="10 5"/>',
      f'<rect x="80" y="650" width="920" height="22" rx="5" fill="{DESK}" stroke="{INK}" stroke-width="4"/>',
      # window
      f'<rect x="850" y="150" width="170" height="320" rx="8" fill="{SKY}" stroke="{INK}" stroke-width="6"/>',
      f'<line x1="935" y1="150" x2="935" y2="470" stroke="{INK}" stroke-width="4"/>',
      f'<line x1="850" y1="310" x2="1020" y2="310" stroke="{INK}" stroke-width="4"/>',
      f'<path d="M 850,150 Q 870,260 850,370" fill="{JUTE}" stroke="{INK}" stroke-width="4" opacity="0.8"/>',
      # front desk
      f'<rect x="260" y="1455" width="560" height="28" rx="8" fill="{DESK}" stroke="{INK}" stroke-width="6"/>',
      f'<rect x="270" y="1483" width="12" height="90" fill="{DESK}" stroke="{INK}" stroke-width="4"/>',
      f'<rect x="798" y="1483" width="12" height="90" fill="{DESK}" stroke="{INK}" stroke-width="4"/>',
    ])
    return '\n'.join(p)

def bg_corridor():
    p=[f'<rect width="{W}" height="{H}" fill="#EDE0C4"/>',
       f'<rect width="{W}" height="1320" fill="#F0DEB8"/>',
       f'<rect y="1320" width="{W}" height="{H-1320}" fill="#C8A878"/>',
       f'<line x1="0" y1="1320" x2="{W}" y2="1320" stroke="{INK}" stroke-width="5"/>',
       f'<rect y="860" width="{W}" height="14" fill="{TERRACOTTA}" opacity="0.5"/>',
       f'<rect width="{W}" height="80" fill="#D8C8A8"/>',
       f'<line x1="0" y1="80" x2="{W}" y2="80" stroke="{INK}" stroke-width="4"/>']
    for lx in [30,130,230,808,908]:
        p.extend([
          f'<rect x="{lx}" y="250" width="88" height="560" rx="8" fill="{JUTE}" stroke="{INK}" stroke-width="4"/>',
          f'<circle cx="{lx+44}" cy="650" r="8" fill="{INK}"/>',
          f'<line x1="{lx}" y1="560" x2="{lx+88}" y2="560" stroke="{INK}" stroke-width="2"/>'])
    return '\n'.join(p)

def bg_warm_tips():
    p=[f'<rect width="{W}" height="{H}" fill="#F6EDDC"/>',
       f'<rect width="{W}" height="90" fill="{TEAL}"/>',
       f'<text x="540" y="58" text-anchor="middle" font-size="40" font-weight="700" fill="white" font-family="Hind Siliguri,Lohit Bengali,sans-serif">সুমনের স্মার্ট টিপস</text>',
       f'<rect y="{H-90}" width="{W}" height="90" fill="{TEAL}" opacity="0.9"/>',
       f'<rect y="1350" width="{W}" height="{H-1350}" fill="{JUTE}" opacity="0.4"/>',
       f'<line x1="0" y1="1350" x2="{W}" y2="1350" stroke="{INK}" stroke-width="3" opacity="0.3"/>']
    for i in range(0,W,60):
        p.append(f'<circle cx="{i+30}" cy="45" r="14" fill="{MARIGOLD}" opacity="0.65"/>')
        p.append(f'<circle cx="{i+30}" cy="{H-45}" r="14" fill="{MARIGOLD}" opacity="0.65"/>')
    for i in range(-H,W+H,180):
        p.append(f'<line x1="{i}" y1="0" x2="{i+H}" y2="{H}" stroke="{JUTE}" stroke-width="1.5" opacity="0.1"/>')
    return '\n'.join(p)

def bg_study():
    p=[f'<rect width="{W}" height="{H}" fill="#F5EDD8"/>',
       f'<rect width="{W}" height="1320" fill="#EDE0C8"/>',
       f'<rect y="1320" width="{W}" height="{H-1320}" fill="#C8A878"/>',
       f'<line x1="0" y1="1320" x2="{W}" y2="1320" stroke="{INK}" stroke-width="5"/>',
       f'<rect x="0" y="250" width="210" height="800" fill="{DESK}" stroke="{INK}" stroke-width="6"/>']
    for sy in [370,490,610,730,850]:
        p.append(f'<rect x="10" y="{sy}" width="190" height="12" fill="#5A3418" stroke="{INK}" stroke-width="2"/>')
    book_data=[(LAL,32),(TEAL,28),(MARIGOLD,36),('#5A3080',30)]
    for shelf_y in [380,500,620,740]:
        bx=15
        for bc,bw in book_data:
            p.append(f'<rect x="{bx}" y="{shelf_y}" width="{bw}" height="85" fill="{bc}" stroke="{INK}" stroke-width="2"/>')
            bx+=bw+4
    p.extend([
      f'<rect x="850" y="680" width="22" height="280" fill="{DESK}" stroke="{INK}" stroke-width="4"/>',
      f'<path d="M 800,680 L 920,680 L 870,560 Z" fill="{MARIGOLD}" stroke="{INK}" stroke-width="4"/>',
      f'<ellipse cx="860" cy="800" rx="220" ry="280" fill="{MARIGOLD}" opacity="0.07"/>',
      f'<rect y="1310" width="{W}" height="85" fill="{DESK}" stroke="{INK}" stroke-width="6"/>'])
    for bi,(bx,bw,bc) in enumerate([(680,140,LAL),(660,170,TEAL),(640,200,MARIGOLD)]):
        p.append(f'<rect x="{bx}" y="{1250-bi*22}" width="{bw}" height="22" rx="4" fill="{bc}" stroke="{INK}" stroke-width="3"/>')
    return '\n'.join(p)

def bg_celebration():
    p=[f'<rect width="{W}" height="{H}" fill="#FFF8E8"/>']
    for a in range(0,360,20):
        ar=math.radians(a)
        p.append(f'<line x1="{W//2+150*math.cos(ar):.0f}" y1="{700+150*math.sin(ar):.0f}" x2="{W//2+1500*math.cos(ar):.0f}" y2="{700+1500*math.sin(ar):.0f}" stroke="{MARIGOLD}" stroke-width="2.5" opacity="0.22"/>')
    for sx2,sy2,sr in [(180,350,25),(900,280,22),(100,750,18),(980,620,20),(250,1050,24),(850,900,20),(540,200,30)]:
        p.append(_sparkle(sx2,sy2,sr))
    for i in range(28):
        cx2=(i*157+60)%W; cy2=(i*113+80)%900; cr=8+(i%5)*3
        cc=[MARIGOLD,LAL,TEAL,TERRACOTTA][i%4]
        p.append(f'<circle cx="{cx2}" cy="{cy2}" r="{cr}" fill="{cc}" opacity="0.5"/>')
    p.extend([f'<rect y="1350" width="{W}" height="{H-1350}" fill="#F0D890" opacity="0.5"/>',
              f'<line x1="0" y1="1350" x2="{W}" y2="1350" stroke="{MARIGOLD}" stroke-width="3" opacity="0.5"/>'])
    return '\n'.join(p)

def bg_outro():
    p=[f'<rect width="{W}" height="{H}" fill="{NIGHT}"/>']
    for i in range(55):
        sx2=(i*137+23)%W; sy2=(i*97+41)%(H//2); sr=1+(i%4)
        p.append(f'<circle cx="{sx2}" cy="{sy2}" r="{sr}" fill="white" opacity="{0.3+(i%5)*0.08:.2f}"/>')
    p.extend([
      f'<rect x="40" y="40" width="{W-80}" height="{H-80}" rx="20" fill="none" stroke="{MARIGOLD}" stroke-width="4" opacity="0.4"/>'])
    for i in range(0,W,55):
        p.append(f'<circle cx="{i+28}" cy="62" r="5" fill="{MARIGOLD}" opacity="0.5"/>')
        p.append(f'<circle cx="{i+28}" cy="{H-62}" r="5" fill="{MARIGOLD}" opacity="0.5"/>')
    for j in range(0,H,55):
        p.append(f'<circle cx="62" cy="{j+28}" r="5" fill="{MARIGOLD}" opacity="0.5"/>')
        p.append(f'<circle cx="{W-62}" cy="{j+28}" r="5" fill="{MARIGOLD}" opacity="0.5"/>')
    return '\n'.join(p)

# ── scene composers ────────────────────────────────────────────
def compose(t):
    sc=scene_at(t); b=breath(t); ms,sp=mouth_at(t); bk=do_blink(t)
    ct,ch=caption_at(t)
    op=1.0
    if t<0.5: op=ease(t/0.5)
    elif t>TOTAL-0.5: op=ease((TOTAL-t)/0.5)

    if sc==1:   return _s1(t,b,ms,sp,bk,ct,ch,op)
    elif sc==2: return _s2(t,b,ms,sp,bk,ct,ch,op)
    elif sc==3: return _s3(t,b,ms,sp,bk,ct,ch,op)
    elif sc==4: return _s4(t,b,ms,sp,bk,ct,ch,op)
    elif sc==5: return _s5(t,b,ms,sp,bk,ct,ch,op)
    elif sc==6: return _s6(t,b,ms,sp,bk,ct,ch,op)
    elif sc==7: return _s7(t,b,ms,sp,bk,ct,ch,op)
    elif sc==8: return _s8(t,b,ms,sp,bk,ct,ch,op)
    else:       return _s9(t,b,ms,sp,bk,ct,ch,op)

def _s1(t,b,ms,sp,bk,ct,ch,op):
    # Classroom — Rahul sad with 50-marks paper
    ex='sad' if t>1.5 else 'surprised'
    arm='hold_paper' if t>3.0 else 'sad'
    ms_r=ms if sp=='Rahul' else 'closed'
    char=rahul(540, 1050+b, s=2.8, ex=ex, ms=ms_r, arm=arm, blink=bk)
    # paper prop near hands when holding
    prop=''
    if t>3.0:
        prop=prop_paper(400, 1120, '৫০', s=1.1)
    extras=f'<g opacity="{1 if t>4.8 else 0}">{prop_paper(650,1120,"১০০",s=1.1)}</g>' if t>5.5 else ''
    return bg_classroom(), char+'\n'+prop+'\n'+extras, ct, ch, op

def _s2(t,b,ms,sp,bk,ct,ch,op):
    # Corridor — dialogue, Rahul left frustrated, Suman right confident
    ms_r=ms if sp=='Rahul' else 'closed'
    ms_s=ms if sp=='Suman' else 'closed'
    ex_r='annoyed' if t<10.5 else 'sad'
    ex_s='confident'
    r=rahul(300, 1080+b, s=2.3, ex=ex_r, ms=ms_r, arm='gesture', blink=bk)
    s=suman(780, 1080+b, s=2.3, ex=ex_s, ms=ms_s, arm='rest', blink=bk)
    prop=prop_paper(700,970,'১০০',s=0.9)
    return bg_corridor(), r+'\n'+s+'\n'+prop, ct, ch, op

def _s3(t,b,ms,sp,bk,ct,ch,op):
    # Suman answers — confident close shot
    ms_s=ms if sp=='Suman' else 'closed'
    ex_s='happy' if t>14 else 'confident'
    s=suman(540, 1050+b, s=2.8, ex=ex_s, ms=ms_s, arm='explain', blink=bk)
    return bg_corridor(), s, ct, ch, op

def _s4(t,b,ms,sp,bk,ct,ch,op):
    # Tip 1 — Active Recall. Suman explains + book prop + step card
    ms_s=ms if sp=='Suman' else 'closed'
    book_open=t>20.5
    s=suman(350, 1020+b, s=2.4, ex='explaining', ms=ms_s, arm='explain', blink=bk)
    book=prop_book(620, 950, s=1.3, color=TEAL, closed=not book_open)
    card=prop_step_card(80, 950, '১', 'বই বন্ধ রেখে মনে করো', s=1.1)
    extras=f'{book}\n{card}'
    return bg_warm_tips(), s+'\n'+extras, ct, ch, op

def _s5(t,b,ms,sp,bk,ct,ch,op):
    # Tip 2 — Practice papers
    ms_s=ms if sp=='Suman' else 'closed'
    s=suman(350, 1020+b, s=2.4, ex='explaining', ms=ms_s, arm='explain', blink=bk)
    qp=prop_paper(650, 900, '?', s=1.2)
    card=prop_step_card(80, 950, '২', 'প্রশ্নপত্র প্র্যাকটিস করো', s=1.1)
    # clock
    cx2,cy2,r2=750,920,55
    clock=f'<circle cx="{cx2}" cy="{cy2}" r="{r2}" fill="white" stroke="{INK}" stroke-width="5"/><circle cx="{cx2}" cy="{cy2}" r="5" fill="{INK}"/><line x1="{cx2}" y1="{cy2}" x2="{cx2}" y2="{cy2-r2+10}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/><line x1="{cx2}" y1="{cy2}" x2="{cx2+r2-15}" y2="{cy2}" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
    return bg_warm_tips(), s+'\n'+qp+'\n'+card+'\n'+clock, ct, ch, op

def _s6(t,b,ms,sp,bk,ct,ch,op):
    # Tip 3 — Exam strategy
    ms_s=ms if sp=='Suman' else 'closed'
    s=suman(350, 1020+b, s=2.4, ex='explaining', ms=ms_s, arm='explain', blink=bk)
    ep=prop_paper(650, 900, '✓', s=1.2)
    card=prop_step_card(80, 950, '৩', 'ভালো জানাটা আগে লিখো', s=1.1)
    return bg_warm_tips(), s+'\n'+ep+'\n'+card, ct, ch, op

def _s7(t,b,ms,sp,bk,ct,ch,op):
    # Rahul studying and improving
    prog=min(1.0,(t-38.0)/6.0)
    ex='thinking' if prog<0.5 else 'happy'
    arm='write' if prog<0.5 else 'celebrate'
    r=rahul(540, 1050+b, s=2.7, ex=ex, ms='closed', arm=arm, blink=bk)
    # show improved score
    score='৯৫' if t>42 else ''
    prop=prop_paper(650,950,score,s=1.1) if score else ''
    book=prop_book(300,1200,s=1.1,color=TEAL,closed=False) if prog<0.5 else ''
    return bg_study(), r+'\n'+prop+'\n'+book, ct, ch, op

def _s8(t,b,ms,sp,bk,ct,ch,op):
    # Rahul celebrates — ওয়াও!
    ms_r=ms if sp=='Rahul' else 'closed'
    bounce_ex=abs(math.sin(t*6))*3
    r=rahul(540, 1050+b-bounce_ex, s=2.8, ex='excited', ms=ms_r, arm='celebrate', blink=bk)
    score=prop_paper(380,890,'৯৫',s=1.3)
    return bg_celebration(), r+'\n'+score, ct, ch, op

def _s9(t,b,ms,sp,bk,ct,ch,op):
    # Motivational outro — just big text
    return bg_outro(), '', ct, ch, op

# ── HTML frame builder ─────────────────────────────────────────
CSS_FONT = ''  # filled from font file at startup

def build_html(bg, chars, ct, ch, op, end_card=False):
    # caption html
    cap_html=''
    if ct:
        inner=ct
        if ch and ch in ct:
            parts=ct.split(ch,1)
            inner=f'{parts[0]}<span style="color:{MARIGOLD}">{ch}</span>{parts[1] if len(parts)>1 else ""}'
        cap_html=f'<div style="position:absolute;bottom:90px;left:50%;transform:translateX(-50%);background:rgba(27,26,34,0.90);padding:18px 36px;border-radius:60px;max-width:980px;text-align:center;font-size:48px;font-weight:700;color:white;white-space:nowrap;font-family:BengaliF,sans-serif;line-height:1.3;">{inner}</div>'

    # end card
    end_html=''
    if end_card:
        end_html=f'''<div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);text-align:center;">
<div style="font-size:72px;font-weight:700;color:{MARIGOLD};font-family:BengaliF,sans-serif;margin-bottom:30px;">পড়ো Smartly</div>
<div style="font-size:72px;font-weight:700;color:white;font-family:BengaliF,sans-serif;">লিখো Confidently!</div>
</div>'''

    return f'''<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{W}px;height:{H}px;overflow:hidden;background:{ALPONA}}}
#fr{{width:{W}px;height:{H}px;position:relative;opacity:{op:.3f}}}
{CSS_FONT}
</style></head><body><div id="fr">
<svg width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg">{bg}\n{chars}</svg>
{cap_html}{end_html}
</div></body></html>'''

# ── main render ────────────────────────────────────────────────
def main():
    global CSS_FONT
    from playwright.sync_api import sync_playwright
    out = Path('frames'); out.mkdir(exist_ok=True)
    audio = Path('assets/voiceover.mp3')
    font_path = Path('assets/font.ttf')

    # Load & embed font as base64
    if font_path.exists():
        b64 = base64.b64encode(font_path.read_bytes()).decode()
        CSS_FONT = f"@font-face{{font-family:'BengaliF';src:url('data:font/truetype;base64,{b64}') format('truetype');font-weight:700;}}"
        print(f"[font] embedded {len(b64)//1024}KB")
    else:
        CSS_FONT = "@import url('https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@700&display=swap');@font-face{font-family:'BengaliF';src:local('Hind Siliguri Bold'),local('Lohit Bengali');}"
        print("[font] using system/CDN font")

    print(f"[render] {NF} frames at {FPS}fps ({TOTAL:.1f}s)")

    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=['--no-sandbox','--disable-setuid-sandbox','--disable-dev-shm-usage'])
        ctx = browser.new_context(viewport={'width':W,'height':H}, device_scale_factor=1)
        page = ctx.new_page()

        # warm-up page (loads font)
        page.set_content(f'<html><head><meta charset="utf-8"><style>{CSS_FONT} body{{font-family:BengaliF,sans-serif}}</style></head><body><div style="font-size:48px">বাংলা</div></body></html>')
        page.wait_for_load_state('networkidle')

        step = max(1, NF // 100)  # progress every 1%
        t0 = __import__('time').time()
        for fn in range(NF):
            t = fn / FPS
            sc = scene_at(t)
            # end card for last 5s
            bg_v, chars_v, ct_v, ch_v, op_v = compose(t)
            html = build_html(bg_v, chars_v, ct_v, ch_v, op_v, end_card=(t>=TOTAL-5.0 and sc==9))
            page.set_content(html)
            page.screenshot(path=str(out/f'frame_{fn:06d}.png'), type='png')
            if fn % step == 0:
                elapsed = __import__('time').time() - t0
                eta = elapsed/max(1,fn+1)*(NF-fn-1)
                print(f"[frame] {fn+1}/{NF}  t={t:.2f}s  ETA={eta:.0f}s", flush=True)

        browser.close()

    print("[encode] running ffmpeg...")
    # Build video from frames + audio
    cmd = [
        'ffmpeg', '-y',
        '-framerate', str(FPS),
        '-i', 'frames/frame_%06d.png',
        '-i', str(audio),
        '-c:v', 'libx264',
        '-preset', 'veryfast',
        '-crf', '20',
        '-pix_fmt', 'yuv420p',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-shortest',
        '-movflags', '+faststart',
        'bangla_toon_v1.mp4'
    ]
    subprocess.check_call(cmd)
    # verify
    result = subprocess.run(['ffprobe','-v','quiet','-print_format','json','-show_format','-show_streams','bangla_toon_v1.mp4'], capture_output=True, text=True)
    info = __import__('json').loads(result.stdout)
    dur = float(info['format']['duration'])
    size = int(info['format']['size'])//1024//1024
    print(f"\n✅ bangla_toon_v1.mp4 — {dur:.1f}s — {size}MB")
    print("অনুমান: রাহুল ও সুমনের গল্প, ৩টি স্মার্ট টিপস সহ — রেন্ডার সম্পন্ন")

if __name__ == '__main__':
    main()
