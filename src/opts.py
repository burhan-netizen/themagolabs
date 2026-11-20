"""/options/ page: live alternatives for four homepage sections, so the owner can pick by looking.
A concept builds, B process, C reviews, D contact. Three options each. noindex, not in the sitemap."""
import json, os

CSS = r'''
.op-intro{padding:calc(150px + env(safe-area-inset-top,0px)) 0 64px}
.op-intro h1{font-size:clamp(46px,7vw,110px);line-height:.92;letter-spacing:-.06em;max-width:12ch}
.op-intro p{margin-top:24px;max-width:58ch;color:var(--graphite);font-size:18px}
.op-jump{display:flex;flex-wrap:wrap;gap:10px;margin-top:36px}
.op-jump a{display:inline-flex;align-items:center;min-height:44px;padding:0 18px;border-radius:999px;border:1px solid var(--rule);text-decoration:none;color:var(--ink);font-size:15px}
.op-jump a:hover{background:var(--ink);color:var(--paper)}
.op-group{background:var(--ink);color:var(--paper);padding:56px 0 52px}
.op-group span{font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--go)}
.op-group h2{font-size:clamp(34px,4.6vw,72px);letter-spacing:-.05em;line-height:.95;margin-top:14px}
.op-group p{color:#B9B7AF;margin-top:14px;max-width:60ch}
.op-tag{position:relative;z-index:5;display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 16px;padding:22px 0;border-bottom:1px solid var(--rule)}
.op-tag .k{font-family:var(--mono);font-size:12px;letter-spacing:.06em;text-transform:uppercase;background:var(--go);color:#04130B;border-radius:999px;padding:6px 12px}
.op-tag b{font-weight:500;font-size:22px;letter-spacing:-.03em}
.op-tag i{font-style:normal;color:var(--graphite);font-size:15px}
.op-dark .op-tag{border-color:#2A2A28}.op-dark .op-tag i{color:#9C9A93}
.op-sec{position:relative}
.op-dark{background:var(--space);color:var(--paper)}
.op-ink{background:var(--ink);color:var(--paper)}
.op-paper{background:var(--paper);color:var(--ink)}
.op-h{font-size:clamp(38px,5vw,76px);line-height:.95;letter-spacing:-.055em}
.op-h em{font-family:"Newsreader",serif;font-weight:300;letter-spacing:-.03em}
.op-lab{font-family:var(--mono);font-size:12px;letter-spacing:.07em;text-transform:uppercase;color:var(--graphite)}
.op-dark .op-lab,.op-ink .op-lab{color:#9C9A93}
.op-btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;min-height:52px;padding:0 24px;border-radius:999px;border:0;background:var(--paper);color:var(--ink);font:inherit;font-size:16px;text-decoration:none;cursor:pointer;transition:transform .3s,background .3s}
.op-btn:hover{transform:translateY(-2px)}
.op-btn.ink{background:var(--ink);color:var(--paper)}
.op-btn.go{background:var(--go);color:#04130B}
.op-round{width:52px;height:52px;border-radius:50%;border:1px solid currentColor;background:none;color:inherit;font-size:20px;cursor:pointer;display:inline-grid;place-items:center;opacity:.8;transition:opacity .2s,background .2s,color .2s}
.op-round:hover{opacity:1;background:var(--paper);color:var(--ink)}
.op-paper .op-round:hover{background:var(--ink);color:var(--paper)}

/* phone frame shared by A options */
.o-ph{display:block;text-decoration:none;color:inherit}
.o-scr{position:relative;display:block;aspect-ratio:440/901;border-radius:26px;overflow:hidden;background:#111;box-shadow:0 0 0 6px #1B1B1A,0 0 0 7px #2C2C2A,0 40px 80px -30px rgba(0,0,0,.8)}
.o-scr img{position:absolute;top:0;left:0;width:100%;height:auto;display:block}
.o-scr img.long{opacity:0;transform:translateY(0);transition:opacity .35s,transform 7s linear}
.o-ph:hover .o-scr img.long,.o-scr.on img.long{opacity:1;transform:translateY(-68.5%)}
.o-scr .bdg{position:absolute;z-index:2;top:12px;left:12px;font-family:var(--mono);font-size:10px;letter-spacing:.06em;text-transform:uppercase;background:rgba(242,241,236,.92);color:var(--ink);border-radius:999px;padding:5px 9px}
.o-cap{display:block;margin-top:16px}
.o-cap b{display:block;font-weight:500;font-size:16px;letter-spacing:-.02em}
.o-cap i{display:block;font-style:normal;font-size:13px;color:#9C9A93;margin-top:2px}

/* A1 parallax columns */
.a1{padding:80px 0 0;overflow:hidden}
.a1-head{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-end;gap:24px}
.a1-head p{max-width:40ch;color:#B9B7AF}
.a1-view{position:relative;height:130vh;margin-top:56px;overflow:hidden;-webkit-mask-image:linear-gradient(180deg,transparent,#000 12%,#000 88%,transparent);mask-image:linear-gradient(180deg,transparent,#000 12%,#000 88%,transparent)}
.a1-cols{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:clamp(18px,3vw,48px);max-width:1280px;margin:0 auto;padding:0 32px}
.a1-col{display:flex;flex-direction:column;gap:56px;will-change:transform}
.a1-col:nth-child(even){margin-top:-30vh}
@media (max-width:900px){.a1-cols{grid-template-columns:repeat(2,minmax(0,1fr));padding:0 18px}.a1-col:nth-child(n+3){display:none}.a1-view{height:110vh}.a1-col{gap:36px}}

/* A2 centre stage */
.a2{padding:80px 0 90px;overflow:hidden}
.a2-stage{position:relative;height:clamp(460px,64vw,640px);margin-top:48px;touch-action:pan-y;user-select:none;-webkit-user-select:none}
.a2-stage .o-ph{position:absolute;left:50%;top:0;width:clamp(190px,23vw,290px);margin-left:calc(clamp(190px,23vw,290px) / -2);transition:transform .8s cubic-bezier(.2,.8,.2,1),opacity .6s,filter .6s;cursor:pointer}
.a2-stage .o-ph .o-cap{display:none}
.a2-bar{display:flex;align-items:center;justify-content:space-between;gap:20px;flex-wrap:wrap;margin-top:28px}
.a2-info b{display:block;font-size:clamp(24px,2.6vw,38px);font-weight:500;letter-spacing:-.04em}
.a2-info span{color:#9C9A93}
.a2-ctl{display:flex;align-items:center;gap:12px}
.a2-ctl .n{font-family:var(--mono);font-size:13px;color:#9C9A93;min-width:64px;text-align:center}
.a2-bar .live{color:var(--paper);text-decoration:none;border-bottom:1px solid var(--go);padding-bottom:3px}

/* A3 index + phone */
.a3{padding:80px 0 100px}
.a3-grid{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,.75fr);gap:clamp(32px,6vw,96px);margin-top:48px;align-items:start}
.a3-list{list-style:none;margin:0;padding:0;border-top:1px solid #2A2A28}
.a3-list button{all:unset;box-sizing:border-box;width:100%;display:grid;grid-template-columns:44px minmax(0,1fr) auto;gap:16px;align-items:baseline;padding:16px 4px;border-bottom:1px solid #2A2A28;cursor:pointer;transition:color .3s,padding .4s}
.a3-list .i{font-family:var(--mono);font-size:12px;color:#6E6C66}
.a3-list .nm{font-size:clamp(20px,2.2vw,32px);letter-spacing:-.04em;color:#77756F;transition:color .3s}
.a3-list .wh{font-size:13px;color:#6E6C66;text-align:right}
.a3-list button[aria-selected=true]{padding-left:18px}
.a3-list button[aria-selected=true] .nm{color:var(--paper)}
.a3-list button[aria-selected=true] .i{color:var(--go)}
.a3-list button:focus-visible{outline:2px solid var(--go);outline-offset:2px}
.a3-ph{position:sticky;top:110px;width:min(100%,320px);margin-left:auto}
.a3-ph .o-scr img{transition:opacity .45s}
.a3-ph .o-scr img.base{opacity:0}.a3-ph .o-scr img.base.on{opacity:1}
.a3-ph .meta{margin-top:20px;display:flex;justify-content:space-between;gap:12px;align-items:baseline}
.a3-ph .meta a{color:var(--paper);font-size:14px;text-decoration:none;border-bottom:1px solid var(--go);white-space:nowrap}
@media (max-width:900px){.a3-grid{grid-template-columns:1fr}.a3-ph{position:relative;top:0;order:-1;margin:0 auto;width:min(70%,280px)}.a3-list .wh{display:none}.a3-list{max-height:none}}

/* B shared visual chips */
.b-vis{display:inline-flex;flex-direction:column;gap:6px;padding:18px 20px;border-radius:16px;background:#1C1C1A;border:1px solid #2C2C2A;min-width:220px;font-size:14px;color:#B9B7AF}
.op-paper .b-vis{background:#FBFAF6;border-color:var(--rule);color:var(--graphite)}
.b-vis .v{font-size:28px;letter-spacing:-.04em;color:var(--paper)}
.op-paper .b-vis .v{color:var(--ink)}
.b-vis .ok{color:var(--go);font-size:18px}
.b-vis s{opacity:.6}

/* B1 horizontal track */
.b1{overflow:hidden}
.b1-pin{height:100vh;height:100svh;display:flex;flex-direction:column;justify-content:center;padding:90px 0 40px}
.b1-top{display:flex;justify-content:space-between;align-items:flex-end;gap:24px;flex-wrap:wrap}
.b1-prog{height:2px;background:#2A2A28;margin-top:28px;position:relative}
.b1-prog i{position:absolute;inset:0 auto 0 0;width:0;background:var(--go)}
.b1-track{display:flex;gap:28px;margin-top:40px;padding-left:max(32px,calc((100vw - 1376px) / 2));will-change:transform}
.b1-p{flex:none;width:min(72vw,760px);min-height:46vh;border-radius:28px;background:#1A1A18;border:1px solid #2A2A28;padding:clamp(28px,3.4vw,48px);display:grid;grid-template-columns:auto 1fr;gap:12px 36px;align-content:start}
.b1-p .num{grid-row:span 3;font-size:clamp(90px,11vw,170px);line-height:.8;letter-spacing:-.07em;color:var(--paper)}
.b1-p .when{font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--go)}
.b1-p h3{font-size:clamp(28px,3vw,46px);letter-spacing:-.045em;line-height:1;font-weight:500}
.b1-p p{color:#B9B7AF;max-width:42ch}
.b1-p .b-vis{grid-column:2;margin-top:12px;justify-self:start}
.b1-p:last-child{margin-right:max(32px,calc((100vw - 1376px) / 2))}
@media (max-width:900px){.b1-pin{height:auto;padding:70px 0}.b1-track{flex-direction:column;padding:0 18px;transform:none!important}.b1-p{width:auto;min-height:0;grid-template-columns:1fr}.b1-p .num{grid-row:auto;font-size:72px}.b1-p .b-vis{grid-column:1}.b1-p:last-child{margin-right:0}.b1-prog{display:none}}

/* B2 journey line */
.b2{height:260vh}
.b2-in{position:sticky;top:0;height:100vh;height:100svh;display:flex;flex-direction:column;justify-content:center;padding:90px 0 40px;overflow:hidden}
.b2-line{position:relative;height:2px;background:var(--rule);margin:70px 0 0}
.b2-line .f{position:absolute;inset:0 auto 0 0;width:0;background:var(--ink)}
.b2-line .dot{position:absolute;top:50%;left:0;width:18px;height:18px;margin:-9px 0 0 -9px;border-radius:50%;background:var(--go);box-shadow:0 0 0 8px rgba(16,181,101,.18)}
.b2-cols{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:28px;margin-top:0}
.b2-c{position:relative;padding-top:44px;opacity:.28;transform:translateY(16px);transition:opacity .6s,transform .7s cubic-bezier(.2,.8,.2,1)}
.b2-c::before{content:"";position:absolute;top:-7px;left:0;width:12px;height:12px;border-radius:50%;background:var(--paper);border:2px solid var(--rule);transition:background .4s,border-color .4s}
.b2-c.on{opacity:1;transform:none}
.b2-c.on::before{background:var(--ink);border-color:var(--ink)}
.b2-c .n{font-size:clamp(56px,6vw,96px);line-height:.85;letter-spacing:-.07em}
.b2-c .when{display:block;margin-top:18px;font-family:var(--mono);font-size:12px;letter-spacing:.07em;text-transform:uppercase;color:#0B7A45}
.b2-c h3{font-size:clamp(22px,2vw,30px);letter-spacing:-.04em;font-weight:500;margin-top:8px;line-height:1.05}
.b2-c p{color:var(--graphite);font-size:15.5px;margin-top:10px}
.b2-c .b-vis{margin-top:18px;min-width:0}
@media (max-width:900px){.b2{height:auto}.b2-in{position:relative;height:auto;padding:70px 0}.b2-line{display:none}.b2-cols{grid-template-columns:1fr;gap:0;border-left:2px solid var(--rule);margin-left:8px}.b2-c{padding:0 0 40px 28px;opacity:1;transform:none}.b2-c::before{top:6px;left:-8px}.b2-c .n{font-size:56px}}

/* B3 accordion */
.b3{padding:90px 0 110px}
.b3-grid{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr);gap:clamp(32px,6vw,96px);margin-top:56px;align-items:center}
.b3-list{border-top:1px solid #2A2A28}
.b3-row{border-bottom:1px solid #2A2A28}
.b3-row button{all:unset;box-sizing:border-box;width:100%;display:grid;grid-template-columns:56px minmax(0,1fr) auto;gap:16px;align-items:baseline;padding:22px 0;cursor:pointer}
.b3-row button:focus-visible{outline:2px solid var(--go);outline-offset:4px}
.b3-row .i{font-family:var(--mono);font-size:12px;color:#6E6C66}
.b3-row .t{font-size:clamp(24px,2.6vw,40px);letter-spacing:-.045em;color:#6E6C66;transition:color .3s;line-height:1.05}
.b3-row .w{font-family:var(--mono);font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:#6E6C66}
.b3-row.on .t{color:var(--paper)}.b3-row.on .i,.b3-row.on .w{color:var(--go)}
.b3-body{display:grid;grid-template-rows:0fr;transition:grid-template-rows .5s cubic-bezier(.2,.8,.2,1)}
.b3-row.on .b3-body{grid-template-rows:1fr}
.b3-body>div{overflow:hidden}
.b3-body p{color:#B9B7AF;max-width:46ch;padding:0 0 22px 72px}
.b3-row .bar{height:2px;background:#2A2A28;margin:0 0 -1px 72px;position:relative;overflow:hidden;opacity:0}
.b3-row.on .bar{opacity:1}
.b3-row .bar i{position:absolute;inset:0;background:var(--go);transform:scaleX(0);transform-origin:left}
.b3-card{position:relative;aspect-ratio:4/3.4;border-radius:28px;background:radial-gradient(120% 100% at 20% 0%,#1F2A22,#141413 60%);border:1px solid #2A2A28;overflow:hidden}
.b3-card .s{position:absolute;inset:0;display:grid;place-items:center;opacity:0;transform:translateY(18px) scale(.98);transition:opacity .5s,transform .7s cubic-bezier(.2,.8,.2,1)}
.b3-card .s.on{opacity:1;transform:none}
.b3-card .s .b-vis{transform:scale(1.35)}
.b3-card .big{position:absolute;right:24px;bottom:-14px;font-size:clamp(120px,16vw,230px);line-height:.8;letter-spacing:-.08em;color:rgba(242,241,236,.06)}
@media (max-width:900px){.b3-grid{grid-template-columns:1fr}.b3-card{order:-1;aspect-ratio:16/10}.b3-body p{padding-left:0}.b3-row .bar{margin-left:0}.b3-row button{grid-template-columns:40px minmax(0,1fr)}.b3-row .w{display:none}}

/* C1 big quote */
.c1{padding:100px 0 110px;text-align:center}
.c1-logo{height:64px;display:grid;place-items:center;margin-top:48px}
.c1-logo img{max-height:56px;max-width:220px;width:auto}
.c1-q{font-family:"Newsreader",serif;font-style:italic;font-weight:300;font-size:clamp(28px,3.6vw,56px);line-height:1.18;letter-spacing:-.02em;max-width:24ch;margin:28px auto 0;min-height:5.2em;display:grid;place-items:center}
.c1-res{display:inline-flex;align-items:center;gap:10px;margin-top:28px;padding:8px 16px;border-radius:999px;background:var(--ink);color:var(--paper);font-size:15px}
.c1-res::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--go)}
.c1-who{margin-top:18px;color:var(--graphite)}
.c1-who b{color:var(--ink);font-weight:500}
.c1-fade{transition:opacity .45s,transform .6s cubic-bezier(.2,.8,.2,1)}
.c1.out .c1-fade{opacity:0;transform:translateY(14px)}
.c1-ctl{display:flex;justify-content:center;align-items:center;gap:16px;margin-top:44px}
.c1-dots{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin-top:26px}
.c1-dots button{width:34px;height:4px;border:0;border-radius:4px;background:var(--rule);cursor:pointer;padding:0;position:relative;overflow:hidden}
.c1-dots button[aria-current=true]{background:var(--ink)}
.c1-badge{display:inline-flex;gap:12px;align-items:center;margin-top:10px;color:var(--graphite);font-size:15px;text-decoration:none}
.c1-badge b{font-size:22px;color:var(--ink);font-weight:500}

/* C2 wall of love */
.c2{padding:90px 0 0}
.c2-head{display:flex;justify-content:space-between;align-items:flex-end;gap:24px;flex-wrap:wrap}
.c2-badge{display:inline-flex;align-items:center;gap:14px;padding:14px 22px;border-radius:20px;background:#1A1A18;border:1px solid #2A2A28;color:var(--paper);text-decoration:none}
.c2-badge .n{font-size:40px;letter-spacing:-.05em;line-height:1}
.c2-badge .s{font-size:13px;color:#B9B7AF}.c2-badge .s b{display:block;color:#F5C451;letter-spacing:2px;font-weight:400}
.c2-view{position:relative;height:min(820px,92vh);margin-top:48px;overflow:hidden;-webkit-mask-image:linear-gradient(180deg,transparent,#000 14%,#000 86%,transparent);mask-image:linear-gradient(180deg,transparent,#000 14%,#000 86%,transparent)}
.c2-cols{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}
.c2-col{display:flex;flex-direction:column;gap:20px;animation:c2up var(--d,48s) linear infinite}
.c2-col.rev{animation-direction:reverse}
.c2-view:hover .c2-col{animation-play-state:paused}
@keyframes c2up{to{transform:translateY(calc(-50% - 10px))}}
.c2-card{background:#161615;border:1px solid #2A2A28;border-radius:22px;padding:24px;text-decoration:none;color:inherit;display:block;transition:border-color .3s,transform .4s}
.c2-card:hover{border-color:var(--go);transform:translateY(-3px)}
.c2-card .st{color:#F5C451;letter-spacing:2px;font-size:14px}
.c2-card .h{display:block;margin-top:12px;font-size:20px;letter-spacing:-.03em;font-weight:500;color:var(--paper)}
.c2-card p{margin-top:10px;display:-webkit-box;-webkit-line-clamp:8;-webkit-box-orient:vertical;overflow:hidden;color:#C9C7BF;font-size:15.5px;line-height:1.5}
.c2-card .who{display:flex;align-items:center;gap:12px;margin-top:18px}
.c2-card .lg{width:44px;height:44px;border-radius:12px;background:#FBFAF6;display:grid;place-items:center;flex:none;overflow:hidden}
.c2-card .lg img{max-width:36px;max-height:30px;width:auto;height:auto}
.c2-card .lg span{font-size:13px;color:var(--ink);font-weight:500}
.c2-card .who b{display:block;font-weight:500;font-size:15px;color:var(--paper)}
.c2-card .who i{display:block;font-style:normal;font-size:13px;color:#9C9A93}
@media (max-width:900px){.c2-cols{grid-template-columns:1fr}.c2-col:nth-child(n+2){display:none}.c2-view{height:640px}}
@media (prefers-reduced-motion:reduce){.c2-col{animation:none}.c2-view{height:auto;-webkit-mask-image:none;mask-image:none}}

/* C3 result rail */
.c3{padding:90px 0 100px;overflow:hidden}
.c3-top{display:flex;justify-content:space-between;align-items:flex-end;gap:24px;flex-wrap:wrap}
.c3-rail{display:flex;gap:20px;overflow-x:auto;scroll-snap-type:x mandatory;padding:44px max(32px,calc((100vw - 1376px) / 2)) 12px;scrollbar-width:none;cursor:grab}
.c3-rail::-webkit-scrollbar{display:none}
.c3-rail.drag{cursor:grabbing;scroll-snap-type:none}
.c3-card{flex:none;width:min(84vw,400px);min-height:470px;scroll-snap-align:start;border-radius:28px;background:var(--ink);color:var(--paper);padding:30px;display:flex;flex-direction:column;user-select:none}
.c3-card:nth-child(3n+2){background:#1F3A2B}
.c3-card:nth-child(3n){background:#FBFAF6;color:var(--ink);border:1px solid var(--rule)}
.c3-card .res{font-size:clamp(32px,3vw,44px);line-height:.98;letter-spacing:-.05em}
.c3-card .res::before{content:"";display:inline-block;width:.22em;height:.22em;border-radius:50%;background:var(--go);margin-right:.18em;vertical-align:.14em}
.c3-card p.lq{font-size:17px}
.c3-card p{margin-top:20px;font-family:"Newsreader",serif;font-style:italic;font-weight:300;font-size:21px;line-height:1.3;opacity:.9}
.c3-card .who{margin-top:auto;padding-top:28px;display:flex;align-items:center;gap:14px}
.c3-card .lg{height:52px;min-width:52px;padding:0 10px;border-radius:14px;background:#FBFAF6;display:grid;place-items:center}
.c3-card:nth-child(3n) .lg{background:var(--paper)}
.c3-card .lg img{max-height:36px;max-width:110px;width:auto;height:auto}
.c3-card .who b{display:block;font-weight:500}
.c3-card .who i{display:block;font-style:normal;font-size:13px;opacity:.65}
.c3-ctl{display:flex;gap:12px}

/* D shared */
.d-ok{display:none}
.d-err{color:#E5484D;font-size:14px;margin-top:10px;min-height:1.2em}

/* D1 chat */
.d1{padding:90px 0 110px}
.d1-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,560px);gap:clamp(32px,6vw,96px);align-items:center}
.d1-grid .side p{color:#B9B7AF;margin-top:20px;max-width:40ch}
.d1-grid .side ul{list-style:none;padding:0;margin:28px 0 0;display:grid;gap:10px;color:#C9C7BF}
.d1-grid .side li::before{content:"";display:inline-block;width:7px;height:7px;border-radius:50%;background:var(--go);margin-right:12px;vertical-align:2px}
.d1-win{border-radius:28px;background:#121211;border:1px solid #2A2A28;overflow:hidden;box-shadow:0 50px 100px -40px rgba(0,0,0,.8)}
.d1-hd{display:flex;align-items:center;gap:12px;padding:16px 20px;border-bottom:1px solid #2A2A28;background:#171716}
.d1-hd img{width:42px;height:42px;border-radius:50%;object-fit:cover;object-position:50% 20%}
.d1-hd b{display:block;font-weight:500}
.d1-hd span{font-size:13px;color:var(--go)}
.d1-log{height:430px;overflow-y:auto;padding:22px 20px;display:flex;flex-direction:column;gap:10px;scroll-behavior:smooth}
.d1-m{max-width:82%;padding:12px 16px;border-radius:20px;font-size:16px;line-height:1.4;animation:d1in .4s cubic-bezier(.2,.8,.2,1)}
.d1-m.bot{background:#232321;color:var(--paper);border-bottom-left-radius:6px;align-self:flex-start}
.d1-m.me{background:var(--go);color:#04130B;border-bottom-right-radius:6px;align-self:flex-end}
.d1-m.typing{display:inline-flex;gap:4px}
.d1-m.typing i{width:7px;height:7px;border-radius:50%;background:#9C9A93;animation:d1dot 1s infinite}
.d1-m.typing i:nth-child(2){animation-delay:.15s}.d1-m.typing i:nth-child(3){animation-delay:.3s}
@keyframes d1in{from{opacity:0;transform:translateY(10px)}}
@keyframes d1dot{50%{opacity:.3;transform:translateY(-3px)}}
.d1-opts{display:flex;flex-wrap:wrap;gap:8px;align-self:flex-end;justify-content:flex-end;max-width:90%}
.d1-opts button{min-height:40px;padding:0 16px;border-radius:999px;border:1px solid var(--go);background:none;color:var(--paper);font:inherit;font-size:15px;cursor:pointer}
.d1-opts button[aria-pressed=true],.d1-opts button:hover{background:var(--go);color:#04130B}
.d1-in{display:flex;gap:10px;padding:14px;border-top:1px solid #2A2A28}
.d1-in input{flex:1;min-width:0;min-height:48px;border-radius:999px;border:1px solid #2F2F2C;background:#1B1B1A;color:var(--paper);padding:0 18px;font:inherit;font-size:16px}
.d1-in input:focus{outline:none;border-color:var(--go)}
.d1-in button{width:48px;height:48px;border-radius:50%;border:0;background:var(--go);color:#04130B;font-size:20px;cursor:pointer;flex:none}
.d1-in.off input,.d1-in.off button{opacity:.35;pointer-events:none}
@media (max-width:900px){.d1-grid{grid-template-columns:1fr}.d1-log{height:400px}}

/* D2 split card */
.d2{padding:100px 0 110px}
.d2-grid{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);gap:clamp(32px,6vw,96px);align-items:start}
.d2-side p{color:var(--graphite);margin-top:20px;max-width:38ch;font-size:18px}
.d2-lines{margin-top:36px;display:grid;gap:4px;border-top:1px solid var(--rule)}
.d2-lines a,.d2-lines div{display:flex;justify-content:space-between;gap:16px;align-items:center;padding:18px 0;border-bottom:1px solid var(--rule);text-decoration:none;color:var(--ink);font-size:18px}
.d2-lines span{font-family:var(--mono);font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--graphite)}
.d2-lines a:hover{color:#0B7A45}
.d2-card{background:#FBFAF6;border:1px solid var(--rule);border-radius:28px;padding:clamp(24px,3.4vw,44px);box-shadow:0 40px 80px -50px rgba(17,17,16,.35)}
.d2-row{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.d2-f{display:block;margin-top:18px}
.d2-f>span{display:block;font-size:14px;color:var(--graphite);margin-bottom:8px}
.d2-f input,.d2-f textarea{width:100%;min-height:54px;border-radius:14px;border:1px solid var(--rule);background:#fff;padding:14px 16px;font:inherit;font-size:16px;color:var(--ink);transition:border-color .2s,box-shadow .2s}
.d2-f textarea{min-height:110px;resize:vertical}
.d2-f input:focus,.d2-f textarea:focus{outline:none;border-color:var(--ink);box-shadow:0 0 0 4px rgba(17,17,16,.06)}
.d2-f [aria-invalid=true]{border-color:#E5484D}
.d2-seg{display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:6px;border-radius:16px;background:var(--stone)}
.d2-seg label{position:relative}
.d2-seg input{position:absolute;opacity:0;inset:0}
.d2-seg span{display:grid;place-items:center;min-height:46px;border-radius:12px;font-size:15px;cursor:pointer;transition:background .25s,box-shadow .25s}
.d2-seg input:checked+span{background:#fff;box-shadow:0 4px 12px -6px rgba(17,17,16,.3)}
.d2-seg input:focus-visible+span{outline:2px solid var(--ink)}
.d2-pills{display:flex;flex-wrap:wrap;gap:8px}
.d2-pills label{position:relative}
.d2-pills input{position:absolute;opacity:0;inset:0}
.d2-pills span{display:inline-flex;align-items:center;min-height:44px;padding:0 18px;border-radius:999px;border:1px solid var(--rule);cursor:pointer;font-size:15px;transition:background .2s,color .2s}
.d2-pills input:checked+span{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.d2-pills input:focus-visible+span{outline:2px solid var(--go)}
.d2-send{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;margin-top:28px}
.d2-send small{color:var(--graphite);font-size:13.5px;max-width:30ch}
.d2-done{text-align:center;padding:40px 10px}
.d2-done h3{font-size:clamp(28px,3vw,40px);letter-spacing:-.045em;font-weight:500}
.d2-done p{color:var(--graphite);margin:12px auto 26px;max-width:36ch}
@media (max-width:900px){.d2-grid,.d2-row{grid-template-columns:1fr}.d2-row{gap:0}}

/* D3 one question at a time */
.d3{padding:90px 0 110px;min-height:100vh}
.d3-box{max-width:980px;margin:40px auto 0}
.d3-prog{display:flex;align-items:center;gap:16px;font-family:var(--mono);font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:#9C9A93}
.d3-prog .t{flex:1;height:2px;background:#2A2A28;position:relative}
.d3-prog .t i{position:absolute;inset:0 auto 0 0;background:var(--go);transition:width .6s cubic-bezier(.2,.8,.2,1)}
.js .d3-step{display:none}.d3-step{margin-top:56px;animation:d3in .6s cubic-bezier(.2,.8,.2,1)}
.js .d3-step.on{display:block}
@keyframes d3in{from{opacity:0;transform:translateY(30px)}}
.d3-step label,.d3-step .d3-q{display:block;font-size:clamp(34px,5vw,72px);letter-spacing:-.055em;line-height:1}
.d3-step .d3-q em,.d3-step label em{font-family:"Newsreader",serif;font-weight:300}
.d3-step input{display:block;width:100%;margin-top:36px;background:none;border:0;border-bottom:2px solid #3A3A37;color:var(--paper);font:inherit;font-size:clamp(24px,3vw,40px);padding:10px 0;letter-spacing:-.03em}
.d3-step input::placeholder{color:#55534E}
.d3-step input:focus{outline:none;border-color:var(--go)}
.d3-ch{display:flex;flex-wrap:wrap;gap:12px;margin-top:36px}
.d3-ch button{min-height:60px;padding:0 26px;border-radius:999px;border:1px solid #3A3A37;background:none;color:var(--paper);font:inherit;font-size:clamp(17px,1.6vw,22px);cursor:pointer;transition:background .2s,color .2s,border-color .2s}
.d3-ch button:hover{border-color:var(--paper)}
.d3-ch button[aria-pressed=true]{background:var(--go);border-color:var(--go);color:#04130B}
.d3-nav{display:flex;align-items:center;gap:18px;margin-top:40px;flex-wrap:wrap}
.d3-nav .hint{font-size:14px;color:#9C9A93}
.d3-nav .back{background:none;border:0;color:#9C9A93;font:inherit;cursor:pointer;text-decoration:underline;text-underline-offset:4px}
.d3-sum{margin-top:30px;display:grid;gap:2px;border-top:1px solid #2A2A28}
.d3-sum div{display:flex;justify-content:space-between;gap:20px;padding:14px 0;border-bottom:1px solid #2A2A28;font-size:18px}
.d3-sum span{color:#9C9A93;font-family:var(--mono);font-size:12px;letter-spacing:.06em;text-transform:uppercase}
@media (prefers-reduced-motion:reduce){.d3-step,.d1-m{animation:none}.o-scr img.long{transition:opacity .3s}}
'''

