import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Sidebar from './components/Sidebar'
import Dashboard from './pages/Dashboard'
import Analyze from './pages/Analyze'
import History from './pages/History'
import Result from './pages/Result'
import Topbar from './components/Topbar'
import { ThemeProvider } from './hooks/useTheme'

export default function App(){
  return (
    <BrowserRouter>
    <ThemeProvider>
    <div className="min-h-screen bg-gray-900 text-gray-100 dark:bg-slate-900">
      <div className="flex">
        <Sidebar />
        <main className="flex-1 p-6">
          <Topbar />
          <Routes>
            <Route path="/" element={<Dashboard/>} />
            <Route path="/analyze" element={<Analyze/>} />
            <Route path="/history" element={<History/>} />
            <Route path="/history/:id" element={<Result/>} />
          </Routes>
        </main>
      </div>
    </div>
    </ThemeProvider>
    </BrowserRouter>
  )
}
