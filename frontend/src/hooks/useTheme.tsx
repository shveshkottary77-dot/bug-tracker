import React, { createContext, useContext, useEffect, useState } from 'react'

const ThemeContext = createContext({ dark:true, toggle: ()=>{} })

export const ThemeProvider = ({ children }: { children: React.ReactNode }) => {
  const [dark, setDark] = useState<boolean>(()=>{
    try{ return localStorage.getItem('codesense:dark') !== 'false' }catch{ return true }
  })
  useEffect(()=>{
    try{ localStorage.setItem('codesense:dark', dark ? 'true':'false') }catch{}
    if(dark) document.documentElement.classList.add('dark')
    else document.documentElement.classList.remove('dark')
  },[dark])
  return <ThemeContext.Provider value={{ dark, toggle: ()=>setDark(d=>!d) }}>{children}</ThemeContext.Provider>
}

export const useTheme = () => useContext(ThemeContext)
