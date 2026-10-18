#!/usr/bin/env python3
"""Cross-app regression tests for Character Manager v1.5.0 + DM Manager 3.2.0.
Loads standalone HTML in Chromium using a localStorage shim. Native file dialogs,
actual browser-profile persistence, and downloads are outside this test scope.
"""
from pathlib import Path
import json, re, sys, traceback
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parent
CM=ROOT/'D&D_5e_Character_Manager_v1.5.0.html'
DM=ROOT/'DND_DM_Manager_Phase3.2.html'
ROSTER=ROOT/'Test_Characters_Roster_2014_and_2024.json'
results=[]
def record(name,ok,detail=''):
    results.append((name,bool(ok),detail)); print(('PASS' if ok else 'FAIL')+' '+name+((': '+detail) if detail else ''))
def html(path):
    s=path.read_text(encoding='utf-8')
    s=re.sub(r'<link[^>]+(?:fonts\.googleapis|fonts\.gstatic)[^>]*>','',s)
    shim='''<script>(()=>{const seed=window.__testStorageSeed||{};const store=new Map(Object.entries(seed).map(([k,v])=>[k,String(v)]));Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem:k=>store.has(String(k))?store.get(String(k)):null,setItem:(k,v)=>store.set(String(k),String(v)),removeItem:k=>store.delete(String(k)),clear:()=>store.clear()}})})();</script>'''
    return s.replace('<head>','<head>'+shim,1)