JS = r'''
document.addEventListener('DOMContentLoaded',function(){
var $=function(s,r){return (r||document).querySelector(s)},$$=function(s,r){return [].slice.call((r||document).querySelectorAll(s))};
var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
var _d=$('#op-data');var DATA=_d?JSON.parse(_d.textContent):{concepts:[],reviews:[]};
function msg(o){return ['Hi Burhan, I\'m '+(o.name||'')+(o.business?' from '+o.business:'')+'.',
 o.has==='no'?'I don\'t have a website yet. I\'d like the free 48-hour preview.':'I have a website'+(o.website?' at '+o.website:'')+'. I\'d like the free audit.',
 o.goals&&o.goals.length?'I want more '+o.goals.join(', ')+'.':'', o.msg||'', 'Reach me at '+(o.reach||'')+'.'].filter(Boolean).join('\n');}
function wa(o){var n=(window.MAGO&&MAGO.whatsapp)||'';return 'https://wa.me/'+n+'?text='+encodeURIComponent(msg(o));}
function sendMail(o){var M=window.MAGO||{},ep=M.formEndpoint;
 var subj='New enquiry: '+(o.business||o.name||'website')+(o.has==='no'?' (no website yet)':'');
 if(!ep){location.href='mailto:'+(M.email||'')+'?subject='+encodeURIComponent(subj)+'&body='+encodeURIComponent(msg(o));return Promise.resolve('mailto');}
 var body={name:o.name||'',business:o.business||'',has_website:o.has==='no'?'no':'yes',website:o.website||'',wants_more:(o.goals||[]).join(', '),contact:o.reach||'',message:msg(o),subject:subj,_subject:subj,page:location.pathname};
 if(M.formKey)body.access_key=M.formKey;
 return fetch(ep,{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify(body)}).then(function(r){if(!r.ok)throw new Error(r.status);return 'sent'});}
function loadLong(ph){var l=$('img.long',ph);if(l&&!l.src)l.src=l.dataset.src;}
$$('.o-ph').forEach(function(ph){ph.addEventListener('pointerenter',function(){loadLong(ph)});ph.addEventListener('focus',function(){loadLong(ph)});});

/* A1 parallax columns */
$$('.a1-view').forEach(function(v){var cols=$$('.a1-col',v),sp=[-320,220,-420,160];
 function f(){var r=v.getBoundingClientRect(),p=(innerHeight-r.top)/(innerHeight+r.height);p=Math.max(0,Math.min(1,p));
  cols.forEach(function(c,i){c.style.transform='translate3d(0,'+((p-.5)*sp[i%4]*(innerWidth<900?.6:1)).toFixed(1)+'px,0)'});}
 if(!reduce){addEventListener('scroll',f,{passive:true});addEventListener('resize',f);f();}});

/* A2 centre stage */
$$('.a2').forEach(function(sec){var st=$('.a2-stage',sec),ph=$$('.o-ph',st),n=ph.length,i=0,t=null;
 function lay(){ph.forEach(function(p,k){var d=k-i;if(d>n/2)d-=n;if(d<-n/2)d+=n;var a=Math.abs(d),sm=innerWidth<700;
  p.style.transform='translateX('+(d*(sm?58:68))+'%) scale('+(1-Math.min(a,3)*.17)+')';p.style.zIndex=20-a;p.style.opacity=a>(sm?1:2)?0:1;p.style.filter='brightness('+(1-a*.32)+')';
  p.classList.toggle('c',d===0);var s=$('.o-scr',p);if(d===0){loadLong(p);setTimeout(function(){s.classList.add('on')},500)}else s.classList.remove('on');p.tabIndex=d===0?0:-1;});
  var c=DATA.concepts[i];$('.a2-info b',sec).textContent=c.name;$('.a2-info span',sec).textContent=c.trade+' · '+c.where;$('.a2-ctl .n',sec).textContent=String(i+1).padStart(2,'0')+' / '+n;$('.a2-bar .live',sec).href=c.url;}
 function go(k){i=(k+n)%n;lay();}
 function auto(){clearInterval(t);if(!reduce)t=setInterval(function(){go(i+1)},4200);}
 $('.prev',sec).onclick=function(){go(i-1);auto()};$('.next',sec).onclick=function(){go(i+1);auto()};
 ph.forEach(function(p,k){p.addEventListener('click',function(e){if(k!==i){e.preventDefault();go(k);auto();}});});
 var x0=null;st.addEventListener('pointerdown',function(e){x0=e.clientX});st.addEventListener('pointerup',function(e){if(x0===null)return;var dx=e.clientX-x0;x0=null;if(Math.abs(dx)>50){go(i+(dx<0?1:-1));auto();}});
 st.addEventListener('pointerenter',function(){clearInterval(t)});st.addEventListener('pointerleave',auto);
 lay();auto();addEventListener('resize',lay);});

/* A3 index + phone */
$$('.a3').forEach(function(sec){var bs=$$('.a3-list button',sec),imgs=$$('.a3-ph img.base',sec),long=$('.a3-ph img.long',sec),scr=$('.a3-ph .o-scr',sec);
 function set(k){bs.forEach(function(b,j){b.setAttribute('aria-selected',j===k)});imgs.forEach(function(im,j){im.classList.toggle('on',j===k)});
  var c=DATA.concepts[k];scr.classList.remove('on');long.style.transition='none';long.style.transform='';long.src=c.long;void long.offsetWidth;long.style.transition='';
  setTimeout(function(){scr.classList.add('on')},350);$('.a3-ph .meta b',sec).textContent=c.name;$('.a3-ph .meta a',sec).href=c.url;}
 bs.forEach(function(b,k){b.addEventListener('mouseenter',function(){set(k)});b.addEventListener('focus',function(){set(k)});b.addEventListener('click',function(){set(k)});});
 set(0);});

/* B1 horizontal track */
$$('.b1').forEach(function(sec){if(innerWidth<900||!window.gsap||!window.ScrollTrigger||reduce)return;gsap.registerPlugin(ScrollTrigger);
 var tr=$('.b1-track',sec),bar=$('.b1-prog i',sec);var dist=function(){return tr.scrollWidth-innerWidth};
 gsap.to(tr,{x:function(){return -dist()},ease:'none',scrollTrigger:{trigger:$('.b1-pin',sec),pin:true,start:'top top',end:function(){return '+='+dist()},scrub:.6,invalidateOnRefresh:true,onUpdate:function(s){bar.style.width=(s.progress*100)+'%'}}});});

/* B2 journey line */
$$('.b2').forEach(function(sec){var f=$('.b2-line .f',sec),dot=$('.b2-line .dot',sec),cs=$$('.b2-c',sec);
 function u(){if(innerWidth<900){cs.forEach(function(c){c.classList.add('on')});return;}var r=sec.getBoundingClientRect(),p=-r.top/(r.height-innerHeight);p=Math.max(0,Math.min(1,p));
  var w=(p*1.08)*100;w=Math.min(100,w);f.style.width=w+'%';dot.style.left=w+'%';cs.forEach(function(c,k){c.classList.toggle('on',w>=k*25+2)});}
 addEventListener('scroll',u,{passive:true});addEventListener('resize',u);u();});

/* B3 accordion */
$$('.b3').forEach(function(sec){var rows=$$('.b3-row',sec),ss=$$('.b3-card .s',sec),big=$('.b3-card .big',sec),i=0,anim=null,user=false;
 function set(k){i=k;rows.forEach(function(r,j){r.classList.toggle('on',j===k);$('button',r).setAttribute('aria-expanded',j===k)});ss.forEach(function(s,j){s.classList.toggle('on',j===k)});big.textContent='0'+(k+1);
  if(anim)anim.cancel();var bar=$('.bar i',rows[k]);if(!user&&!reduce&&bar.animate){anim=bar.animate([{transform:'scaleX(0)'},{transform:'scaleX(1)'}],{duration:5200,easing:'linear'});anim.onfinish=function(){set((i+1)%rows.length)};}}
 rows.forEach(function(r,k){$('button',r).addEventListener('click',function(){user=true;set(k)})});
 var io=new IntersectionObserver(function(es){if(es[0].isIntersecting){set(i);io.disconnect()}},{threshold:.4});io.observe(sec);set(0);if(anim)anim.pause();});

/* C1 big quote */
$$('.c1').forEach(function(sec){var T=DATA.reviews,i=0,t=null,dots=$$('.c1-dots button',sec);
 function show(k){sec.classList.add('out');setTimeout(function(){i=(k+T.length)%T.length;var r=T[i];
  $('.c1-q',sec).textContent='“'+r.quote+'”';var L=r.quote.length;$('.c1-q',sec).style.fontSize=L>260?'clamp(20px,1.9vw,27px)':L>160?'clamp(22px,2.4vw,34px)':L>90?'clamp(26px,3vw,44px)':'';$('.c1-q',sec).style.maxWidth=L>160?'40ch':'';$('.c1-res',sec).textContent=r.head;$('.c1-who',sec).innerHTML='<b></b>, <span></span>';$('.c1-who b',sec).textContent=r.name;$('.c1-who span',sec).textContent=r.role;
  var lg=$('.c1-logo',sec);lg.innerHTML=r.logo?'<img alt="">':'';if(r.logo){$('img',lg).src=r.logo;$('img',lg).alt=r.company;}
  dots.forEach(function(d,j){d.setAttribute('aria-current',j===i)});sec.classList.remove('out');},reduce?0:420);}
 function auto(){clearInterval(t);if(!reduce)t=setInterval(function(){show(i+1)},5000);}
 $('.prev',sec).onclick=function(){show(i-1);auto()};$('.next',sec).onclick=function(){show(i+1);auto()};
 dots.forEach(function(d,j){d.onclick=function(){show(j);auto()}});
 var sw=$('.c1-swipe',sec),x0=null,y0=0;sw.addEventListener('pointerdown',function(e){x0=e.clientX;y0=e.clientY});
 sw.addEventListener('pointerup',function(e){if(x0===null)return;var dx=e.clientX-x0,dy=e.clientY-y0;x0=null;if(Math.abs(dx)>45&&Math.abs(dx)>Math.abs(dy)){show(i+(dx<0?1:-1));auto();}});
 sw.addEventListener('pointercancel',function(){x0=null});
 sec.addEventListener('pointerenter',function(e){if(e.pointerType==='mouse')clearInterval(t)});sec.addEventListener('pointerleave',function(e){if(e.pointerType==='mouse')auto()});
 dots.forEach(function(d,j){d.setAttribute('aria-current',j===0)});
 var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting)auto();else clearInterval(t)})});io.observe(sec);});

/* C3 rail drag + arrows */
$$('.c3').forEach(function(sec){var r=$('.c3-rail',sec),down=false,x0=0,s0=0,moved=false;
 r.addEventListener('pointerdown',function(e){if(e.pointerType!=='mouse')return;down=true;moved=false;x0=e.clientX;s0=r.scrollLeft;r.classList.add('drag')});
 addEventListener('pointermove',function(e){if(!down)return;var d=e.clientX-x0;if(Math.abs(d)>4)moved=true;r.scrollLeft=s0-d});
 addEventListener('pointerup',function(){if(!down)return;down=false;r.classList.remove('drag')});
 var step=function(){return ($('.c3-card',r).offsetWidth+20)};
 $('.prev',sec).onclick=function(){r.scrollBy({left:-step(),behavior:'smooth'})};$('.next',sec).onclick=function(){r.scrollBy({left:step(),behavior:'smooth'})};});

/* D1 chat */
$$('.d1').forEach(function(sec){var log=$('.d1-log',sec),form=$('.d1-in',sec),inp=$('input',form),o={goals:[]},k=0;
 var Q=[{key:'name',q:'Hi! I\'m Burhan. What should I call you?',ph:'Your name'},
  {key:'business',q:function(){return 'Nice to meet you, '+o.name+'. What\'s your business called?'},ph:'Business name'},
  {key:'has',q:'Do you have a website yet?',ch:[['yes','Yes, I do'],['no','Not yet']]},
  {key:'website',q:'What\'s the address? I\'ll take a look before we talk.',ph:'yourbusiness.com',skip:function(){return o.has==='no'}},
  {key:'goals',q:'What do you want more of? Pick any.',multi:['calls','bookings','enquiries','sales']},
  {key:'reach',q:'Last one. Best email or phone to reach you?',ph:'Email or phone'}];
 function say(t,who){var m=document.createElement('div');m.className='d1-m '+who;m.textContent=t;log.appendChild(m);log.scrollTop=log.scrollHeight;return m;}
 function typing(cb){var m=document.createElement('div');m.className='d1-m bot typing';m.innerHTML='<i></i><i></i><i></i>';log.appendChild(m);log.scrollTop=log.scrollHeight;setTimeout(function(){m.remove();cb()},reduce?0:750);}
 function ask(){while(Q[k]&&Q[k].skip&&Q[k].skip())k++;var s=Q[k];if(!s)return done();
  typing(function(){say(typeof s.q==='function'?s.q():s.q,'bot');
   if(s.ch||s.multi){form.classList.add('off');var w=document.createElement('div');w.className='d1-opts';
    (s.ch||s.multi.map(function(g){return [g,g]})).forEach(function(c){var b=document.createElement('button');b.type='button';b.textContent=c[1];b.setAttribute('aria-pressed','false');w.appendChild(b);
     b.onclick=function(){if(s.ch){o[s.key]=c[0];w.remove();say(c[1],'me');k++;ask();}else{var on=b.getAttribute('aria-pressed')!=='true';b.setAttribute('aria-pressed',on);}};});
    if(s.multi){var d=document.createElement('button');d.type='button';d.textContent='Done →';d.style.background='var(--go)';d.style.color='#04130B';w.appendChild(d);
     d.onclick=function(){o.goals=$$('button[aria-pressed=true]',w).map(function(b){return b.textContent});if(!o.goals.length)o.goals=['calls'];w.remove();say(o.goals.join(', '),'me');k++;ask();};}
    log.appendChild(w);log.scrollTop=log.scrollHeight;}
   else{form.classList.remove('off');inp.placeholder=s.ph;inp.value='';if(sec.dataset.seen)inp.focus({preventScroll:true});}});}
 form.addEventListener('submit',function(e){e.preventDefault();var v=inp.value.trim();if(!v)return;var s=Q[k];o[s.key]=v;say(v,'me');inp.value='';k++;form.classList.add('off');ask();});
 function done(){typing(function(){say('Perfect. '+(o.has==='no'?'I\'ll send your free preview within 48 hours.':'I\'ll send your free audit within one business day.')+' Tap below to send this to me on WhatsApp.','bot');
  var a=document.createElement('a');a.className='op-btn go';a.style.alignSelf='flex-start';a.style.marginTop='6px';a.href=wa(o);a.target='_blank';a.rel='noopener';a.textContent='Send on WhatsApp';log.appendChild(a);log.scrollTop=log.scrollHeight;});}
 var io=new IntersectionObserver(function(es){if(es[0].isIntersecting){sec.dataset.seen=1;ask();io.disconnect();}},{threshold:.35});io.observe(sec);});

/* D2 split card */
$$('.d2').forEach(function(sec){var f=$('form',sec),url=$('.d2-url',sec);
 function sync(){url.hidden=$('input[name=has]:checked',f).value==='no'}$$('input[name=has]',f).forEach(function(r){r.onchange=sync});sync();
 f.addEventListener('submit',function(e){e.preventDefault();var bad=false;['name','reach'].forEach(function(n){var el=f.elements[n];var b=!el.value.trim();el.setAttribute('aria-invalid',b);if(b)bad=true;});
  $('.d-err',f).textContent=bad?'Add your name and an email or phone so we know who to reply to.':'';if(bad)return;
  var o={name:f.elements.name.value.trim(),business:f.elements.business.value.trim(),has:$('input[name=has]:checked',f).value,website:f.elements.website.value.trim(),goals:$$('input[name=goal]:checked',f).map(function(x){return x.value}),reach:f.elements.reach.value.trim(),msg:f.elements.msg.value.trim()};
  $('.d2-done a',sec).href=wa(o);f.style.display='none';$('.d2-done',sec).style.display='block';});});

/* D3 one at a time */
$$('.d3-box').forEach(function(sec){var st=$$('.d3-step',sec),i=0,o={goals:[]},bar=$('.d3-prog i',sec),lab=$('.d3-prog .c',sec);
 function vis(k){return !(st[k].dataset.key==='website'&&o.has==='no')}
 function show(k,foc){i=k;st.forEach(function(s,j){s.classList.toggle('on',j===k)});var tot=st.length-2;bar.style.width=(Math.min(k,tot)/tot*100)+'%';lab.textContent=k>tot?'Sent':k===tot?'Review':(String(k+1)+' of '+tot);
  var inp=$('input',st[k]);if(inp&&foc!==false)setTimeout(function(){inp.focus({preventScroll:true})},50);if(st[k].dataset.key==='sum')sum();}
 function next(){var s=st[i],key=s.dataset.key,inp=$('input',s);if(inp){var v=inp.value.trim();if(!v&&inp.required){inp.setAttribute('aria-invalid','true');inp.focus();return;}o[key]=v;}
  var k=i+1;while(k<st.length&&!vis(k))k++;show(k);}
 function back(){var k=i-1;while(k>0&&!vis(k))k--;show(Math.max(0,k));}
 function sum(){var rows=[['Name',o.name],['Business',o.business],['Website',o.has==='no'?'Not yet':(o.website||'Yes')],['Wants more',(o.goals.length?o.goals:['calls']).join(', ')],['Reach at',o.reach]];
  $('.d3-sum',sec).innerHTML=rows.map(function(r){return '<div><span></span><b></b></div>'}).join('');$$('.d3-sum div',sec).forEach(function(d,j){$('span',d).textContent=rows[j][0];$('b',d).textContent=rows[j][1]||'-'});$$('.d3-wa',sec).forEach(function(a){a.href=wa(o)});}
 $$('.d3-step input',sec).forEach(function(inp){inp.addEventListener('keydown',function(e){if(e.key==='Enter'){e.preventDefault();next();}})});
 $$('.next',sec).forEach(function(b){b.onclick=next});$$('.back',sec).forEach(function(b){b.onclick=back});
 $$('.d3-ch',sec).forEach(function(w){var s=w.closest('.d3-step'),multi=s.dataset.key==='goals';$$('button',w).forEach(function(b){b.onclick=function(){
  if(multi){b.setAttribute('aria-pressed',b.getAttribute('aria-pressed')!=='true');o.goals=$$('button[aria-pressed=true]',w).map(function(x){return x.dataset.v});}
  else{$$('button',w).forEach(function(x){x.setAttribute('aria-pressed',x===b)});o[s.dataset.key]=b.dataset.v;setTimeout(next,reduce?0:260);}}})});
 document.addEventListener('mago:site',function(e){o.has=e.detail;$$('.d3-step[data-key=has] button',sec).forEach(function(b){b.setAttribute('aria-pressed',b.dataset.v===e.detail)});});
 var sb=$('.d3-send',sec),stt=$('.d3-status',sec);
 if(sb)sb.addEventListener('click',function(){if(!o.goals.length)o.goals=['calls'];sb.disabled=true;stt.textContent='Sending...';
  sendMail(o).then(function(how){stt.textContent='';try{(window.dataLayer=window.dataLayer||[]).push({event:'generate_lead',form:'contact',has_site:o.has||'yes',via:how})}catch(e){}
   if(how==='sent'){var k=st.length-1;show(k,false);}else{sb.disabled=false;stt.textContent='Your email app should open with the message ready. Nothing opened? Use WhatsApp instead.';}})
  .catch(function(){sb.disabled=false;stt.textContent='That didn\'t go through. Please try again, or send it on WhatsApp.';});});
 show(0,false);});
});
'''


