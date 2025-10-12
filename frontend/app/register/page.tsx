'use client'
import { useState } from 'react'
export default function Register(){
  const [email,setEmail]=useState(''); const [password,setPassword]=useState(''); const [msg,setMsg]=useState('')
  const reg=async()=>{
    const r=await fetch((process.env.NEXT_PUBLIC_API_URL||'http://localhost:8000')+'/auth/register',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email,password})})
    const j=await r.json(); setMsg(r.ok?'Registered':'Error: '+(j.detail||''))
  }
  return <div><h2>Register</h2><input placeholder="email" value={email} onChange={e=>setEmail(e.target.value)}/><br/><input placeholder="password" type="password" value={password} onChange={e=>setPassword(e.target.value)}/><br/><button onClick={reg}>Create</button><p>{msg}</p></div>
}
