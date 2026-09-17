import React from 'react'
import { Sun, Moon } from 'lucide-react'
import { useTheme } from '../hooks/useTheme'

export default function Topbar(){
  const { dark, toggle } = useTheme()
  return (
    <div className="flex items-center justify-between mb-6">
      <div>
        <div className="text-sm text-slate-400">CodeSense</div>
        <div className="text-xl font-semibold">Python Code Intelligence</div>
      </div>
      <div className="flex items-center gap-3">
        <button aria-label="toggle theme" onClick={toggle} className="p-2 rounded bg-slate-800 hover:bg-slate-700">
          {dark ? <Sun /> : <Moon />}
        </button>
      </div>
    </div>
  )
}
