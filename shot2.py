import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        errs=[]
        for name,w,page in [('about',1440,'about.html'),('gallery',1440,'gallery.html'),('contact',1440,'contact.html'),('case',1440,'project-fruit.html'),('speaking',1440,'speaking.html'),('expertise',1440,'expertise.html'),('m-about',390,'about.html'),('m-projects',390,'projects.html')]:
            pg = await b.new_page(viewport={'width':w,'height':900})
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.on('console', lambda m: errs.append(m.text) if m.type=='error' else None)
            await pg.goto('file:///home/claude/site/dist/'+page); await pg.wait_for_timeout(1500)
            if name=='expertise': await pg.click('#ai .xp__head')
            if name=='contact':
                await pg.fill('#cf-name','Test'); await pg.fill('#cf-message','Hello'); await pg.click('#contact-form button[type=submit]')
            await pg.add_style_tag(content='.js .reveal{opacity:1!important;transform:none!important}.js .clip{clip-path:none!important}.header{position:absolute!important}html{scroll-behavior:auto!important}')
            h = await pg.evaluate('document.documentElement.scrollHeight')
            for y in range(0,h,700):
                await pg.evaluate(f'window.scrollTo(0,{y})'); await pg.wait_for_timeout(120)
            await pg.evaluate('window.scrollTo(0,0)'); await pg.wait_for_timeout(500)
            await pg.screenshot(path=f'/tmp/s-{name}.jpg', type='jpeg', quality=60, full_page=True)
            ov = await pg.evaluate('document.documentElement.scrollWidth - window.innerWidth')
            print(name,h,'overflow-x',ov)
            await pg.close()
        print('errors',set(errs))
        await b.close()
asyncio.run(main())
