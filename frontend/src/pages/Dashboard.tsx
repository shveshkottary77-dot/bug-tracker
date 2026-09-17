import React, { useEffect, useState } from 'react'
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import api from '../services/api'

const COLORS = ['#4f46e5','#06b6d4','#f97316','#ef4444','#a78bfa','#f59e0b']

export default function Dashboard(){
  const [history, setHistory] = useState<any[]>([])
  useEffect(()=>{
    (async ()=>{
      try{
        const res = await api.get('/history')
        setHistory(res.data.history || [])
      }catch(e){
        console.error(e)
      }
    })()
  },[])
  const trendData = history.slice(0,10).map(h=>({ name: new Date(h.timestamp).toLocaleDateString(), score: h.score }))
  const distribution = [
    { name: 'Complexity', value: 20 },
    { name: 'Naming', value: 12 },
    { name: 'Maintainability', value: 18 },
    { name: 'Duplication', value: 10 },
    { name: 'Documentation', value: 25 },
    { name: 'Style', value: 15 }
  ]
  return (
    <div>
      <header className="mb-6">
        <h2 className="text-3xl font-semibold">Good evening 👋</h2>
        <p className="text-slate-400">Analyze your Python code. Understand complexity. Find problems. Improve quality.</p>
      </header>
      <div className="grid grid-cols-4 gap-4 mb-6">
        <div className="p-4 bg-slate-800 rounded">Total Analyses<br/><strong>{history.length}</strong></div>
        <div className="p-4 bg-slate-800 rounded">Average Quality<br/><strong>{history.length? Math.round(history.reduce((s,a)=>s+a.score,0)/history.length): '--'}%</strong></div>
        <div className="p-4 bg-slate-800 rounded">Issues Detected<br/><strong>—</strong></div>
        <div className="p-4 bg-slate-800 rounded">High Risk Issues<br/><strong>—</strong></div>
      </div>
      <section className="grid grid-cols-2 gap-4">
        <div className="p-4 bg-slate-800 rounded">
          <h3 className="mb-2">Quality Trend</h3>
          <div style={{width: '100%', height: 220}}>
            <ResponsiveContainer>
              <LineChart data={trendData}>
                <XAxis dataKey="name" />
                <YAxis domain={[0,100]} />
                <Tooltip />
                <Line type="monotone" dataKey="score" stroke="#4f46e5" strokeWidth={3} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
        <div className="p-4 bg-slate-800 rounded">
          <h3 className="mb-2">Issue Distribution</h3>
          <div style={{width: '100%', height: 220}}>
            <ResponsiveContainer>
              <PieChart>
                <Pie data={distribution} dataKey="value" nameKey="name" innerRadius={40} outerRadius={80}>
                  {distribution.map((entry, idx)=>(<Cell key={idx} fill={COLORS[idx%COLORS.length]} />))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </section>
    </div>
  )
}