def parts(ns, tagged=True):
    page, asset, E, it = ns["page"], ns["asset"], ns["E"], ns["it"]
    SITE, CONCEPTS, TESTIMONIALS, C, ROOT = ns["SITE"], ns["CONCEPTS"], ns["TESTIMONIALS"], ns["C"], ns["ROOT"]
    WA = ns["WA"]

    cons = []
    for slug, name, trade, where in CONCEPTS:
        f = slug[:16]
        cons.append({"slug": slug, "name": name, "trade": trade, "where": where, "url": f"https://{slug}.vercel.app/",
                     "poster": asset("/assets/concepts/poster/" + f + ".webp"), "long": asset("/assets/concepts/poster/" + f + "-scroll.webp")})

    def logo(src):
        if not src: return ""
        p = os.path.join(ROOT, "assets", "wall2", src + ".webp")
        return asset("/assets/wall2/" + src + ".webp") if os.path.exists(p) else asset("/assets/logos/" + src + ".webp")
    revs = [{"name": t["name"], "role": ", ".join(x for x in [t["role"], t["company"]] if x), "company": t["company"], "head": t["head"],
             "quote": t["quote"], "logo": logo(t["src"])} for t in TESTIMONIALS]

    def ph(c, cls=""):
        return (f'<a class="o-ph {cls}" href="{c["url"]}" target="_blank" rel="noopener" aria-label="{E(c["name"])}, concept website">'
                f'<span class="o-scr"><span class="bdg">Concept</span><img src="{c["poster"]}" alt="Mobile homepage of the concept website for {E(c["name"])}" width="440" height="901" loading="lazy" decoding="async">'
                f'<img class="long" data-src="{c["long"]}" alt="" aria-hidden="true"></span>'
                f'<span class="o-cap"><b>{E(c["name"])}</b><i>{E(c["trade"])} · {E(c["where"])}</i></span></a>')

    def tag(k, name, desc):
        if not tagged: return ''
        return f'<div class="wrap"><div class="op-tag"><span class="k">{k}</span><b>{E(name)}</b><i>{E(desc)}</i></div></div>'

    def group(id_, k, title, desc):
        return f'<div class="op-group" id="{id_}"><div class="wrap"><span>{k}</span><h2>{it(title)}</h2><p>{E(desc)}</p></div></div>'

    head_concepts = '<span class="op-lab">From the lab · Concept builds</span><h2 class="op-h" style="margin-top:18px">What we\'d build <em>for your trade.</em></h2>'
    note = f'<p>Working concept sites for trades businesses. Names and logos belong to their owners. {len(cons)} so far.</p>'

    # A1
    cols = [[], [], [], []]
    seq = cons + cons[:7]
    for i, c in enumerate(seq): cols[i % 4].append(ph(c))
    a1 = (f'<section class="op-sec op-dark a1" aria-label="Option A1">{tag("A1", "Parallax columns", "Four columns drift at different speeds as you scroll. Hover any phone to scroll that site.")}'
          f'<div class="wrap" style="margin-top:56px"><div class="a1-head"><div>{head_concepts}</div>{note}</div></div>'
          f'<div class="a1-view"><div class="a1-cols">{"".join(f"<div class=a1-col>{chr(10).join(c)}</div>" for c in cols)}</div></div></section>')
    # A2
    a2 = (f'<section class="op-sec op-dark a2" aria-label="Option A2">{tag("A2", "Centre stage", "One site at a time, front and centre. It scrolls itself, then the next one slides in. Swipe, click or use the arrows.")}'
          f'<div class="wrap" style="margin-top:56px">{head_concepts}</div>'
          f'<div class="a2-stage">{"".join(ph(c) for c in cons)}</div>'
          f'<div class="wrap"><div class="a2-bar"><div class="a2-info"><b>{E(cons[0]["name"])}</b><span>{E(cons[0]["trade"])} · {E(cons[0]["where"])}</span></div>'
          f'<div class="a2-ctl"><button class="op-round prev" type="button" aria-label="Previous concept">←</button><span class="n"></span><button class="op-round next" type="button" aria-label="Next concept">→</button></div>'
          f'<a class="live" href="{cons[0]["url"]}" target="_blank" rel="noopener">Open the live concept ↗</a></div>'
          f'<div class="a2-more">{ns["CNOTE"]}<a class="op-btn" href="{ns["href"]("/concepts/")}">See all {len(cons)} concepts</a></div></div></section>')
    # A3
    rows = "".join(f'<li><button type="button" role="tab" aria-selected="false"><span class="i">{i:02d}</span><span class="nm">{E(c["name"])}</span><span class="wh">{E(c["trade"])} · {E(c["where"])}</span></button></li>' for i, c in enumerate(cons, 1))
    bases = "".join(f'<img class="base" src="{c["poster"]}" alt="" loading="lazy" decoding="async">' for c in cons)
    a3 = (f'<section class="op-sec op-dark a3" aria-label="Option A3">{tag("A3", "Index and phone", "A typographic list of every trade. Hover a name and the phone beside it switches to that site and scrolls it.")}'
          f'<div class="wrap" style="margin-top:56px">{head_concepts}<div class="a3-grid"><ul class="a3-list" role="tablist" aria-label="Concept sites">{rows}</ul>'
          f'<div class="a3-ph"><span class="o-scr"><span class="bdg">Concept</span>{bases}<img class="long" alt="" aria-hidden="true"></span><div class="meta"><b></b><a href="#" target="_blank" rel="noopener">Open ↗</a></div></div></div></div></section>')

    # B
    vis = ['<div class="b-vis"><span>Calls this week</span><span class="v"><s>12</s> → <b>?</b></span></div>',
           '<div class="b-vis"><span>Your quote</span><span class="v">Fixed</span><span>In writing, before we start</span></div>',
           '<div class="b-vis"><span>Homepage design</span><span class="ok">✓ Approved by you</span></div>',
           '<div class="b-vis"><span>Status</span><span class="ok">● Live and tracking</span></div>']
    head_proc = f'<span class="op-lab">How it works</span><h2 class="op-h" style="margin-top:18px">{it(C.HOME["method_h"])}</h2>'
    b1p = "".join(f'<div class="b1-p"><span class="num">0{i + 1}</span><span class="when">{E(w)}</span><h3>{E(t)}</h3><p>{E(d)}</p>{vis[i]}</div>' for i, (w, t, d) in enumerate(C.METHOD))
    b1 = (f'<section class="op-sec op-ink b1" aria-label="Option B1">{tag("B1", "Sideways track", "The section holds still and the four steps slide past sideways as you scroll down. Stacks on phones.")}'
          f'<div class="b1-pin"><div class="wrap"><div class="b1-top"><div>{head_proc}</div></div><div class="b1-prog"><i></i></div></div><div class="b1-track">{b1p}</div></div></section>')
    b2c = "".join(f'<div class="b2-c"><span class="n">0{i + 1}</span><span class="when">{E(w)}</span><h3>{E(t)}</h3><p>{E(d)}</p>{vis[i]}</div>' for i, (w, t, d) in enumerate(C.METHOD))
    b2 = (f'<section class="op-sec op-paper b2" aria-label="Option B2">{tag("B2", "Journey line", "A green dot travels along one line as you scroll, lighting up each step as it arrives.")}'
          f'<div class="b2-in"><div class="wrap">{head_proc}<div class="b2-line"><span class="f"></span><span class="dot"></span></div><div class="b2-cols">{b2c}</div></div></div></section>')
    b3r = "".join(f'<div class="b3-row"><button type="button" aria-expanded="false"><span class="i">0{i + 1}</span><span class="t">{E(t)}</span><span class="w">{E(w)}</span></button>'
                  f'<div class="b3-body"><div><p>{E(d)}</p></div></div><div class="bar"><i></i></div></div>' for i, (w, t, d) in enumerate(C.METHOD))
    b3s = "".join(f'<div class="s{" on" if i_ == 0 else ""}">{v}</div>' for i_, v in enumerate(vis))
    b3 = (f'<section class="op-sec op-ink b3" aria-label="Option B3">{tag("B3", "Step player", "Steps play one after another with a timer bar, and the card on the right shows what you get at each step. Click any step.")}'
          f'<div class="wrap" style="margin-top:56px">{head_proc}<div class="b3-grid"><div class="b3-list">{b3r}</div><div class="b3-card">{b3s}<span class="big">01</span></div></div></div></section>')

    # C
    g = f'<a class="c1-badge" href="{SITE["google_reviews"]}" rel="noopener"><b>{SITE["rating"]}</b>★★★★★ · {SITE["review_count"]} Google reviews ↗</a>'
    dots = "".join(f'<button type="button" aria-label="Review {i + 1}"></button>' for i in range(len(revs)))
    c1 = (f'<section class="op-sec op-paper c1" aria-label="Option C1">{tag("C1", "One big quote", "One review at a time, huge, with the client logo and the result. Changes every few seconds.")}'
          f'<div class="wrap" style="margin-top:56px"><span class="op-lab">Reviews</span><h2 class="op-h" style="margin-top:18px">In their <em>own words.</em></h2>{g}'
          f'<div class="c1-swipe"><div class="c1-logo c1-fade">{(chr(60) + 'img src="' + revs[0]["logo"] + '" alt="' + E(revs[0]["company"]) + '">') if revs[0]["logo"] else ""}</div><blockquote class="c1-q c1-fade">\u201C{E(revs[0]["quote"])}\u201D</blockquote>'
          f'<span class="c1-res c1-fade">{E(revs[0]["head"])}</span><p class="c1-who c1-fade"><b>{E(revs[0]["name"])}</b>, <span>{E(revs[0]["role"])}</span></p></div>'
          f'<div class="c1-ctl"><button class="op-round prev" type="button" aria-label="Previous review">←</button><button class="op-round next" type="button" aria-label="Next review">→</button></div>'
          f'<div class="c1-dots">{dots}</div></div></section>')

    def c2card(r):
        lg = f'<img src="{r["logo"]}" alt="" loading="lazy">' if r["logo"] else f'<span>{E("".join(w[0] for w in r["name"].split()[:2]))}</span>'
        return (f'<div class="c2-card"><span class="st" aria-label="5 stars">★★★★★</span><span class="h">{E(r["head"])}</span><p>"{E(r["quote"])}"</p>'
                f'<div class="who"><span class="lg">{lg}</span><span><b>{E(r["name"])}</b><i>{E(r["role"])}</i></span></div></div>')
    cc = [[], [], []]
    for i, r in enumerate(revs): cc[i % 3].append(c2card(r))
    c2cols = "".join(f'<div class="c2-col{" rev" if j == 1 else ""}" style="--d:{[52, 64, 58][j]}s">{"".join(col)}{"".join(col)}</div>' for j, col in enumerate(cc))
    c2 = (f'<section class="op-sec op-dark c2" aria-label="Option C2">{tag("C2", "Wall of love", "Every review at once in slowly moving columns. Hover to pause and read.")}'
          f'<div class="wrap" style="margin-top:56px"><div class="c2-head"><div><span class="op-lab">Reviews</span><h2 class="op-h" style="margin-top:18px">In their <em>own words.</em></h2></div>'
          f'<a class="c2-badge" href="{SITE["google_reviews"]}" rel="noopener"><span class="n">{SITE["rating"]}</span><span class="s"><b>★★★★★</b>{SITE["review_count"]} Google reviews ↗</span></a></div>'
          f'<div class="c2-view"><div class="c2-cols">{c2cols}</div></div></div></section>')

    def c3card(r):
        lg = f'<span class="lg"><img src="{r["logo"]}" alt="" loading="lazy" draggable="false"></span>' if r["logo"] else ""
        return f'<div class="c3-card"><span class="res">{E(r["head"])}</span><p{' class="lq"' if len(r["quote"]) > 220 else ''}>"{E(r["quote"])}"</p><div class="who">{lg}<span><b>{E(r["name"])}</b><i>{E(r["role"])}</i></span></div></div>'
    c3 = (f'<section class="op-sec op-paper c3" aria-label="Option C3">{tag("C3", "Result cards", "Each review leads with the result it produced. Drag, swipe or use the arrows.")}'
          f'<div class="wrap" style="margin-top:56px"><div class="c3-top"><div><span class="op-lab">Reviews</span><h2 class="op-h" style="margin-top:18px">Results, <em>in their words.</em></h2>{g}</div>'
          f'<div class="c3-ctl"><button class="op-round prev" type="button" aria-label="Previous">←</button><button class="op-round next" type="button" aria-label="Next">→</button></div></div></div>'
          f'<div class="c3-rail">{"".join(c3card(r) for r in revs)}</div></section>')

    # D
    sofa = asset("/assets/founder/sofa.webp")
    d1 = (f'<section class="op-sec op-dark d1" aria-label="Option D1">{tag("D1", "Chat with Burhan", "Feels like messaging a person. Six quick questions, then one tap sends it to you on WhatsApp.")}'
          f'<div class="wrap" style="margin-top:56px"><div class="d1-grid"><div class="side"><span class="op-lab">Let\'s talk</span><h2 class="op-h" style="margin-top:18px">Your hardest working hire <em>starts here.</em></h2>'
          f'<p>Have a website? You get a free audit of where it loses customers. No website yet? You get a free working preview in 48 hours.</p>'
          f'<ul><li>Reply within one business day</li><li>No strings, no spam</li><li>Or <a href="{WA}" style="color:var(--paper)">WhatsApp Burhan directly</a></li></ul></div>'
          f'<div class="d1-win"><div class="d1-hd"><img src="{sofa}" alt="Burhan"><div><b>Burhan Kapasi</b><span>● Usually replies within a day</span></div></div>'
          f'<div class="d1-log" aria-live="polite"></div><form class="d1-in off"><label class="sr" for="d1i">Your answer</label><input id="d1i" autocomplete="off"><button type="submit" aria-label="Send">↑</button></form></div></div></div></section>')
    goals = "".join(f'<label><input type="checkbox" name="goal" value="{x}"{" checked" if x == "calls" else ""}><span>{x.capitalize()}</span></label>' for x in ["calls", "bookings", "enquiries", "sales"])
    d2 = (f'<section class="op-sec op-paper d2" aria-label="Option D2">{tag("D2", "Clean card", "A calm, conventional form done properly: clear labels, big tap targets, direct lines beside it.")}'
          f'<div class="wrap" style="margin-top:56px"><div class="d2-grid"><div class="d2-side"><span class="op-lab">Let\'s talk</span><h2 class="op-h" style="margin-top:18px">Your hardest working hire <em>starts here.</em></h2>'
          f'<p>Tell us where you are. You get a free audit, or a free working preview in 48 hours if you have no site yet.</p>'
          f'<div class="d2-lines"><a href="{WA}"><span>WhatsApp</span>{E(SITE.get("whatsapp_display", "+" + SITE["whatsapp"]))} ↗</a><a href="mailto:{SITE["email"]}"><span>Email</span>{E(SITE["email"])}</a><div><span>Reply</span>Within one business day</div></div></div>'
          f'<div class="d2-card"><form novalidate><div class="d2-row"><label class="d2-f"><span>Your name</span><input name="name" autocomplete="name"></label><label class="d2-f"><span>Business name</span><input name="business" autocomplete="organization"></label></div>'
          f'<div class="d2-f"><span>Do you have a website?</span><div class="d2-seg"><label><input type="radio" name="has" value="yes" checked><span>Yes, I do</span></label><label><input type="radio" name="has" value="no"><span>Not yet</span></label></div></div>'
          f'<label class="d2-f d2-url"><span>Website address</span><input name="website" inputmode="url" placeholder="yourbusiness.com"></label>'
          f'<div class="d2-f"><span>I want more</span><div class="d2-pills">{goals}</div></div>'
          f'<label class="d2-f"><span>Email or phone</span><input name="reach" autocomplete="email"></label>'
          f'<label class="d2-f"><span>Anything else? (optional)</span><textarea name="msg"></textarea></label>'
          f'<p class="d-err" role="alert"></p><div class="d2-send"><button class="op-btn ink" type="submit">Send it →</button><small>Free. No strings. We reply within one business day.</small></div></form>'
          f'<div class="d2-done d-ok"><h3>Ready to send.</h3><p>Tap below and your answers go to Burhan on WhatsApp.</p><a class="op-btn go" href="#" target="_blank" rel="noopener">Send on WhatsApp</a></div></div></div></div></section>')
    ch = lambda opts: "".join(f'<button type="button" data-v="{v}" aria-pressed="false">{E(l)}</button>' for v, l in opts)
    steps = [
        ('name', f'<label for="d3a">Hi, I\'m Burhan. <em>And you are?</em></label><input id="d3a" name="name" placeholder="Type your name" required autocomplete="name">'),
        ('business', f'<label for="d3b">What\'s your <em>business</em> called?</label><input id="d3b" name="business" placeholder="Business name" autocomplete="organization">'),
        ('has', f'<span class="d3-q">Do you have a <em>website</em> yet?</span><div class="d3-ch">{ch([("yes", "Yes, I do"), ("no", "Not yet")])}</div>'),
        ('website', f'<label for="d3c">Where can I <em>find it?</em></label><input id="d3c" name="website" placeholder="yourbusiness.com" inputmode="url">'),
        ('goals', f'<span class="d3-q">What do you want <em>more of?</em></span><div class="d3-ch">{ch([(g_, g_.capitalize()) for g_ in ["calls", "bookings", "enquiries", "sales"]])}</div>'),
        ('reach', f'<label for="d3d">Best way to <em>reach you?</em></label><input id="d3d" name="reach" placeholder="Email or phone" required autocomplete="email">'),
    ]
    d3s = "".join(f'<div class="d3-step" data-key="{k}">{h}<div class="d3-nav"><button class="op-btn next" type="button">OK →</button>'
                  f'{"<span class=hint>or press Enter</span>" if "input" in h else ""}{"" if i == 0 else "<button class=back type=button>Back</button>"}</div></div>' for i, (k, h) in enumerate(steps))
    d3s += ('<div class="d3-step" data-key="sum"><span class="d3-q">All set. <em>Send it?</em></span><div class="d3-sum"></div>'
            '<div class="d3-nav"><button class="op-btn go d3-send" type="button">Send it →</button><a class="d3-wa" href="#" target="_blank" rel="noopener">or send it on WhatsApp</a><button class="back" type="button">Back</button></div>'
            '<p class="d3-status" role="status" aria-live="polite"></p></div>'
            '<div class="d3-step" data-key="done"><span class="d3-q">Thank you. <em>It\'s with Burhan.</em></span>'
            '<p class="d3-done-p">You\'ll hear back within one business day. Want an answer sooner? <a class="d3-wa" href="#" target="_blank" rel="noopener">Message Burhan on WhatsApp</a>.</p></div>')
    d3box = f'<div class="d3-box"><div class="d3-prog"><span class="c">1 of 6</span><span class="t"><i style="width:0"></i></span></div>{d3s}</div>'
    d3 = (f'<section class="op-sec op-dark d3" aria-label="Option D3">{tag("D3", "One question at a time", "Full-screen, one big question per step with a progress bar. Press Enter to move on.")}'
          f'<div class="wrap">{d3box}</div></section>')

    data = json.dumps({"concepts": cons, "reviews": revs}, ensure_ascii=False).replace("</", "<\\/")
    return dict(a1=a1, a2=a2, a3=a3, b1=b1, b2=b2, b3=b3, c1=c1, c2=c2, c3=c3, d1=d1, d2=d2, d3=d3, d3box=d3box, data=data, group=group, it=it, E=E)


