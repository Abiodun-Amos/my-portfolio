import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        errs=[]
        jobs=[('h-dark',1440,900,'index.html','dark',False),('h-light',1440,900,'index.html','light',False),('h-short',1150,620,'index.html','dark',False),('h-tab',820,900,'index.html','light',False),('h-mob',390,844,'index.html','light',False),
              ('about',1440,900,'about.html','light',False),('speak',1440,900,'speaking.html','dark',True),('home-full',1440,900,'index.html','light',True),('gal',1440,900,'gallery.html','dark',True),('about-tab',900,900,'about.html','dark',False)]
        for name,w,h,page,theme,full in jobs:
            ctx = await b.new_context(viewport={'width':w,'height':h})
            await ctx.add_init_script(f"try{{localStorage.setItem('aa-theme','{theme}')}}catch(e){{}}")
            pg = await ctx.new_page()
            pg.on('pageerror', lambda e: errs.append(str(e)))
            await pg.goto('file:///home/claude/site/dist/'+page); await pg.wait_for_timeout(2200)
            if full:
                await pg.add_style_tag(content='.js .reveal{opacity:1!important;transform:none!important}.js .clip{clip-path:none!important}.header{position:absolute!important}html{scroll-behavior:auto!important}')
                hh = await pg.evaluate('document.documentElement.scrollHeight')
                for y in range(0,hh,700):
                    await pg.evaluate(f'window.scrollTo(0,{y})'); await pg.wait_for_timeout(100)
                await pg.evaluate('window.scrollTo(0,0)'); await pg.wait_for_timeout(400)
            if name=='about-tab': await pg.evaluate('window.scrollTo(0,520)'); await pg.wait_for_timeout(900)
            ov = await pg.evaluate('document.documentElement.scrollWidth - window.innerWidth')
            if ov>0: print(name,'overflow',ov)
            await pg.screenshot(path=f'/tmp/n-{name}.jpg', type='jpeg', quality=62, full_page=full)
            await ctx.close()
        print('errors',set(errs)); await b.close()
asyncio.run(main())
