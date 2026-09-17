import React, { useEffect, useState } from 'react'
import { getHistory } from '../services/api'
import { useNavigate } from 'react-router-dom'

export default function History(){
  const [items, setItems] = useState<any[]>([])
  const nav = useNavigate()
  useEffect(()=>{
    (async ()=>{
      try{
        const res = await getHistory()
        setItems(res.data.history || [])
      }catch(e){
        console.error(e)
      }
    })()
  },[])
  return (
    <div>
      <h2 className="text-2xl font-semibold mb-4">Analysis History</h2>
      <div className="space-y-3">
        {items.length===0 && <div className="p-6 bg-slate-800 rounded text-center">No analyses yet. Use <strong>Analyze Code</strong> to create your first report.</div>}
        {items.map(it=> (
          <div key={it.id} className="p-4 bg-gradient-to-r from-slate-800 to-slate-900 rounded flex justify-between items-center hover:scale-[1.01] transition-transform">
            <div>
              <div className="font-medium">{it.filename}</div>
              <div className="text-sm text-slate-400">{new Date(it.timestamp).toLocaleString()}</div>
            </div>
            <div className="text-right">
              <div className="font-semibold text-lg">{it.score}</div>
              <div className="text-sm text-slate-400">{it.issue_count} issues</div>
              <div className="mt-2 flex gap-2 justify-end">
                <button onClick={()=>nav(`/history/${it.id}`)} className="px-3 py-1 bg-indigo-600 rounded text-sm">View</button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