def build(ns):
    P = parts(ns, True)
    a1, a2, a3, b1, b2, b3, c1, c2, c3, d1, d2, d3, group, data, it, E = [P[k] for k in "a1 a2 a3 b1 b2 b3 c1 c2 c3 d1 d2 d3 group data it E".split()]
    jump = "".join(f'<a href="#{i}">{l}</a>' for i, l in [("g-a", "A · Concept builds"), ("g-b", "B · How it works"), ("g-c", "C · Reviews"), ("g-d", "D · Contact form")])
    body = (''
            f'<section class="op-intro op-paper"><div class="wrap"><span class="op-lab">Design options · not part of the live site</span><h1>Pick your <em style="font-family:Newsreader,serif;font-weight:300">favourites.</em></h1>'
            f'<p>Three live options for each of the four sections you flagged. Scroll, hover and click them like the real thing, then tell me a letter and number for each, like A2, B3, C1, D1.</p><div class="op-jump">{jump}</div></div></section>'
            + group("g-a", "Section A", "Concept builds", "Replaces the tilted lab floor.") + a1 + a2 + a3
            + group("g-b", "Section B", "How it works", "Replaces the rolling-number process section. No prices anywhere.") + b1 + b2 + b3
            + group("g-c", "Section C", "Reviews", "Replaces the review player. Uses all 11 written testimonials and the 8 Google reviews badge.") + c1 + c2 + c3
            + group("g-d", "Section D", "Contact form", "Replaces the fill-in-the-blanks form. Every option ends in a ready-to-send WhatsApp message.") + d1 + d2 + d3
            + f'<script type="application/json" id="op-data">{data}</script>')
    for k in ('op-dark', 'op-ink'):
        body = body.replace(f'class="op-sec {k}', f'data-dark class="op-sec {k}')
    body = body.replace('<div class="op-group"', '<div data-dark class="op-group"')
    page("/options/", "Design Options", "Design options for review.", body, noindex=True)

