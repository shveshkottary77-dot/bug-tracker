import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import api from '../services/api'
import Editor, { OnMount } from '@monaco-editor/react'
import * as monacoEditor from 'monaco-editor'

export default function Result(){
  const { id } = useParams()
  const [analysis, setAnalysis] = useState<any>(null)
  useEffect(()=>{
    (async ()=>{
      if(!id) return
      try{
        const res = await api.get(`/history/${id}`)
        setAnalysis(res.data.analysis)
      }catch(e){
        console.error(e)
      }
    })()
  },[id])
  if(!analysis) return <div>Loading...</div>
  const code = analysis && analysis.metrics && analysis.metrics.source || ''
  const [editorApi, setEditorApi] = useState<monacoEditor.editor.IStandaloneCodeEditor| null>(null)
  const [monacoApi, setMonacoApi] = useState<typeof monacoEditor | null>(null)
  const [decorations, setDecorations] = useState<string[]>([])
  const [selectedIdx, setSelectedIdx] = useState<number>(-1)
  const [toast, setToast] = useState<string | null>(null)
  const onMount: OnMount = (editor, monaco) => {
    setEditorApi(editor)
    setMonacoApi(monaco as unknown as typeof monacoEditor)
  }

  // keyboard navigation: when container is focused, arrow keys navigate issues
  useEffect(()=>{
    const handler = (e: KeyboardEvent) => {
      if(!(document.activeElement && (document.activeElement as HTMLElement).id === 'issues-list')) return
      if(!analysis || !analysis.issues) return
      if(e.key === 'ArrowDown'){
        e.preventDefault()
        setSelectedIdx(i=> Math.min(i+1, analysis.issues.length-1))
      }else if(e.key === 'ArrowUp'){
        e.preventDefault()
        setSelectedIdx(i=> Math.max(i-1, 0))
      }else if(e.key === 'Enter'){
        e.preventDefault()
        const it = analysis.issues[selectedIdx]
        if(it){
          const ln = it.line || it.lineno || 1
          if(editorApi){
            editorApi.revealPositionInCenter({ lineNumber: ln, column: 1 })
            const newDec = monacoApi ? [{ range: new monacoApi.Range(ln,1,ln,1), options: { isWholeLine: true, className: 'lineHighlight' } }] : []
            if(monacoApi){
              const ids = editorApi.deltaDecorations(decorations, newDec)
              setDecorations(ids)
              setTimeout(()=>{ editorApi.deltaDecorations(ids, []) }, 3500)
            }
          }
        }
      }
    }
    window.addEventListener('keydown', handler)
    return ()=> window.removeEventListener('keydown', handler)
  },[analysis, editorApi, monacoApi, decorations, selectedIdx])
  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-semibold">Analysis Result — {analysis.filename}</h2>
        <div className="flex gap-2">
          <button className="px-3 py-1 bg-slate-700 rounded" onClick={async ()=>{
            try{ await navigator.clipboard.writeText(analysis.metrics?.source || '')
              setToast('Code copied to clipboard')
              setTimeout(()=>setToast(null),2000)
            }catch(e){ setToast('Copy failed'); setTimeout(()=>setToast(null),2000) }
          }}>Copy Code</button>
          <button className="px-3 py-1 bg-slate-700 rounded" onClick={()=>{
            const data = JSON.stringify(analysis, null, 2)
            const blob = new Blob([data], { type: 'application/json' })
            const url = URL.createObjectURL(blob)
            const a = document.createElement('a')
            a.href = url
            a.download = `${analysis.filename || 'analysis'}.codesense.json`
            a.click()
            URL.revokeObjectURL(url)
          }}>Download Report</button>
          <button className="px-3 py-1 bg-indigo-600 rounded" onClick={async ()=>{
            const shareUrl = window.location.href
            try{ await navigator.clipboard.writeText(shareUrl)
              setToast('Share link copied')
              setTimeout(()=>setToast(null),2000)
            }catch(e){ setToast('Copy failed'); setTimeout(()=>setToast(null),2000) }
          }}>Share Link</button>
        </div>
      </div>
      {toast && <div className="fixed bottom-6 right-6 bg-slate-900 text-white px-4 py-2 rounded shadow">{toast}</div>}
      <div className="grid grid-cols-3 gap-4">
        <div className="p-4 bg-slate-800 rounded">
          <div className="text-sm text-slate-400">Quality Score</div>
          <div className="text-3xl font-bold">{analysis.overall_score}</div>
          <div className="text-sm">{analysis.quality_level}</div>
        </div>
        <div className="p-4 bg-slate-800 rounded col-span-2">
          <div className="text-sm text-slate-400">Summary</div>
          <pre className="text-sm mt-2 max-h-60 overflow-auto">{JSON.stringify(analysis.component_scores, null, 2)}</pre>
        </div>
      </div>
      <section className="mt-6 grid grid-cols-2 gap-4">
        <div>
          <h3 className="text-xl font-semibold mb-2">Code</h3>
          <div className="bg-slate-800 rounded p-2">
                <Editor height="360px" defaultLanguage="python" theme="vs-dark" value={analysis.metrics && analysis.metrics.source || ''} options={{readOnly:true,lineNumbers:'on',minimap:{enabled:false}}} onMount={onMount} />
          </div>
        </div>
        <div>
          <h3 className="text-xl font-semibold mb-2">Issues</h3>
          <div id="issues-list" tabIndex={0} role="listbox" aria-label="Issues list" className="space-y-3">
            {analysis.issues && analysis.issues.map((it:any, idx:number)=> (
              <div key={idx} role="option" aria-selected={selectedIdx===idx} tabIndex={0} onFocus={()=>setSelectedIdx(idx)} className={`p-3 bg-slate-800 rounded border-l-4 border-indigo-600 ${selectedIdx===idx? 'ring-2 ring-indigo-600':''}`}>
                <div className="flex items-center justify-between">
                  <button className="text-left flex-1" onClick={()=>{
                    const ln = it.line || it.lineno || 1
                    if(editorApi){
                      editorApi.revealPositionInCenter({ lineNumber: ln, column: 1 })
                      const newDec = monacoApi ? [{ range: new monacoApi.Range(ln,1,ln,1), options: { isWholeLine: true, className: 'lineHighlight' } }] : []
                      if(monacoApi){
                        const ids = editorApi.deltaDecorations(decorations, newDec)
                        setDecorations(ids)
                        setTimeout(()=>{ editorApi.deltaDecorations(ids, []) }, 3500)
                      }
                    }
                  }} aria-label={`Highlight code line ${it.line || it.lineno || 1}`}>
                    <div className="font-semibold">{it.title}</div>
                    <div className="text-sm text-slate-400 mt-1">{it.description}</div>
                  </button>
                  <div className={`ml-3 px-2 py-1 rounded text-sm ${it.severity==='HIGH' || it.severity==='CRITICAL' ? 'bg-red-600':'bg-yellow-600'}`} role="status">{it.severity}</div>
                </div>
                <div className="text-sm mt-2">Suggestion: {it.suggestion}</div>
                <div className="mt-2 text-xs text-slate-500">Line: {it.line}</div>
                {code && (
                  <pre className="mt-2 text-xs bg-black/20 p-2 rounded max-h-28 overflow-auto">{code.split(/\r?\n/).slice(Math.max(0,(it.line||it.lineno||1)-3), (it.line||it.lineno||1)+2).join('\n')}</pre>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  )
}
