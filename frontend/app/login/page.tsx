'use client'
import { useState } from 'react'
export default function Login(){
  const [email,setEmail]=useState(''); const [password,setPassword]=useState(''); const [msg,setMsg]=useState('')
  const login=async()=>{
    const r=await fetch((process.env.NEXT_PUBLIC_API_URL||'http://localhost:8000')+'/auth/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email,password})})
    const j=await r.json(); if(r.ok){ localStorage.setItem('token', j.access); setMsg('OK') } else setMsg(j.detail||'err')
  }
  return <div><h2>Login</h2><input placeholder="email" value={email} onChange={e=>setEmail(e.target.value)}/><br/><input placeholder="password" type="password" value={password} onChange={e=>setPassword(e.target.value)}/><br/><button onClick={login}>Login</button><p>{msg}</p></div>
}
