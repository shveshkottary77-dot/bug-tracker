import React, { useState, useEffect } from 'react'
import Editor from '@monaco-editor/react'
import { analyze as analyzeApi } from '../services/api'
import { useNavigate } from 'react-router-dom'

export default function Analyze(){
  const [code, setCode] = useState('')
  const [fileInfo, setFileInfo] = useState<{name:string,size:number,lines:number}|null>(null)
  const [loading, setLoading] = useState(false)
  const [liveMessage, setLiveMessage] = useState<string>('')
  const nav = useNavigate()
  const analyze = async () => {
    if(!code) return alert('Please paste code or upload a file')
    setLoading(true)
    setLiveMessage('Analyzing: parsing source and building AST')
    try{
      setLiveMessage('Sending source to analyzer')
      const res = await analyzeApi('snippet.py', code)
      setLiveMessage('Analysis complete')
      setLoading(false)
      nav('/history')
    }catch(e:any){
      setLoading(false)
      setLiveMessage('Analysis failed')
      alert(e?.response?.data?.error || 'Analysis failed')
    }
  }
  // keyboard shortcut: Ctrl/Cmd + Enter to analyze
  useEffect(()=>{
    const handler = (e: KeyboardEvent) => {
      if((e.ctrlKey || e.metaKey) && e.key === 'Enter'){
        e.preventDefault()
        analyze()
      }
    }
    window.addEventListener('keydown', handler)
    return ()=> window.removeEventListener('keydown', handler)
  },[code])
  const onFile = (f?: File|null) => {
    if(!f) return
    const reader = new FileReader()
    reader.onload = () => {
      const txt = String(reader.result || '')
      setCode(txt)
      setFileInfo({ name: f.name, size: f.size, lines: txt.split(/\r?\n/).length })
    }
    reader.readAsText(f)
  }
  return (
    <div>
      <header className="mb-4">
        <h2 className="text-2xl font-semibold">Analyze Python Code</h2>
        <p className="text-slate-400">Upload a Python file or paste your code below.</p>
      </header>
      <div aria-live="polite" aria-atomic="true" className="sr-only">{liveMessage}</div>
      {loading && (
        <div className="mb-4">
          <div className="w-full bg-slate-700 rounded h-2 overflow-hidden">
            <div className="h-2 bg-indigo-500 animate-pulse" style={{width: '60%'}} />
          </div>
          <div className="text-sm text-slate-300 mt-1">{liveMessage}</div>
        </div>
      )}
      <div className="mb-4 flex items-center gap-4">
        <label className="bg-slate-700 px-3 py-2 rounded cursor-pointer">
          Upload .py
          <input accept=".py" onChange={(e)=>onFile(e.target.files?.[0]||null)} type="file" className="hidden" />
        </label>
        {fileInfo && <div className="text-sm text-slate-400">{fileInfo.name} • {fileInfo.lines} lines • {(fileInfo.size/1024).toFixed(1)} KB</div>}
      </div>
      <div className="mb-4 relative">
        <Editor height="400px" defaultLanguage="python" theme="vs-dark" value={code} onChange={v=>setCode(v||'')} />
        {loading && (
          <div className="absolute inset-0 bg-black/40 flex items-center justify-center">
            <div className="bg-slate-800 p-6 rounded shadow-lg text-center">
              <div className="animate-pulse text-lg">Analyzing your code...</div>
              <div className="text-sm text-slate-400 mt-2">Parsing AST · Calculating complexity · Detecting code smells</div>
            </div>
          </div>
        )}
      </div>
      <div className="flex gap-2">
        <button onClick={analyze} className="px-4 py-2 bg-indigo-600 rounded" disabled={loading}>{loading? 'Analyzing...':'Analyze Code'}</button>
        <button onClick={()=>setCode('')} className="px-4 py-2 bg-slate-700 rounded">Clear</button>
      </div>
    </div>
  )
}
