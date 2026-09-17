import React from 'react'
import { NavLink } from 'react-router-dom'
import { Home, Search, Grid, PieChart, Settings } from 'lucide-react'

export default function Sidebar(){
  const linkClass = (isActive:boolean) => `flex items-center gap-3 p-2 rounded ${isActive? 'bg-slate-700':''}`
  return (
    <aside className="w-72 bg-gradient-to-b from-slate-800 to-slate-900 p-6 min-h-screen flex flex-col">
      <h1 className="text-2xl font-semibold mb-6">CodeSense</h1>
      <nav className="space-y-3">
        <NavLink to="/" className={({isActive})=>linkClass(isActive)}><Home /> Dashboard</NavLink>
        <NavLink to="/analyze" className={({isActive})=>linkClass(isActive)}><Search /> Analyze Code</NavLink>
        <NavLink to="/history" className={({isActive})=>linkClass(isActive)}><Grid /> History</NavLink>
        <a className="flex items-center gap-3 p-2 rounded hover:bg-slate-700"><PieChart /> Analytics</a>
        <a className="flex items-center gap-3 p-2 rounded hover:bg-slate-700"><Settings /> Settings</a>
      </nav>
      <div className="mt-auto text-sm text-slate-400 pt-6">
        <div>CodeSense v1.0</div>
        <div>Local Static Analyzer</div>
      </div>
    </aside>
  )
}
