import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        for name,w,h,page,full in [('home-d',1440,900,'index.html',False),('home-m',390,844,'index.html',False),('home-full',1440,900,'index.html',True),('about-full',1440,900,'about.html',True)]:
            pg = await b.new_page(viewport={'width':w,'height':h})
            await pg.goto('file:///home/claude/site/dist/'+page); await pg.wait_for_timeout(2400)
            if full:
                await pg.add_style_tag(content='.js .reveal{opacity:1!important;transform:none!important}.js .clip{clip-path:none!important}.header{position:absolute!important}')
                await pg.wait_for_timeout(300)
            await pg.screenshot(path=f'/tmp/{name}.jpg', type='jpeg', quality=60, full_page=full)
            await pg.close()
        await b.close()
asyncio.run(main())