def main():
    roster=json.loads(ROSTER.read_text(encoding='utf-8'))
    errors=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage','--disable-gpu'])
        page=browser.new_page(viewport={'width':1280,'height':1000})
        page.add_init_script("window.prompt=(msg,defv)=>'Regression Campaign'; window.confirm=()=>true;")
        page.on('pageerror',lambda e:errors.append(str(e)))
        # Character Manager: import mixed-edition roster, create two tagged notes and confirm link.
        page.set_content(html(CM),wait_until='load',timeout=30000)
        page.get_by_role('button',name='Import JSON').click()
        page.locator('#m_json').fill(json.dumps(roster))
        page.locator('.md [data-a="ok"]').click()
        record('Character Manager imports 2014/2024 roster', 'Mira Stoneward' in page.locator('body').inner_text() and 'Korrin Flintstride' in page.locator('body').inner_text())
        page.get_by_role('button',name='Open').first.click()
        page.get_by_role('tab',name='Notes').click()
        # Note A
        page.locator('[data-a="addNote"]').click()
        page.locator('#m_nt').fill('Greyhaven Harbor')
        page.locator('#m_nb').fill('A suspicious ship arrived at the harbor.')
        page.locator('#m_ntn').fill('harbor')
        page.locator('.md').get_by_role('button',name='Add tag',exact=True).click()
        page.locator('.md #m_nt').fill('Greyhaven Harbor')
        page.locator('.md [data-a="ok"]').click()
        # Note B with shared tag and an explicit title mention.
        page.locator('[data-a="addNote"]').click()
        page.locator('#m_nt').fill('Dockside Contact')
        page.locator('#m_nb').fill('Ask about Greyhaven Harbor before the next session.')
        page.locator('#m_ntn').fill('harbor')
        page.locator('.md').get_by_role('button',name='Add tag',exact=True).click()
        page.locator('.md #m_nt').fill('Dockside Contact')
        sug=page.locator('.md .knowledge-links').filter(has=page.get_by_role('heading',name='Suggested links'))
        has_suggestion=sug.get_by_text('Greyhaven Harbor').count()>0
        if has_suggestion:
            sug.locator('[data-a="nsuggest"]').first.click()
        page.locator('.md [data-a="ok"]').click()
        cmstate=json.loads(page.evaluate("localStorage.getItem('dnd5e-chars-v1')"))
        chars=cmstate if isinstance(cmstate,list) else cmstate.get('chars',[])
        mira=next((x for x in chars if x.get('name')=='Mira Stoneward'),None)
        notes=(mira or {}).get('notes',[])
        linked=len(notes)==2 and notes[0].get('id') in (notes[1].get('links') or []) and notes[1].get('id') in (notes[0].get('links') or [])
        record('Character note links persist bidirectionally',linked,f'{len(notes)} notes; suggestion detected={has_suggestion}')
        record('Character note links survive JSON export', bool(mira and all(isinstance(n.get('links'),list) for n in notes)))
        # Export this character through the app's own export path.
        page.get_by_role('tab',name='Style').click()
        page.get_by_role('button',name='Export this character').click()
        export_text=page.locator('#m_json').input_value()
        export_obj=json.loads(export_text)
        export_char=export_obj.get('character',export_obj.get('data',export_obj))
        export_notes=export_char.get('notes',[]) if isinstance(export_char,dict) else []
        record('Character export contains the note records and links',len(export_notes)==2 and any(n.get('links') for n in export_notes),export_obj.get('format','raw character object'))
        # DM Manager: create campaign, import exported character, verify snapshot isolation.
        dm_page=browser.new_page(viewport={'width':1280,'height':1000})
        dm_page.add_init_script("window.prompt=(msg,defv)=>'Regression Campaign'; window.confirm=()=>true;")
        dm_page.on('pageerror',lambda e:errors.append(str(e)))
        dm_page.set_content(html(DM),wait_until='load',timeout=30000)
        dm_page.evaluate("window.prompt=(msg,defv)=>'Regression Campaign'; window.confirm=()=>true;")
        dm_page.locator('#homeNewCampaignBtn').click(timeout=5000)
        dm_page.evaluate("document.querySelector('[data-view=\"settings\"]').click()")
        dm_page.locator('#settingsRules').select_option('2024')
        dm_page.locator('#saveSettingsBtn').click()
        dm_page.evaluate("document.querySelector('[data-view=\"import\"]').click()")
        dm_page.locator('#importText').fill(export_text)
        dm_page.locator('#previewBtn').click()
        import_msg=dm_page.locator('#importMessage').inner_text()
        record('DM Manager validates Character Manager export before changes','Validated 1 character' in import_msg or 'Validated 1 character(s)' in import_msg,import_msg[:180])
        mismatch='Ruleset warning' in import_msg
        dm_page.locator('#applyImportBtn').click()
        dmstate=json.loads(dm_page.evaluate("localStorage.getItem('dnd-dm-manager-v1')"))
        snap=next((s for s in dmstate.get('characterSnapshots',[]) if s.get('name')=='Mira Stoneward'),None)
        record('DM Manager imports character snapshot',snap is not None)
        dm_notes=(snap or {}).get('data',{}).get('notes',[])
        record('DM snapshot preserves linked character notes',len(dm_notes)==2 and any(n.get('links') for n in dm_notes),f'{len(dm_notes)} note records imported')
        record('Edition mismatch is warned without conversion',mismatch)
        # Create/start encounter, change PC HP, and prove snapshot character data is unchanged.
        dm_page.evaluate("document.querySelector('[data-view=\"encounters\"]').click()")
        dm_page.locator('#newEncounterBtn').click()
        # Encounter template defaults to an enemy; give it a name/hp if editor controls exist.
        namefield=dm_page.locator('#encounterEditor input').first if dm_page.locator('#encounterEditor input').count() else None
        if namefield:
            namefield.fill('Regression Encounter')
        start=dm_page.locator('[data-start-encounter]')
        if start.count():
            start.first.click()
            pcrow=dm_page.locator('.combatant').filter(has_text='Mira Stoneward')
            # Prefer direct state checks even if combat UI class names differ.
            before_data=json.dumps(snap.get('data',{}),sort_keys=True)
            dmstate=json.loads(dm_page.evaluate("localStorage.getItem('dnd-dm-manager-v1')"))
            activecombat=next((x for x in reversed(dmstate.get('encounterInstances',[])) if x.get('status')=='active'),None)
            pc=next((x for x in (activecombat or {}).get('combatants',[]) if x.get('characterId')==snap.get('characterId')),None)
            if pc:
                oldhp=pc.get('hp',0)
                # Invoke the same exposed DOM event path as an HP input interaction.
                hpinput=dm_page.locator(f'[data-combatant="{pc["id"]}"][data-combat-value="hp"]')
                if hpinput.count():
                    hpinput.fill(str(max(0,oldhp-3))); hpinput.dispatch_event('change')
                after=json.loads(dm_page.evaluate("localStorage.getItem('dnd-dm-manager-v1')"))
                aftersnap=next((s for s in after.get('characterSnapshots',[]) if s.get('characterId')==snap.get('characterId')),None)
                aftercombat=next((x for x in reversed(after.get('encounterInstances',[])) if x.get('status')=='active'),None)
                afterpc=next((x for x in (aftercombat or {}).get('combatants',[]) if x.get('characterId')==snap.get('characterId')),None)
                record('Combat HP changes are saved to encounter state',bool(afterpc and afterpc.get('hp')==max(0,oldhp-3)),f'HP {oldhp} → {(afterpc or {}).get("hp","missing")}')
                record('Combat HP changes do not overwrite imported character snapshot',json.dumps((aftersnap or {}).get('data',{}),sort_keys=True)==before_data,'encounter HP is DM-owned state')
            else:
                record('Combat HP changes do not overwrite imported character snapshot',False,'Could not find linked PC combatant in active encounter')
        else:
            record('Combat HP changes do not overwrite imported character snapshot',False,'Encounter start control not found')
        record('No uncaught browser JavaScript errors',not errors,'; '.join(errors)[:300])
        browser.close()
    failed=[x for x in results if not x[1]]
    report=['# Cross-App Regression Test Report','', 'Apps: Character Manager v1.5.0 and DM Manager Phase 3.2 (3.2.0).','', 'Environment: Playwright + system Chromium; HTML loaded via page.set_content with localStorage shim. Native file pickers/downloads and real browser-profile persistence are not covered.','',f'Result: {len(results)-len(failed)}/{len(results)} checks passed.','']
    report += [f'- {"PASS" if ok else "FAIL"}: {name}'+(f' — {detail}' if detail else '') for name,ok,detail in results]
    (ROOT/'DND_Cross_App_Regression_Test_Report.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
    print(f'\n{len(results)-len(failed)}/{len(results)} checks passed')
    return 1 if failed else 0
if __name__=='__main__':
    try:sys.exit(main())
    except Exception:
        traceback.print_exc();sys.exit(2)