SITE_CSS = r"""
/* contact v2: calm background, one card, one question style */
.cx{position:relative;background:#0B0B0A;color:var(--paper);overflow:hidden;padding:clamp(90px,11vw,150px) 0 clamp(70px,8vw,110px)}
.cx-glow{position:absolute;inset:0;pointer-events:none;background:radial-gradient(60% 55% at 85% 0%,rgba(16,181,101,.13),transparent 70%),radial-gradient(50% 60% at 0% 100%,rgba(242,241,236,.05),transparent 70%)}
.cx .wrap{position:relative;z-index:1}
.cx-head{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;gap:14px 32px}
.cx .c-h{margin:0;font-size:clamp(20px,1.8vw,26px);color:#B9B7AF}
.cx-card{margin-top:36px;border-radius:32px;background:linear-gradient(180deg,#151514,#111110);border:1px solid #262624;padding:clamp(26px,5vw,72px);box-shadow:0 60px 120px -60px rgba(0,0,0,.9)}
.cx .d3-box{margin:0;max-width:none}
.cx .d3-step{margin-top:clamp(28px,4vw,48px)}
.cx .d3-step label,.cx .d3-step .d3-q{display:block;font-size:clamp(30px,4.2vw,60px);line-height:1.02;letter-spacing:-.05em;color:var(--paper);background:none;border:0;padding:0;width:auto}
.cx .d3-step input{border-bottom-color:#33332F}
.cx .d3-sum div{font-size:17px}
.cx .d3-nav{gap:14px 22px}
.cx .d3-wa{color:#C9C7BF;font-size:15px;text-decoration:none;border-bottom:1px solid rgba(242,241,236,.3);padding-bottom:2px}
.cx .d3-wa:hover{color:var(--go);border-color:var(--go)}
.d3-status{min-height:1.4em;margin-top:16px;color:#C9C7BF;font-size:15px}
.d3-done-p{margin-top:22px;color:#B9B7AF;font-size:18px;max-width:46ch}
.d3-done-p a{color:var(--paper)}
.d3-send[disabled]{opacity:.6;cursor:progress}
.cx .d3-alt{display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px 28px;align-items:center;margin-top:28px;color:#8F8D86;font-size:14.5px}
.cx .d3-alt a{color:var(--paper);text-decoration:none;border-bottom:1px solid rgba(242,241,236,.35);padding-bottom:3px;display:inline-flex;gap:8px;align-items:center}
.cx .d3-alt a:hover{border-color:var(--go);color:var(--go)}
@media (max-width:700px){.cx-card{border-radius:24px}.cx .d3-alt{flex-direction:column;align-items:flex-start}}
.formgrid.solo{display:block}.formgrid.solo .intro{max-width:880px}
/* chosen sections on the live site */
.a2-more{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:20px;margin-top:44px;padding-top:28px;border-top:1px solid #2A2A28}
.a2-more .cnote,.a2-more>div:first-child{max-width:720px}
.c1-swipe{touch-action:pan-y;user-select:none;-webkit-user-select:none;cursor:grab}
.c1-swipe:active{cursor:grabbing}
@media (pointer:coarse){.d3-nav .hint{display:none}}
.contact-sec .d3-box{margin-top:36px;position:relative;z-index:2}
.contact-sec .d3-step label,.contact-sec .d3-step .d3-q{font-size:clamp(30px,4.4vw,64px)}
.contact-sec .d3-step{margin-top:40px}
.contact-sec .c-h{max-width:none;font-size:clamp(20px,2vw,28px);letter-spacing:-.03em;margin-top:18px;color:#DAD8D0;font-weight:400}
.contact-sec .c-h em{font-family:"Newsreader",serif;font-weight:300}
.contact-sec .d3-alt{display:flex;flex-wrap:wrap;gap:12px 28px;align-items:center;margin-top:44px;color:#B9B7AF;font-size:15px}
.contact-sec .d3-alt a{color:var(--paper);text-decoration:none;border-bottom:1px solid rgba(242,241,236,.4);padding-bottom:3px;display:inline-flex;gap:8px;align-items:center}
.contact-sec .d3-alt a:hover{border-color:var(--go);color:var(--go)}
"""
