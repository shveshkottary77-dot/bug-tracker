const fs = require('fs')
const { chromium } = require('playwright')
const axe = require('axe-core')

async function run(url){
  const browser = await chromium.launch({ args: ['--no-sandbox'] })
  const page = await browser.newPage()
  console.log('Opening', url)
  await page.goto(url, { waitUntil: 'networkidle' })
  // inject axe
  const axeSource = axe.source
  await page.addScriptTag({ content: axeSource })
  console.log('Running axe-core...')
  const results = await page.evaluate(async () => {
    return await axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa'] } })
  })
  await browser.close()
  fs.writeFileSync('axe-report.json', JSON.stringify(results, null, 2))
  console.log('Wrote axe-report.json — violations:', results.violations.length)
  if(results.violations && results.violations.length>0){
    console.error('Accessibility violations found:')
    results.violations.forEach(v=>{
      console.error(`- ${v.id}: ${v.help} (${v.impact}) — nodes: ${v.nodes.length}`)
    })
    process.exit(2)
  }
  console.log('No accessibility violations found.')
  process.exit(0)
}

const url = process.argv[2] || 'http://localhost:5177'
run(url).catch(e=>{ console.error(e); process.exit(3) })
